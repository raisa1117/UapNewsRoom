from django.apps import AppConfig
from django.db.models.signals import post_migrate, post_save

DEPTS = [("CSE", "Computer Science & Engineering"), ("EEE", "Electrical & Electronic Engineering"),
         ("CE", "Civil Engineering"), ("ARCH", "Architecture"), ("PHARM", "Pharmacy"),
         ("LAW", "Law"), ("ENG", "English"), ("BBA", "Business Administration")]

def seed(sender, **kw):
    from .models import Department
    if not Department.objects.exists():
        Department.objects.bulk_create([Department(code=c, name=n) for c, n in DEPTS])

def make_profile(sender, instance, created, **kw):
    from .models import MemberProfile
    if created:
        MemberProfile.objects.create(user=instance)

class MembersConfig(AppConfig):
    name = "members"
    def ready(self):
        from django.contrib.auth import get_user_model
        post_save.connect(make_profile, sender=get_user_model())
        post_migrate.connect(seed, sender=self)
