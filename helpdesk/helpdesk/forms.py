from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile, ServiceCategory, Ticket, TicketAttachment, TicketComment


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    department = forms.CharField(max_length=120, required=False)
    phone = forms.CharField(max_length=20, required=False)

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "department", "phone", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            user.profile.department = self.cleaned_data.get("department", "")
            user.profile.phone = self.cleaned_data.get("phone", "")
            user.profile.save()
        return user


class TicketForm(forms.ModelForm):
    attachment = forms.FileField(required=False)

    class Meta:
        model = Ticket
        fields = ["title", "description", "category", "priority", "location"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }

    def clean_title(self):
        title = self.cleaned_data["title"].strip()
        if len(title) < 8:
            raise forms.ValidationError("Please enter at least 8 characters.")
        return title


class TicketAttachmentForm(forms.ModelForm):
    class Meta:
        model = TicketAttachment
        fields = ["file"]


class TicketCommentForm(forms.ModelForm):
    class Meta:
        model = TicketComment
        fields = ["message"]
        widgets = {"message": forms.Textarea(attrs={"rows": 3, "placeholder": "Add a comment or update..."})}


class TicketAssignForm(forms.ModelForm):
    assigned_to = forms.ModelChoiceField(
        queryset=User.objects.filter(profile__role=Profile.Role.TECHNICIAN),
        empty_label="Select technician",
    )

    class Meta:
        model = Ticket
        fields = ["assigned_to"]


class TicketStatusForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["status", "resolution_notes"]
        widgets = {"resolution_notes": forms.Textarea(attrs={"rows": 3})}


class ServiceCategoryForm(forms.ModelForm):
    class Meta:
        model = ServiceCategory
        fields = ["name", "description", "is_active"]
