from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=300, unique=True)
    year = models.CharField(max_length=100, blank=True)
    rated = models.CharField(max_length=10, blank=True)
    released = models.DateField(blank=True)
    runtime = models.PositiveIntegerField(blank=True)
    genre = models.CharField(max_length=500, blank=True)
    director = models.CharField(max_length=100, blank=True)
    writer = models.CharField(max_length=100, blank=True)
    actors = models.CharField(max_length=1000, blank=True)
    plot = models.CharField(max_length=1000, blank=True)
    language = models.CharField(max_length=300, blank=True)
    country = models.CharField(max_length=50, blank=True)
    awards = models.CharField(max_length=1000, blank=True)

    def __str__(self):
        return " ".join([self.title, self.year])
