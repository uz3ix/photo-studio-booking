"""Корневой уровень маршрутов."""

from django.urls import include, path

urlpatterns = [
    path("", include("homepage.urls")),
    path("studios/", include("studios.urls")),
    path("bookings/", include("bookings.urls")),
]
