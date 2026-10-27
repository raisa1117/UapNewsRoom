from django.urls import path
from . import views
urlpatterns = [
    path("", views.front, name="front"),
    path("article/<int:pk>/", views.read, name="read"),
    path("write/", views.write, name="write"),
    path("article/<int:pk>/edit/", views.rewrite, name="rewrite"),
    path("mine/", views.mine, name="mine"),
    path("favourites/", views.favourites, name="favourites"),
    path("article/<int:pk>/reply/", views.reply, name="reply"),
    path("article/<int:pk>/favourite/", views.favourite, name="favourite"),
    path("section/<int:pk>/follow/", views.follow, name="follow"),
]
