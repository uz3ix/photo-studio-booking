from django.urls import path

from . import views

app_name = "studios"
urlpatterns = [
    path("", views.studios, name="list"),
    path("available/", views.available_studios, name="available"),
    path("<int:studio_id>/", views.studio_detail, name="detail"),
]
