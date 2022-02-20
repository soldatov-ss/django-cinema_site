from django.shortcuts import render, redirect

# Create your views here.
from django.views import View
from django.views.generic import ListView, DetailView, CreateView

from web_site.forms import ReviewForm
from web_site.models import Movie, Genre, Actor


class MoviesView(View):
    model = Movie
    template_name = 'web_site/index.html'

    def get(self, request):

        carousel_list = Movie.objects.filter(year=2022).order_by('likes')[:12]
        new_movies_list = Movie.objects.order_by('-world_premiere')[:6]
        cartoon_id = Genre.objects.get(name='мультфильм')
        cartoons_list = Movie.objects.filter(genres=cartoon_id).order_by('-year')[:12]

        context = {'carousel_list': carousel_list, 'new_movies_list': new_movies_list, 'cartoons_list': cartoons_list}
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
        context['actor_movie_lst'] = Movie.objects.filter(actors=self.object)[:12]
        return context

class DirectorDetailView(DetailView):
    model = Actor
    template_name = 'web_site/directors_detail.html'
    slug_field = 'name'
    context_object_name = 'director'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['director_movie_lst'] = Movie.objects.filter(actors=self.object)[:12]
        return context