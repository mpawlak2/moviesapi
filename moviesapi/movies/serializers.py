from rest_framework import serializers

from movies.models import Movie


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = (
            "id",
            "title",
            "year",
            "rated",
            "released",
            "runtime",
            "genre",
            "director",
            "writer",
            "actors",
            "plot",
        )
