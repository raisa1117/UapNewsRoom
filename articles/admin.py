
from django.contrib import admin
from .models import (
    Section,
    Keyword,
    Article,
    Reply,
    Favourite,
    Subscription,
)


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ("name", "color", "created_at", "updated_at")
    search_fields = ("name",)


@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "updated_at")
    search_fields = ("name",)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "kind",
        "section",
        "writer",
        "state",
        "reads",
        "created_at",
        "updated_at",
    )
    list_filter = ("state", "kind", "section")
    search_fields = ("title", "body", "writer__username")
    filter_horizontal = ("keywords",)
    readonly_fields = ("created_at", "updated_at", "reads")
    date_hierarchy = "created_at"


@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ("article", "writer", "created_at", "updated_at")
    search_fields = ("text", "writer__username")


@admin.register(Favourite)
class FavouriteAdmin(admin.ModelAdmin):
    list_display = ("user", "article", "created_at", "updated_at")


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("user", "section", "created_at", "updated_at")
