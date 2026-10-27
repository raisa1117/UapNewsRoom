```python
# Import decorators for authentication and staff-only access control.
from django.contrib.auth.decorators import login_required, user_passes_test 
# Import HTTP exceptions and JSON response utilities.
from django.http import Http404, JsonResponse 
# Import shortcuts for retrieving objects and rendering templates.
from django.shortcuts import get_object_or_404, render 
# Import timezone utilities for publication timestamps.
from django.utils import timezone 
# Import the decorator that restricts views to POST requests.
from django.views.decorators.http import require_POST 
# Import the Article model used by the editorial workflow.
from articles.models import Article 
# Import models for alerts, editorial decisions, and article reports.
from .models import Alert, Decision, Flag 
# Import the function that notifies article followers.
from .notify import notify_followers 
 
# Restrict editorial desk access to staff users.
staff_only = user_passes_test(lambda u: u.is_staff, login_url="login") 
 
# Display the editorial dashboard for staff members.
@staff_only 
def desk(request): 
    # Render the dashboard with pending articles, open reports, and recent decisions.
    return render(request, "desk/desk.html", { 
        # Retrieve pending articles with their related section and writer.
        "pending": Article.objects.filter(state=Article.PENDING).select_related("section", "writer").order_by("created_at"), 
        # Retrieve unresolved reports with related article and reporter details.
        "flags": Flag.objects.filter(closed=False).select_related("article", "raised_by"), 
        # Retrieve the six most recent editorial decisions.
        "history": Decision.objects.select_related("article", "editor")[:6]})

# Process an editor's decision for a pending article.
@staff_only 
@require_POST 
def decide(request, pk, verdict): 
    # Reject unsupported editorial verdicts.
    if verdict not in ("approve", "reject"): 
        raise Http404 

    # Retrieve the article selected for editorial review.
    art = get_object_or_404(Article, pk=pk) 

    # Read the editor's note and limit its length.
    note = request.POST.get("note", "").strip()[:240] 

    # Update the article when the editor approves it.
    if verdict == "approve": 
        art.state, art.published_at, art.editor_note = Article.LIVE, timezone.now(), "" 
        # Prepare a publication notification for the writer.
        text = f'Your article "{art.title}" is now live.' 
    # Update the article when the editor rejects it.
    else: 
        art.state, art.editor_note = Article.REJECTED, note 
        # Prepare a rejection notification, including the editor's note when available.
        text = f'Your article "{art.title}" was rejected.' + (f" Editor's note: {note}" if note else "") 

    # Save the updated article information.
    art.save() 

    # Record the editorial decision for future reference.
    Decision.objects.create(article=art, editor=request.user, verdict=verdict, note=note) 

    # Notify the article writer about the editorial decision.
    Alert.objects.create(to_user=art.writer, article=art, text=text) 

    # Notify followers when the article is approved.
    if verdict == "approve": 
        notify_followers(art) 

    # Return the remaining pending article count as a JSON response.
    return JsonResponse({"ok": True, "left": Article.objects.filter(state=Article.PENDING).count()}) 
 
# Allow authenticated users to report published articles.
@login_required 
@require_POST 
def flag(request, pk): 
    # Retrieve the published article that the user wants to report.
    art = get_object_or_404(Article, pk=pk, state=Article.LIVE) 

    # Read the report reason and provide a default if it is empty.
    reason = request.POST.get("reason", "").strip()[:240] or "No reason given" 

    # Create a report only if this user has not already reported the article.
    _, made = Flag.objects.get_or_create(article=art, raised_by=request.user, defaults={"reason": reason}) 

    # Return whether a new report was created.
    return JsonResponse({"ok": True, "new": made}) 
 
# Allow staff members to close article reports.
@staff_only 
@require_POST 
def close_flag(request, pk): 
    # Mark the selected report as closed.
    Flag.objects.filter(pk=pk).update(closed=True) 

    # Return confirmation that the report was closed.
    return JsonResponse({"ok": True}) 
 
# Display notifications for the currently authenticated user.
@login_required 
def alerts(request): 
    # Retrieve the user's notifications along with related article data.
    items = list(request.user.alerts.select_related("article")) 

    # Mark all unseen notifications as viewed.
    request.user.alerts.filter(seen=False).update(seen=True) 

    # Render the notifications page with the retrieved items.
    return render(request, "desk/alerts.html", {"items": items})
```
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views.decorators.http import require_POST
from articles.models import Article
from .models import Alert, Decision, Flag
from .notify import notify_followers

staff_only = user_passes_test(lambda u: u.is_staff, login_url="login")

@staff_only
def desk(request):
    return render(request, "desk/desk.html", {
        "pending": Article.objects.filter(state=Article.PENDING).select_related("section", "writer").order_by("created_at"),
        "flags": Flag.objects.filter(closed=False).select_related("article", "raised_by"),
        "history": Decision.objects.select_related("article", "editor")[:6]})
```python
# Import decorators for authentication and staff-only access control.
from django.contrib.auth.decorators import login_required, user_passes_test
# Import HTTP exceptions and JSON response utilities.
from django.http import Http404, JsonResponse
# Import shortcuts for retrieving objects and rendering templates.
from django.shortcuts import get_object_or_404, render
# Import timezone utilities for publication timestamps.
from django.utils import timezone
# Import the decorator that restricts views to POST requests.
from django.views.decorators.http import require_POST
# Import the Article model used by the editorial workflow.
from articles.models import Article
# Import models for a
```

@staff_only
@require_POST
def decide(request, pk, verdict):
    if verdict not in ("approve", "reject"):
        raise Http404
    art = get_object_or_404(Article, pk=pk)
    note = request.POST.get("note", "").strip()[:240]
    if verdict == "approve":
        art.state, art.published_at, art.editor_note = Article.LIVE, timezone.now(), ""
        text = f'Your article "{art.title}" is now live.'
    else:
        art.state, art.editor_note = Article.REJECTED, note
        text = f'Your article "{art.title}" was rejected.' + (f" Editor's note: {note}" if note else "")
    art.save()
    Decision.objects.create(article=art, editor=request.user, verdict=verdict, note=note)
    Alert.objects.create(to_user=art.writer, article=art, text=text)
    if verdict == "approve":
        notify_followers(art)
    return JsonResponse({"ok": True, "left": Article.objects.filter(state=Article.PENDING).count()})

@login_required
@require_POST
def flag(request, pk):
    art = get_object_or_404(Article, pk=pk, state=Article.LIVE)
    reason = request.POST.get("reason", "").strip()[:240] or "No reason given"
    _, made = Flag.objects.get_or_create(article=art, raised_by=request.user, defaults={"reason": reason})
    return JsonResponse({"ok": True, "new": made})

@staff_only
@require_POST
def close_flag(request, pk):
    Flag.objects.filter(pk=pk).update(closed=True)
    return JsonResponse({"ok": True})

@login_required
def alerts(request):
    items = list(request.user.alerts.select_related("article"))
    request.user.alerts.filter(seen=False).update(seen=True)
    return render(request, "desk/alerts.html", {"items": items})
