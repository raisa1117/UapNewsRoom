```python
# Import the path function to define URL patterns
from django.urls import path

# Import views from the current application
from . import views

# Define URL patterns for the application
urlpatterns = [

    # Homepage: display the front page
    path("", views.front, name="front"),

    # Display a specific article using its primary key
    path("article/<int:pk>/", views.read, name="read"),

    # Open the page for writing a new article
    path("write/", views.write, name="write"),

    # Edit an existing article using its primary key
    path("article/<int:pk>/edit/", views.rewrite, name="rewrite"),

    # Display articles written by the current user
    path("mine/", views.mine, name="mine"),

    # Display the user's favourite articles
    path("favourites/", views.favourites, name="favourites"),

    # Add a reply to a specific article
    path("article/<int:pk>/reply/", views.reply, name="reply"),

    # Add or remove an article from the user's favourites
    path("article/<int:pk>/favourite/", views.favourite, name="favourite"),

    # Follow a specific section using its primary key
    path("section/<int:pk>/follow/", views.follow, name="follow"),
]
```
