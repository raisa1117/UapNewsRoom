from django.conf import settings
from django.db import models```python
# Import Django settings to reference the configured user model.
from django.conf import settings 
# Import Django model classes and field definitions.
from django.db import models 
 
# Get the active user model configured in the project settings.
USER = settings.AUTH_USER_MODEL 
 
# Define the model for recording editorial decisions on articles.```python
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

    # Save the verdict selected by the editor.
    verdict = models.CharField(max_length=10, choices=VERDICTS) 

    # Store an optional note explaining the decision.
    note = models.CharField(max_length=240, blank=True) 

    # Automatically record when the decision is created.
    created_at = models.DateTimeField(auto_now_add=True) 

    # Configure the default ordering for decision records.
    class Meta: 
        ordering = ["-created_at"] 

# Define the model for article reports submitted by users.
class Flag(models.Model): 

    # Reference the article associated with the report.
    article = models.ForeignKey("articles.Article", on_delete=models.CASCADE, related_name="flags") 

    # Identify the user who submitted the report.
    raised_by = models.ForeignKey(USER, on_delete=models.CASCADE, related_name="flags_raised") 

    # Store the reason provided for reporting the article.
    reason = models.CharField(max_length=240) 

    # Indicate whether the report has been resolved.
    closed = models.BooleanField(default=False) 

    # Record the date and time when the report was submitted.
    created_at = models.DateTimeField(auto_now_add=True) 

    # Configure the default ordering for reported items.
    class Meta: 
        ordering = ["-created_at"] 

        # Prevent duplicate reports from the same user for the same article.
        constraints = [models.UniqueConstraint(fields=["article", "raised_by"], name="flag_once")] 

# Define the model for user notifications and alerts.
class Alert(models.Model): 

    # Specify the user who receives the notification.
    to_user = models.ForeignKey(USER, on_delete=models.CASCADE, related_name="alerts") 

    # Optionally associate the notification with an article.
    article = models.ForeignKey("articles.Article", on_delete=models.CASCADE, null=True, blank=True, related_name="alerts") 

    # Store the notification message.
    text = models.CharField(max_length=240) 

    # Track whether the notification has been viewed.
    seen = models.BooleanField(default=False) 

    # Automatically record when the notification is created.
    created_at = models.DateTimeField(auto_now_add=True) 

    # Display the newest notifications first.
    class Meta: 
        ordering = ["-created_at"] 

# Define the model for publishing announcements.
class Announcement(models.Model): 

    # Record the user responsible for publishing the announcement.
    posted_by = models.ForeignKey(USER, on_delete=models.CASCADE, related_name="announcements") 

    # Store the announcement content.
    text = models.CharField(max_length=200) 

    # Determine whether the announcement is currently active.
    active = models.BooleanField(default=True) 

    # Automatically record when the announcement is created.
    created_at = models.DateTimeField(auto_now_add=True) 

    # Display announcements in reverse chronological order.
    class Meta: 
        ordering = ["-created_at"] 

    # Return the announcement text as its string representation.
    def __str__(self): 
        return self.text
```

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
