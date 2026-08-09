from django.contrib.auth.models import User

from .models import Notification, Ticket, TicketHistory


VALID_TRANSITIONS = {
    Ticket.Status.NEW: {Ticket.Status.ASSIGNED, Ticket.Status.REJECTED},
    Ticket.Status.ASSIGNED: {Ticket.Status.IN_PROGRESS, Ticket.Status.ON_HOLD, Ticket.Status.REJECTED},
    Ticket.Status.IN_PROGRESS: {Ticket.Status.ON_HOLD, Ticket.Status.RESOLVED},
    Ticket.Status.ON_HOLD: {Ticket.Status.IN_PROGRESS, Ticket.Status.REJECTED},
    Ticket.Status.RESOLVED: {Ticket.Status.CLOSED, Ticket.Status.REOPENED},
    Ticket.Status.CLOSED: {Ticket.Status.REOPENED},
    Ticket.Status.REOPENED: {Ticket.Status.ASSIGNED, Ticket.Status.IN_PROGRESS},
    Ticket.Status.REJECTED: set(),
}


def user_role(user: User) -> str:
    return getattr(getattr(user, "profile", None), "role", "student")


def can_view_ticket(user: User, ticket: Ticket) -> bool:
    role = user_role(user)
    if role == "admin":
        return True
    if role == "technician":
        return ticket.assigned_to_id == user.id
    return ticket.created_by_id == user.id


def can_transition(ticket: Ticket, new_status: str) -> bool:
    return new_status in VALID_TRANSITIONS.get(ticket.status, set())


def notify(user: User | None, ticket: Ticket, message: str):
    if user:
        Notification.objects.create(user=user, ticket=ticket, message=message)


def record_history(ticket: Ticket, actor: User | None, previous: str, new: str, note: str):
    TicketHistory.objects.create(
        ticket=ticket,
        actor=actor,
        previous_status=previous or "",
        new_status=new or "",
        note=note,
    )


def assign_ticket(ticket: Ticket, technician: User, actor: User):
    previous = ticket.status
    ticket.assigned_to = technician
    ticket.status = Ticket.Status.ASSIGNED
    ticket.save()
    record_history(ticket, actor, previous, ticket.status, f"Assigned to {technician.get_full_name() or technician.username}")
    notify(ticket.created_by, ticket, f"{ticket.ticket_number} has been assigned.")
    notify(technician, ticket, f"{ticket.ticket_number} has been assigned to you.")
    return ticket


def update_ticket_status(ticket: Ticket, new_status: str, actor: User, note: str = ""):
    previous = ticket.status
    if previous != new_status and not can_transition(ticket, new_status):
        raise ValueError(f"Invalid transition from {previous} to {new_status}")
    ticket.status = new_status
    if note:
        ticket.resolution_notes = note
    ticket.save()
    record_history(ticket, actor, previous, new_status, note or f"Status changed to {ticket.get_status_display()}")
    notify(ticket.created_by, ticket, f"{ticket.ticket_number} status changed to {ticket.get_status_display()}.")
    if ticket.assigned_to_id and ticket.assigned_to_id != actor.id:
        notify(ticket.assigned_to, ticket, f"{ticket.ticket_number} status changed to {ticket.get_status_display()}.")
    return ticket
