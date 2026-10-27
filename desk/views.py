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
