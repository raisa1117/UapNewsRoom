
from django.conf import settings
from django.core.validators import (
    MaxLengthValidator,
    MinLengthValidator,
    RegexValidator,
)
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils import timezone

USER = settings.AUTH_USER_MODEL


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Section(TimeStampedModel):
    name = models.CharField(max_length=60, unique=True)
    color = models.CharField(
        max_length=7,
        default="#1b6ca8",
        validators=[
            RegexValidator(
                regex=r"^#[0-9a-fA-F]{6}$",
                message="Enter a valid hex color, e.g. #1b6ca8.",
            )
        ],
    )
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
        ]

    def __str__(self):
        return self.name


class Keyword(TimeStampedModel):
    name = models.CharField(max_length=30, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Article(TimeStampedModel):
    PENDING = "pending"
    LIVE = "live"
    REJECTED = "rejected"

    STATES = [
        (PENDING, "Pending"),
        (LIVE, "Live"),
        (REJECTED, "Rejected"),
    ]

    NEWS = "news"
    BLOG = "blog"

    KINDS = [
        (NEWS, "News"),
        (BLOG, "Blog"),
    ]

    title = models.CharField(
        max_length=160,
        validators=[MinLengthValidator(5)],
    )
    slug = models.SlugField(max_length=180, unique=True, blank=True)
    kind = models.CharField(
        "Type",
        max_length=10,
        choices=KINDS,
        default=NEWS,
    )
    section = models.ForeignKey(
        Section,
        on_delete=models.PROTECT,
        related_name="articles",
    )
    keywords = models.ManyToManyField(
        Keyword,
        blank=True,
        related_name="articles",
    )
    body = models.TextField(
        validators=[MinLengthValidator(20)],
    )
    writer = models.ForeignKey(
        USER,
        on_delete=models.CASCADE,
        related_name="articles",
    )
    state = models.CharField(
        max_length=10,
        choices=STATES,
        default=PENDING,
    )
    editor_note = models.CharField(max_length=240, blank=True)
    reads = models.PositiveIntegerField(default=0)
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-published_at", "-created_at"]
        indexes = [
            models.Index(fields=["state", "-created_at"]),
            models.Index(fields=["section", "state"]),
            models.Index(fields=["writer", "-created_at"]),
            models.Index(fields=["kind", "state"]),
        ]
        constraints = [
            models.CheckConstraint(
                condition=Q(reads__gte=0),
                name="article_reads_nonnegative",
            ),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("read", args=[self.pk])

    @property
    def teaser(self):
        return self.body[:170] + ("…" if len(self.body) > 170 else "")

    @property
    def is_published(self):
        return self.state == self.LIVE and self.published_at is not None

    def publish(self):
        self.state = self.LIVE
        if self.published_at is None:
            self.published_at = timezone.now()
        self.save(update_fields=["state", "published_at", "updated_at"])

    def reject(self, note=""):
        self.state = self.REJECTED
        self.editor_note = note[:240]
        self.save(update_fields=["state", "editor_note", "updated_at"])

    def increment_reads(self):
        from django.db.models import F

        Article.objects.filter(pk=self.pk).update(reads=F("reads") + 1)
        self.refresh_from_db(fields=["reads"])


class Reply(TimeStampedModel):
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name="replies",
    )
    writer = models.ForeignKey(
        USER,
        on_delete=models.CASCADE,
        related_name="replies",
    )
    text = models.CharField(
        max_length=500,
        validators=[MinLengthValidator(2)],
    )

    class Meta:
        ordering = ["created_at"]
        verbose_name_plural = "replies"
        indexes = [
            models.Index(fields=["article", "created_at"]),
        ]

    def __str__(self):
        return f"Reply by {self.writer} on {self.article}"


class Favourite(TimeStampedModel):
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name="favourites",
    )
    user = models.ForeignKey(
        USER,
        on_delete=models.CASCADE,
        related_name="favourites",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "article"],
                name="fav_once",
            ),
        ]
        indexes = [
            models.Index(fields=["user", "-created_at"]),
        ]

    def __str__(self):
        return f"{self.user} - {self.article}"


class Subscription(TimeStampedModel):
    section = models.ForeignKey(
        Section,
        on_delete=models.CASCADE,
        related_name="followers",
    )
    user = models.ForeignKey(
        USER,
        on_delete=models.CASCADE,
        related_name="subscriptions",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "section"],
                name="follow_once",
            ),
        ]
        indexes = [
            models.Index(fields=["user", "section"]),
        ]

    def __str__(self):
        return f"{self.user} follows {self.section}"
