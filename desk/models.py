from django.conf import settings
from django.db import models```python
# Import Django settings to reference the configured user model.
from django.conf import settings 
# Import Django model classes and field definitions.
from django.db import models 
 
# Get the active user model configured in the project settings.
USER = settings.AUTH_USER_MODEL 
 
# Define the model for recording editorial decisions on articles.
class Decision(models.Model): 
    """One editor verdict on one article (audit trail).""" 

    # Define the possible approval and rejection outcomes.
    VERDICTS = [("approve", "Approved"), ("reject", "Rejected")] 

    # Connect each editorial decision to its associated article.
    article = models.ForeignKey("articles.Article", on_delete=models.CASCADE, related_name="decisions") 

    # Store the editor responsible for the decision.
    editor = models.ForeignKey(USER, on_delete=models.SET_NULL, null=True, related_name="decisions_made") 

    # Save the verdict selected by the ed
```

USER = settings.AUTH_USER_MODEL

class Decision(models.Model):
    """One editor verdict on one article (audit trail)."""
    VERDICTS = [("approve", "Approved"), ("reject", "Rejected")]
    article = models.ForeignKey("articles.Article", on_delete=models.CASCADE, related_name="decisions")
    editor = models.ForeignKey(USER, on_delete=models.SET_NULL, null=True, related_name="decisions_made")
    verdict = models.CharField(max_length=10, choices=VERDICTS)
    note = models.CharField(max_length=240, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ["-created_at"]

class Flag(models.Model):
    article = models.ForeignKey("articles.Article", on_delete=models.CASCADE, related_name="flags")
    raised_by = models.ForeignKey(USER, on_delete=models.CASCADE, related_name="flags_raised")
    reason = models.CharField(max_length=240)
    closed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ["-created_at"]
        constraints = [models.UniqueConstraint(fields=["article", "raised_by"], name="flag_once")]

class Alert(models.Model):
    to_user = models.ForeignKey(USER, on_delete=models.CASCADE, related_name="alerts")
    article = models.ForeignKey("articles.Article", on_delete=models.CASCADE, null=True, blank=True, related_name="alerts")
    text = models.CharField(max_length=240)
    seen = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ["-created_at"]

class Announcement(models.Model):
    posted_by = models.ForeignKey(USER, on_delete=models.CASCADE, related_name="announcements")
    text = models.CharField(max_length=200)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ["-created_at"]
    def __str__(self):
        return self.text
