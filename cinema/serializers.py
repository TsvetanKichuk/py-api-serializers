from rest_framework import serializers
from cinema.models import (
    CinemaHall,
    Movie,
    Order,
    Ticket,
    MovieSession,
    Actor,
    Genre
)


class CinemaHallSerializer(serializers.ModelSerializer):
    class Meta:
        model = CinemaHall
        fields = (
            "id",
            "name",
            "rows",
            "seats_in_row",
            "capacity"
        )


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"


class GenreRetrieveSerializer(GenreSerializer):
    class Meta:
        model = Genre
        fields = ("name",)


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ("id", "first_name", "last_name", "full_name")


class ActorRetrieveSerializer(ActorSerializer):
    class Meta:
        model = Actor
        fields = ("full_name",)


class MovieSerializer(serializers.ModelSerializer):
    actors = ActorRetrieveSerializer(
        source="full_name",
        many=True,
        read_only=True
    )

    class Meta:
        model = Movie
        fields = (
            "id",
            "title",
            "description",
            "duration",
            "genres",
            "actors",
        )
        read_only_fields = ("id",)


class MovieRetrieveSerializer(MovieSerializer):
    genres = GenreSerializer(many=True)
    actors = ActorSerializer(many=True)


class MovieListSerializer(MovieSerializer):
    genres = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name"
    )
    actors = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="full_name"
    )


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = "__all__"


class TicketListSerializer(serializers.ModelSerializer):
    movie_info = serializers.CharField(source="movie.title", read_only=True)
    cinema_hall = serializers.IntegerField(
        source="cinema_hall.name",
        read_only=True
    )

    class Meta:
        model = Ticket
        fields = ("id", "movie_session", "order", "row", "seat")


class TicketRetrieveSerializer(TicketSerializer):
    movie = MovieRetrieveSerializer(many=False, read_only=True)


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class MovieSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieSession
        fields = "__all__"


class MovieSessionRetrieveSerializer(MovieSessionSerializer):
    movie = MovieListSerializer()
    cinema_hall = CinemaHallSerializer()


class MovieSessionListSerializer(MovieSessionSerializer):
    movie_title = serializers.CharField(source="movie.title", read_only=True)
    cinema_hall_name = serializers.CharField(
        source="cinema_hall.name",
        read_only=True
    )
    cinema_hall_capacity = serializers.IntegerField(
        source="cinema_hall.capacity", read_only=True
    )

    class Meta:
        model = MovieSession
        fields = (
            "id",
            "show_time",
            "movie_title",
            "cinema_hall_name",
            "cinema_hall_capacity",
        )
