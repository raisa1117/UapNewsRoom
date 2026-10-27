from django.contrib import admin
from .models import Department, MemberProfile
admin.site.register(Department)
@admin.register(MemberProfile)
class MemberProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "department", "student_id"]
    list_filter = ["department"]
