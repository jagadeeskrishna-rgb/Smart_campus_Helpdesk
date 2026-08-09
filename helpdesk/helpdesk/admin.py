from django.contrib import admin

from .models import Notification, Profile, ServiceCategory, Ticket, TicketAttachment, TicketComment, TicketHistory


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "role", "department", "phone"]
    list_filter = ["role", "department"]
    search_fields = ["user__username", "user__email", "department"]


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "is_active", "created_at"]
    list_filter = ["is_active"]
    search_fields = ["name"]


class AttachmentInline(admin.TabularInline):
    model = TicketAttachment
    extra = 0


class CommentInline(admin.TabularInline):
    model = TicketComment
    extra = 0


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ["ticket_number", "title", "category", "priority", "status", "created_by", "assigned_to", "created_at"]
    list_filter = ["status", "priority", "category"]
    search_fields = ["ticket_number", "title", "location", "created_by__username"]
    inlines = [AttachmentInline, CommentInline]


admin.site.register(TicketHistory)
admin.site.register(Notification)
