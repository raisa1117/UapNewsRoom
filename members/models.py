from django.conf import settings
from django.db import models

class Department(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=80, unique=True)
    def __str__(self):
        return self.code

class MemberProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    department = models.ForeignKey(Department, null=True, blank=True, on_delete=models.SET_NULL, related_name="members")
    student_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    def __str__(self):
        return f"{self.user} ({self.department or 'no dept'})"
