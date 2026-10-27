from django.conf import settings
from django.db import models
from django.urls import reverse

USER = settings.AUTH_USER_MODEL

class Section(models.Model):
    name = models.CharField(max_length=60, unique=True)
    color = models.CharField(max_length=7, default="#1b6ca8")
    class Meta:
        ordering = ["name"]
    def __str__(self):
        return self.name

class Keyword(models.Model):
    name = models.CharField(max_length=30, unique=True)
    def __str__(self):
        return self.name

class Article(models.Model):
    PENDING, LIVE, REJECTED = "pending", "live", "rejected"
    STATES = [(PENDING, "Pending"), (LIVE, "Live"), (REJECTED, "Rejected")]
    NEWS, BLOG = "news", "blog"
    KINDS = [(NEWS, "News"), (BLOG, "Blog")]

    title = models.CharField(max_length=160)
    kind = models.CharField("Type", max_length=10, choices=KINDS, default=NEWS)
    section = models.ForeignKey(Section, on_delete=models.PROTECT, related_name="articles")
    keywords = models.ManyToManyField(Keyword, blank=True, related_name="articles")
    body = models.TextField()
    writer = models.ForeignKey(USER, on_delete=models.CASCADE, related_name="articles")
    state = models.CharField(max_length=10, choices=STATES, default=PENDING)
    editor_note = models.CharField(max_length=240, blank=True)
    reads = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(null=True, blank=True)
    class Meta:
        ordering = ["-published_at", "-created_at"]
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse("read", args=[self.pk])
    @property
    def teaser(self):
        return self.body[:170] + ("…" if len(self.body) > 170 else "")

class Reply(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="replies")
    writer = models.ForeignKey(USER, on_delete=models.CASCADE, related_name="replies")
    text = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ["created_at"]
        verbose_name_plural = "replies"

class Favourite(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="favourites")
    user = models.ForeignKey(USER, on_delete=models.CASCADE, related_name="favourites")
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints = [models.UniqueConstraint(fields=["user", "article"], name="fav_once")]

class Subscription(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name="followers")
    user = models.ForeignKey(USER, on_delete=models.CASCADE, related_name="subscriptions")
    class Meta:
        constraints = [models.UniqueConstraint(fields=["user", "section"], name="follow_once")]
