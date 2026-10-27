from django.contrib import admin
from django.utils import timezone
from .models import Article, Favourite, Keyword, Reply, Section, Subscription

admin.site.register([Section, Keyword, Reply, Favourite, Subscription])

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ["title", "kind", "section", "writer", "state", "reads"]
    list_filter = ["state", "kind", "section"]
    search_fields = ["title", "body"]
    actions = ["make_live", "reject"]

    @admin.action(description="Publish selected articles")
    def make_live(self, request, qs):
        qs.update(state=Article.LIVE, published_at=timezone.now(), editor_note="")

    @admin.action(description="Reject selected articles")
    def reject(self, request, qs):
        qs.update(state=Article.REJECTED)
