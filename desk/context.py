from articles.models import Article
def badges(request):
    u, out = request.user, {}
    if u.is_authenticated:
        out["alert_count"] = u.alerts.filter(seen=False).count()
        if u.is_staff:
            out["queue_count"] = Article.objects.filter(state=Article.PENDING).count()
    return out
