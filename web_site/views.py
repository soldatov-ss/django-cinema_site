from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView

from web_site.models import Movie


class CarouselMoviesView(ListView):
    model = Movie
    template_name = 'web_site/index.html'
    context_object_name = 'movie_list'

    def get_queryset(self):
        return Movie.objects.filter(year=2022).order_by('likes')