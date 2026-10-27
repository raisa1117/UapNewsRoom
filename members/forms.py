from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Department, MemberProfile

class SignupForm(UserCreationForm):
    department = forms.ModelChoiceField(queryset=Department.objects.all(), required=False)
    student_id = forms.CharField(max_length=20, required=False)
    class Meta:
        model = User
        fields = ["username", "email"]

    def clean_student_id(self):
        sid = self.cleaned_data["student_id"].strip()
        if sid and MemberProfile.objects.filter(student_id=sid).exists():
            raise forms.ValidationError("That student ID is already registered.")
        return sid or None

    def save(self, commit=True):
        user = super().save(commit)
        prof = user.profile
        prof.department, prof.student_id = self.cleaned_data["department"], self.cleaned_data["student_id"]
        prof.save()
        return user
