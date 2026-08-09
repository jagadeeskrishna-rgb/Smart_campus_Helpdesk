from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from .models import Profile, ServiceCategory, Ticket, TicketComment
from .services import assign_ticket, can_view_ticket, update_ticket_status


class HelpdeskWorkflowTests(TestCase):
    def setUp(self):
        self.category = ServiceCategory.objects.create(name="IT and Network Support")
        self.student = User.objects.create_user(username="student1", password="Student@12345")
        self.tech = User.objects.create_user(username="tech1", password="Tech@12345")
        self.admin = User.objects.create_user(username="admin1", password="Admin@12345")
        self.tech.profile.role = Profile.Role.TECHNICIAN
        self.tech.profile.save()
        self.admin.profile.role = Profile.Role.ADMIN
        self.admin.profile.save()

    def test_student_ticket_creation_assigns_ticket_number(self):
        ticket = Ticket.objects.create(
            title="Wi-Fi not working in lab",
            description="Students cannot connect to Wi-Fi in Lab 2.",
            category=self.category,
            priority=Ticket.Priority.HIGH,
            location="Lab 2",
            created_by=self.student,
        )
        self.assertTrue(ticket.ticket_number.startswith("SCH-"))
        self.assertEqual(ticket.status, Ticket.Status.NEW)

    def test_admin_assignment_notifies_student_and_technician(self):
        ticket = Ticket.objects.create(
            title="Projector failure",
            description="Projector is not showing HDMI input.",
            category=self.category,
            priority=Ticket.Priority.URGENT,
            location="Room 204",
            created_by=self.student,
        )
        assign_ticket(ticket, self.tech, self.admin)
        ticket.refresh_from_db()
        self.assertEqual(ticket.assigned_to, self.tech)
        self.assertEqual(ticket.status, Ticket.Status.ASSIGNED)
        self.assertEqual(ticket.history.count(), 1)

    def test_student_cannot_view_another_student_ticket(self):
        other = User.objects.create_user(username="other", password="Other@12345")
        ticket = Ticket.objects.create(
            title="Fan issue in room",
            description="Fan is noisy and slow.",
            category=self.category,
            priority=Ticket.Priority.LOW,
            location="Classroom 101",
            created_by=other,
        )
        self.assertFalse(can_view_ticket(self.student, ticket))
        self.assertTrue(can_view_ticket(other, ticket))

    def test_technician_can_update_status(self):
        ticket = Ticket.objects.create(
            title="Printer offline",
            description="Printer in admin office is offline.",
            category=self.category,
            priority=Ticket.Priority.MEDIUM,
            location="Admin Office",
            created_by=self.student,
        )
        assign_ticket(ticket, self.tech, self.admin)
        update_ticket_status(ticket, Ticket.Status.IN_PROGRESS, self.tech, "Started troubleshooting.")
        ticket.refresh_from_db()
        self.assertEqual(ticket.status, Ticket.Status.IN_PROGRESS)

    def test_comment_is_stored_against_ticket(self):
        ticket = Ticket.objects.create(
            title="Lost ID card",
            description="Student lost ID card near library.",
            category=self.category,
            priority=Ticket.Priority.MEDIUM,
            location="Library",
            created_by=self.student,
        )
        TicketComment.objects.create(ticket=ticket, author=self.student, message="Please process replacement.")
        self.assertEqual(ticket.comments.count(), 1)

    def test_ticket_list_requires_login(self):
        response = Client().get(reverse("ticket_list"))
        self.assertEqual(response.status_code, 302)
