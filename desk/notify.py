from articles.models import Subscription
from .models import Alert

def notify_followers(article):
    subs = Subscription.objects.filter(section=article.section).exclude(user=article.writer)
    Alert.objects.bulk_create([
        Alert(to_user_id=s.user_id, article=article, text=f'New in {article.section.name}: "{article.title}"')
        for s in subs])
