from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, F, Q
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST
from desk.models import Alert, Announcement
from desk.notify import notify_followers
from .forms import ArticleForm, ReplyForm
from .models import Article, Favourite, Keyword, Section, Subscription

def _live():
    return Article.objects.filter(state=Article.LIVE).select_related("section", "writer").prefetch_related("keywords")

def _set_keywords(article, raw):
    names = list(dict.fromkeys(k.strip().lower()[:30] for k in raw.split(",") if k.strip()))[:6]
    article.keywords.set([Keyword.objects.get_or_create(name=n)[0] for n in names])

def front(request):
    u = request.user
    sections = Section.objects.annotate(n=Count("articles", filter=Q(articles__state=Article.LIVE)))
    followed = set(u.subscriptions.values_list("section_id", flat=True)) if u.is_authenticated else set()
    stories = _live()
    return render(request, "articles/front.html", {
        "stories": stories, "sections": sections, "followed": followed, "total": len(stories),
        "notice": Announcement.objects.filter(active=True).first()})

def read(request, pk):
    article = get_object_or_404(Article.objects.select_related("section", "writer__profile__department")
                                .prefetch_related("keywords"), pk=pk)
    u = request.user
    if article.state != Article.LIVE and not (u.is_authenticated and (u.is_staff or u == article.writer)):
        raise Http404
    if article.state == Article.LIVE:
        Article.objects.filter(pk=pk).update(reads=F("reads") + 1)
    return render(request, "articles/read.html", {
        "a": article, "replies": article.replies.select_related("writer"), "form": ReplyForm(),
        "fav": u.is_authenticated and article.favourites.filter(user=u).exists(),
        "fav_count": article.favourites.count()})

@login_required
def write(request):
    form = ArticleForm(request.POST or None)
    if form.is_valid():
        art = form.save(commit=False)
        art.writer = request.user
        if request.user.is_staff:
            art.state, art.published_at = Article.LIVE, timezone.now()
        art.save()
        _set_keywords(art, form.cleaned_data["keywords"])
        if art.state == Article.LIVE:
            notify_followers(art)
            messages.success(request, "Published. Staff articles go live immediately.")
        else:
            messages.success(request, "Sent to the desk. You'll get an alert once an editor decides.")
        return redirect("mine")
    return render(request, "articles/write.html", {"form": form, "heading": "New article"})

@login_required
def rewrite(request, pk):
    art = get_object_or_404(Article, pk=pk, writer=request.user)
    form = ArticleForm(request.POST or None, instance=art,
                       initial={"keywords": ", ".join(k.name for k in art.keywords.all())})
    if form.is_valid():
        art = form.save(commit=False)
        if not request.user.is_staff:
            art.state, art.editor_note, art.published_at = Article.PENDING, "", None
        art.save()
        _set_keywords(art, form.cleaned_data["keywords"])
        messages.success(request, "Saved." + ("" if request.user.is_staff else " It is back in the desk queue."))
        return redirect("mine")
    return render(request, "articles/write.html", {"form": form, "heading": "Edit article"})

@login_required
def mine(request):
    return render(request, "articles/mine.html", {"items": request.user.articles.select_related("section")})

@login_required
def favourites(request):
    ids = request.user.favourites.values_list("article_id", flat=True)
    return render(request, "articles/favourites.html", {"stories": _live().filter(pk__in=ids)})

@login_required
@require_POST
def reply(request, pk):
    art = get_object_or_404(Article, pk=pk, state=Article.LIVE)
    form = ReplyForm(request.POST)
    if form.is_valid():
        r = form.save(commit=False)
        r.article, r.writer = art, request.user
        r.save()
        if art.writer != request.user:
            Alert.objects.create(to_user=art.writer, article=art,
                                 text=f'{request.user.username} replied to "{art.title}"')
    return redirect(art)

@login_required
@require_POST
def favourite(request, pk):
    art = get_object_or_404(Article, pk=pk, state=Article.LIVE)
    obj, made = Favourite.objects.get_or_create(user=request.user, article=art)
    if not made:
        obj.delete()
    return JsonResponse({"on": made, "count": art.favourites.count()})

@login_required
@require_POST
def follow(request, pk):
    sec = get_object_or_404(Section, pk=pk)
    obj, made = Subscription.objects.get_or_create(user=request.user, section=sec)
    if not made:
        obj.delete()
    return JsonResponse({"on": made, "name": sec.name})
