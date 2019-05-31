import re

import requests
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.response import Response

from movies.forms import TopArgsForm
from movies.queries import (filter_all_comments, filter_all_movies,
                            filter_movie_by_title, filter_top_movies)
from movies.serializers import (CommentSerializer, MovieSerializer,
                                TopMoviesSerializer)
from movies.services import get_omdbapi_movie_by_title


class MoviesAPI(RetrieveModelMixin, ListCreateAPIView):
    """List-Create-Retrieve API View."""

    serializer_class = MovieSerializer

    def get_queryset(self):
        qs = filter_all_movies()
        filter_fields = (
            "title", "year", "rated", "released",
            "runtime", "genre", "director", "writer",
            "actors", "plot", "language", "country",
            "awards", "poster", "metascore",
        )
        filter_kwargs = {f"{k}__icontains": v for k, v in self.request.query_params.items() if k in filter_fields and bool(v)}

        ord_by = self.request.query_params.get("ord")
        if ord_by:
            """Verify that the column user want to order by is in filter_fields."""
            match = re.match(r"-?([a-z]+)", ord_by)
            if not match:
                ord_by = None
            else:
                if match.group(1) not in filter_fields:
                    ord_by = None

        qs = qs.filter(**filter_kwargs)
        if ord_by:
            qs = qs.order_by(ord_by)
        return qs

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


class TopAPI(ListAPIView):
    serializer_class = TopMoviesSerializer

    def get_queryset(self):
        return filter_top_movies(
            self.request.query_params.get("date_from"),
            self.request.query_params.get("date_to"),
        )

    def get(self, request, *args, **kwargs):
        form = TopArgsForm(request.query_params)
        if form.is_valid():
            return self.list(request, *args, **kwargs)
        else:
            return Response(form.errors, status.HTTP_400_BAD_REQUEST)
