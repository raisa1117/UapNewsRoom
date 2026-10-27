from django.urls import path
from . import views
urlpatterns = [
    path("desk/", views.desk, name="desk"),
    path("desk/decide/<int:pk>/<str:verdict>/", views.decide, name="decide"),
    path("flag/<int:pk>/", views.flag, name="flag"),
    path("flags/<int:pk>/close/", views.close_flag, name="close_flag"),
    path("alerts/", views.alerts, name="alerts"),
]
