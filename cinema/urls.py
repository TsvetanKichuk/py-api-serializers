from django.urls import path, include
from cinema.views import (
    ActorViewSet,
    MovieViewSet,
    CinemaHallViewSet,
    MovieSessionViewSet,
    GenreViewSet
)
from rest_framework import routers

router = routers.DefaultRouter()
router.register("actors", ActorViewSet)
router.register("genres", GenreViewSet)
router.register("movie_sessions", MovieSessionViewSet)
router.register("movies", MovieViewSet)
router.register("cinema_halls", CinemaHallViewSet)


urlpatterns = [
    path("", include(router.urls))
    ]

app_name = "cinema"
