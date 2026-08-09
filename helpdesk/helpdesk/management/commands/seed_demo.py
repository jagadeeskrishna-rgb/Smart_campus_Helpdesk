from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from helpdesk.models import Profile, ServiceCategory, Ticket, TicketComment
from helpdesk.services import assign_ticket


class Command(BaseCommand):
    help = "Create demo users, categories, and tickets for academic evaluation."

    def handle(self, *args, **options):
        admin, _ = User.objects.get_or_create(username="admin", defaults={"email": "admin@example.com", "is_staff": True, "is_superuser": True})
        admin.set_password("Admin@12345")
        admin.is_staff = True
        admin.is_superuser = True
        admin.save()
        admin.profile.role = Profile.Role.ADMIN
        admin.profile.save()

        tech, _ = User.objects.get_or_create(username="technician", defaults={"email": "tech@example.com", "first_name": "Campus", "last_name": "Technician"})
        tech.set_password("Tech@12345")
        tech.save()
        tech.profile.role = Profile.Role.TECHNICIAN
        tech.profile.department = "IT and Maintenance"
        tech.profile.save()

        student, _ = User.objects.get_or_create(username="student", defaults={"email": "student@example.com", "first_name": "Demo", "last_name": "Student"})
        student.set_password("Student@12345")
        student.save()
        student.profile.role = Profile.Role.STUDENT
        student.profile.department = "Computer Science"
        student.profile.save()

        category_names = [
            ("IT and Network Support", "Wi-Fi, lab systems, projectors, printers, and software issues."),
            ("Campus Infrastructure and Maintenance", "Fan, light, water, furniture, hostel, and classroom maintenance."),
            ("Administrative and Student Services", "ID card, certificate, fee receipt, and transport pass requests."),
            ("Library and Academics", "Book requests, library card issues, and academic document support."),
        ]
        categories = []
        for name, description in category_names:
            category, _ = ServiceCategory.objects.get_or_create(name=name, defaults={"description": description})
            categories.append(category)

        if not Ticket.objects.exists():
            ticket = Ticket.objects.create(
                title="Projector not working in Seminar Hall",
                description="The projector displays no input during morning classes.",
                category=categories[0],
                priority=Ticket.Priority.HIGH,
                location="Seminar Hall A",
                created_by=student,
            )
            assign_ticket(ticket, tech, admin)
            TicketComment.objects.create(ticket=ticket, author=student, message="This is needed for afternoon presentation practice.")
            Ticket.objects.create(
                title="Library card barcode unreadable",
                description="The library scanner cannot read the current ID barcode.",
                category=categories[3],
                priority=Ticket.Priority.MEDIUM,
                location="Central Library",
                created_by=student,
            )

        self.stdout.write(self.style.SUCCESS("Demo data created."))
