from django.shortcuts import render
from django.http import Http404, HttpResponse


def placeholder(request):
    return HttpResponse()
