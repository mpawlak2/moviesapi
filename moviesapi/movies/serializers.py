from rest_framework import serializers

from movies.models import Movie


class MovieSerializer(serializers.Serializer):
    class Meta:
        model = Movie
