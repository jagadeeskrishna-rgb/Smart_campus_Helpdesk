from collections import Counter

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (
    RegistrationForm,
    ServiceCategoryForm,
    TicketAssignForm,
    TicketAttachmentForm,
    TicketCommentForm,
    TicketForm,
    TicketStatusForm,
)
from .models import Notification, Profile, ServiceCategory, Ticket, TicketAttachment, TicketComment
from .services import assign_ticket, can_view_ticket, update_ticket_status, user_role


def role_required(*roles):
    def decorator(view_func):
        @login_required
        def wrapper(request, *args, **kwargs):
            if user_role(request.user) not in roles:
                messages.error(request, "You do not have permission to access that page.")
                return redirect("dashboard")
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration completed successfully.")
            return redirect("dashboard")
    else:
        form = RegistrationForm()
    return render(request, "helpdesk/register.html", {"form": form})


def scoped_tickets(user):
    role = user_role(user)
    if role == "admin":
        return Ticket.objects.select_related("category", "created_by", "assigned_to").all()
    if role == "technician":
        return Ticket.objects.select_related("category", "created_by", "assigned_to").filter(assigned_to=user)
    return Ticket.objects.select_related("category", "created_by", "assigned_to").filter(created_by=user)


@login_required
def dashboard(request):
    tickets = scoped_tickets(request.user)
    status_counts = dict(tickets.values_list("status").annotate(total=Count("id")))
    category_counts = dict(tickets.values_list("category__name").annotate(total=Count("id")))
    priority_counts = dict(tickets.values_list("priority").annotate(total=Count("id")))
    context = {
        "role": user_role(request.user),
        "total_tickets": tickets.count(),
        "new_tickets": tickets.filter(status=Ticket.Status.NEW).count(),
        "in_progress_tickets": tickets.filter(status=Ticket.Status.IN_PROGRESS).count(),
        "resolved_tickets": tickets.filter(status=Ticket.Status.RESOLVED).count(),
        "closed_tickets": tickets.filter(status=Ticket.Status.CLOSED).count(),
        "recent_tickets": tickets[:8],
        "status_counts": status_counts,
        "category_counts": category_counts,
        "priority_counts": priority_counts,
    }
    return render(request, "helpdesk/dashboard.html", context)


@login_required
def ticket_list(request):
    tickets = scoped_tickets(request.user)
    query = request.GET.get("q", "").strip()
    status = request.GET.get("status", "").strip()
    priority = request.GET.get("priority", "").strip()
    category = request.GET.get("category", "").strip()
    if query:
        tickets = tickets.filter(Q(ticket_number__icontains=query) | Q(title__icontains=query) | Q(location__icontains=query))
    if status:
        tickets = tickets.filter(status=status)
    if priority:
        tickets = tickets.filter(priority=priority)
    if category:
        tickets = tickets.filter(category_id=category)
    paginator = Paginator(tickets, 10)
    page_obj = paginator.get_page(request.GET.get("page"))
    context = {
        "page_obj": page_obj,
        "categories": ServiceCategory.objects.filter(is_active=True),
        "status_choices": Ticket.Status.choices,
        "priority_choices": Ticket.Priority.choices,
        "filters": {"q": query, "status": status, "priority": priority, "category": category},
    }
    return render(request, "helpdesk/ticket_list.html", context)


@login_required
def ticket_create(request):
    if request.method == "POST":
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.created_by = request.user
            ticket.save()
            uploaded = request.FILES.get("attachment")
            if uploaded:
                TicketAttachment.objects.create(ticket=ticket, file=uploaded, uploaded_by=request.user)
            messages.success(request, f"Ticket {ticket.ticket_number} created successfully.")
            return redirect(ticket)
    else:
        form = TicketForm()
    return render(request, "helpdesk/ticket_form.html", {"form": form, "title": "Create Ticket"})


@login_required
def ticket_detail(request, pk):
    ticket = get_object_or_404(Ticket.objects.select_related("category", "created_by", "assigned_to"), pk=pk)
    if not can_view_ticket(request.user, ticket):
        messages.error(request, "You do not have permission to view this ticket.")
        return redirect("ticket_list")
    comment_form = TicketCommentForm()
    attachment_form = TicketAttachmentForm()
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "comment":
            comment_form = TicketCommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.ticket = ticket
                comment.author = request.user
                comment.save()
                messages.success(request, "Comment added.")
                return redirect(ticket)
        if action == "attachment":
            attachment_form = TicketAttachmentForm(request.POST, request.FILES)
            if attachment_form.is_valid():
                attachment = attachment_form.save(commit=False)
                attachment.ticket = ticket
                attachment.uploaded_by = request.user
                attachment.save()
                messages.success(request, "Attachment uploaded.")
                return redirect(ticket)
    context = {
        "ticket": ticket,
        "comment_form": comment_form,
        "attachment_form": attachment_form,
        "role": user_role(request.user),
    }
    return render(request, "helpdesk/ticket_detail.html", context)


@role_required("admin")
def ticket_assign(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    if request.method == "POST":
        form = TicketAssignForm(request.POST, instance=ticket)
        if form.is_valid():
            assign_ticket(ticket, form.cleaned_data["assigned_to"], request.user)
            messages.success(request, "Ticket assigned successfully.")
            return redirect(ticket)
    else:
        form = TicketAssignForm(instance=ticket)
    return render(request, "helpdesk/ticket_assign.html", {"ticket": ticket, "form": form})


@login_required
def ticket_status_update(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    role = user_role(request.user)
    if role not in {"admin", "technician"} or (role == "technician" and ticket.assigned_to_id != request.user.id):
        messages.error(request, "You do not have permission to update this ticket.")
        return redirect(ticket)
    if request.method == "POST":
        form = TicketStatusForm(request.POST, instance=ticket)
        if form.is_valid():
            try:
                update_ticket_status(ticket, form.cleaned_data["status"], request.user, form.cleaned_data["resolution_notes"])
                messages.success(request, "Ticket status updated.")
            except ValueError as exc:
                messages.error(request, str(exc))
            return redirect(ticket)
    return redirect(ticket)


@login_required
def close_ticket(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk, created_by=request.user)
    update_ticket_status(ticket, Ticket.Status.CLOSED, request.user, "Student confirmed closure.")
    messages.success(request, "Ticket closed.")
    return redirect(ticket)


@login_required
def reopen_ticket(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk, created_by=request.user)
    update_ticket_status(ticket, Ticket.Status.REOPENED, request.user, "Student reopened the ticket.")
    messages.success(request, "Ticket reopened.")
    return redirect(ticket)


@role_required("admin")
def category_list(request):
    categories = ServiceCategory.objects.annotate(ticket_count=Count("tickets"))
    return render(request, "helpdesk/category_list.html", {"categories": categories})


@role_required("admin")
def category_create(request):
    if request.method == "POST":
        form = ServiceCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Service category created.")
            return redirect("category_list")
    else:
        form = ServiceCategoryForm()
    return render(request, "helpdesk/category_form.html", {"form": form})


@login_required
def notifications(request):
    items = request.user.notifications.select_related("ticket")[:50]
    request.user.notifications.filter(is_read=False).update(is_read=True)
    return render(request, "helpdesk/notifications.html", {"notifications": items})
