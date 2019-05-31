import requests
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.response import Response

from movies.queries import (filter_all_comments, filter_all_movies,
                            filter_movie_by_title)
from movies.serializers import CommentSerializer, MovieSerializer
from movies.services import get_omdbapi_movie_by_title


class MoviesAPI(RetrieveModelMixin, ListCreateAPIView):
    """List-Create-Retrieve API View."""

    serializer_class = MovieSerializer

    def get_queryset(self):
        return filter_all_movies()

    def get_object(self):
        return filter_movie_by_title(self.request.data.get("title"))[0]

    def post(self, request, *args, **kwargs):
        title = request.data.get("title")
        if title:
            if len(filter_movie_by_title(title)) == 1:
                return self.retrieve(request, *args, **kwargs)

        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """The purpose of this override is to communicate with the external API and pass that data to the serializer."""
        serializer_data = {
            "title": request.data.get("title"),
        }

        if serializer_data["title"]:
            movie_data = get_omdbapi_movie_by_title(serializer_data["title"])
            serializer_data.update(movie_data)


        serializer = self.get_serializer(data=serializer_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CommentsAPI(ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        movie_id = self.request.query_params.get("movie", None)
        return filter_all_comments(movie_id=movie_id)
