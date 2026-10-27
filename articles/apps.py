from django.apps import AppConfig
from django.db.models.signals import post_migrate

SECTIONS = [("Campus News", "#d7263d"), ("Academics", "#1b6ca8"), ("Research", "#6a4c93"), ("Events", "#e07a1f"),
            ("Sports", "#2a9d5c"), ("Student Life", "#c2185b"), ("Opinion", "#455a64")]

def seed(sender, **kw):
    from .models import Section
    if not Section.objects.exists():
        Section.objects.bulk_create([Section(name=n, color=c) for n, c in SECTIONS])

class ArticlesConfig(AppConfig):
    name = "articles"
    def ready(self):
        post_migrate.connect(seed, sender=self)
