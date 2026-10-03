from django.urls import path

from . import views

app_name = "studios"
urlpatterns = [
    path("", views.studios, name="list"),
    path("<int:studio_id>/", views.studio_detail, name="detail"),
]
