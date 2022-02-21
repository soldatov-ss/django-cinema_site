from django.shortcuts import render, redirect

# Create your views here.
from django.views import View
from django.views.generic import ListView, DetailView, CreateView

from web_site.forms import ReviewForm
from web_site.models import Movie, Genre, Actor


class MoviesFilter:

    def get_genres(self):
        return Genre.objects.all()



class MoviesView(MoviesFilter, View):
    model = Movie
    template_name = 'web_site/index.html'

    def get(self, request):
        carousel_movies = Movie.objects.order_by('likes')[:12]
        premieres = Movie.objects.order_by('-world_premiere')[:8]
        new_movies = Movie.objects.order_by('-year')[:18]
        cartoon_id = Genre.objects.get(name='мультфильм')
        cartoons_list = Movie.objects.filter(genres=cartoon_id).order_by('-year')[:12]

        context = {'carousel_list': carousel_movies, 'premieres_list': premieres, 'cartoons_list': cartoons_list,
                   'new_movies_list': new_movies}
        return render(request, 'web_site/index.html', context)


class SingleMovieView(DetailView):
    model = Movie
    template_name = 'web_site/movie_detail.html'
    context_object_name = 'movie'


class AddReview(View):
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get('parent', None):
                form.parent_id = int(request.POST.get('parent'))
            form.movie = movie
            form.save()
        return redirect(movie.get_absolute_url())


class ActorDetailView(DetailView):
    model = Actor
    template_name = 'web_site/actor_detail.html'
    slug_field = 'name'
    context_object_name = 'actor'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['actor_movie_lst'] = Movie.objects.filter(actors=self.object)
        return context


class DirectorDetailView(DetailView):
    model = Actor
    template_name = 'web_site/directors_detail.html'
    slug_field = 'name'
    context_object_name = 'director'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['director_movie_lst'] = Movie.objects.filter(actors=self.object)
        return context


class CatalogView(MoviesFilter, ListView):
    model = Movie
    template_name = 'web_site/catalog_movies.html'
    context_object_name = 'movies'

    def get_queryset(self):
        if self.request.GET:
            genres = Genre.objects.get(name=self.request.GET.get('genres'))
            queryset = Movie.objects.filter(genres=genres.id)
            return queryset
        else:
            queryset = Movie.objects.order_by('year')
            return queryset


class CatalogForGenre(MoviesFilter, ListView):
    model = Movie
    template_name = 'web_site/catalog_movies.html'
    context_object_name = 'movies'

    def get_queryset(self):
        if self.kwargs:
            genres = Genre.objects.get(name=self.kwargs['slug'])
            queryset = Movie.objects.filter(genres=genres.id)
            return queryset