from django.contrib import admin
from .models import Alert, Announcement, Decision, Flag

@admin.register(Decision)
class DecisionAdmin(admin.ModelAdmin):
    list_display = ["article", "editor", "verdict", "created_at"]
    list_filter = ["verdict"]

@admin.register(Flag)
class FlagAdmin(admin.ModelAdmin):
    list_display = ["article", "raised_by", "reason", "closed"]
    list_filter = ["closed"]

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ["text", "posted_by", "active"]

admin.site.register(Alert)
