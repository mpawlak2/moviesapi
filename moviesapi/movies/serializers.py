from rest_framework import serializers

from movies.models import Movie, Rating, Comment


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = (
            "source",
            "value",
        )


class MovieSerializer(serializers.ModelSerializer):
    ratings = RatingSerializer(many=True, required=False)

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
            "language",
            "country",
            "awards",
            "poster",
            "ratings",
            "metascore",
            "imdbrating",
            "imdbvotes",
            "imdbid",
            "type",
            "totalseasons",
        )

    def create(self, validated_data):
        ratings = validated_data.pop("ratings")
        movie = Movie.objects.create(**validated_data)

        for rating_data in ratings:
            Rating.objects.create(movie=movie, **rating_data)
        return movie


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            "id",
            "body",
            "movie",
        )


class TopMoviesSerializer(serializers.Serializer):
    pass
