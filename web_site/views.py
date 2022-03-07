from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.list import MultipleObjectMixin

from web_site.forms import ReviewForm, UserRegisterForm, UserLoginForm
from web_site.models import Movie, Genre, Actor, Rating


class MoviesFilter:

    def get_genres(self):
        return Genre.objects.all()

    def get_years(self):
        return Movie.objects.values_list('year', flat=True).distinct()

    def get_countries(self):
        return Movie.objects.values_list('country', flat=True).distinct()

class MoviesView(MoviesFilter, View):
    model = Movie
    template_name = 'web_site/index.html'

    def get(self, request):
        carousel_movies = Movie.objects.order_by('kinopoisk_rating')[:12]
        premieres = Movie.objects.order_by('-world_premiere')[:8]
        new_movies = Movie.objects.order_by('-year')[:18]
        cartoon_id = Genre.objects.get(slug='multfilm')
        cartoons_list = Movie.objects.filter(genres=cartoon_id).order_by('-year')[:12]

        context = {'carousel_list': carousel_movies, 'premieres_list': premieres, 'cartoons_list': cartoons_list,
                   'new_movies_list': new_movies}
        return render(request, 'web_site/index.html', context)


class SingleMovieView(MoviesFilter, DetailView, CreateView):
    model = Movie
    template_name = 'web_site/movie_detail.html'
    context_object_name = 'movie'
    form_class = ReviewForm


class AddReview(View):

    def rating_for_movie(self, pk, rating_review):
        try:
            rating_obj = Rating.objects.get(movie_id=pk)
            ip = self.get_client_ip(self.request)
            count_r = int(rating_obj.count_reviews) + 1
            sum_r = int(rating_obj.sum_rating) + rating_review
            avg_r = round(sum_r / count_r, 1)

            rating_obj.ip = ip
            rating_obj.count_reviews = count_r
            rating_obj.sum_rating = sum_r
            rating_obj.avg_rating = avg_r
            rating_obj.save()

        except ObjectDoesNotExist:

            Rating.objects.create(ip=self.get_client_ip(self.request),
                                  count_reviews=1,
                                  sum_rating=rating_review,
                                  avg_rating=rating_review,
                                  movie_id=pk)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request, pk):
        form = ReviewForm(request.POST)
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if form.rating:
                form.rating = 2 * form.rating
                self.rating_for_movie(pk, int(form.rating))

            if request.POST.get('parent', None):
                form.parent_id = int(request.POST.get('parent'))
            form.movie = movie
            form.save()
        return redirect(movie.get_absolute_url())


class ActorDetailView(DetailView, MultipleObjectMixin):
    model = Actor
    template_name = 'web_site/actor_detail.html'
    context_object_name = 'actor'
    paginate_by = 12

    def get_context_data(self, **kwargs):
        object_list = Movie.objects.filter(actors=self.object)
        context = super().get_context_data(object_list=object_list, **kwargs)
        return context


class DirectorDetailView(DetailView, MultipleObjectMixin):
    model = Actor
    template_name = 'web_site/directors_detail.html'
    context_object_name = 'director'
    paginate_by = 12

    def get_context_data(self, **kwargs):
        object_list = Movie.objects.filter(actors=self.object)
        context = super().get_context_data(object_list=object_list, **kwargs)
        return context


class CatalogView(MoviesFilter, ListView):
    model = Movie
    template_name = 'web_site/catalog_movies.html'
    context_object_name = 'movies'
    paginate_by = 12

    def get_queryset(self):
        if self.kwargs.get('slug'):
            genres = Genre.objects.get(slug=self.kwargs['slug'])
            queryset = Movie.objects.filter(genres=genres.id)
        else:
            queryset = Movie.objects.order_by('year')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.kwargs.get('slug'):
            context['current_genre'] = self.kwargs['slug']
        return context


class FilterMoviesView(MoviesFilter, ListView):
    template_name = 'web_site/catalog_movies.html'
    paginate_by = 12
    context_object_name = 'movies'

    def result_queryset(self, genres, year, country):
        if year and genres and country:
            queryset = Movie.objects.filter(genres=genres, year=year, country=country)
        elif year is None and (genres and country):
            queryset = Movie.objects.filter(genres=genres, country=country).distinct()
        elif genres is None and (year and country):
            queryset = Movie.objects.filter(year=year, country=country).distinct()
        elif country is None and (year and genres):
            queryset = Movie.objects.filter(year=year, genres=genres).distinct()
        else:
            print(f'{year=}, {genres=}')
            queryset = Movie.objects.filter(Q(genres=genres) | Q(country=country) | Q(year=year)).distinct()

        return queryset

    def get_queryset(self):
        genres = None
        if self.request.GET.get('genre') not in ['Genre', 'Жанр']:
            genres = Genre.objects.get(name=self.request.GET.get('genre')).id

        country = None if self.request.GET.get('country') in ['Country', 'Страна'] else self.request.GET.get('country')
        year = None if self.request.GET.get('year') in ['Year', 'Год'] else self.request.GET.get('year')

        queryset = self.result_queryset(genres, year, country)
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["url_genre"] = f'genre={self.request.GET.get("genre")}&'
        context["country"] = f"year={self.request.GET.get('year')}&"
        context["year"] = f"country={self.request.GET.get('country')}&"
        return context


class UserRegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'web_site/register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'web_site/login.html'
    next_page = 'home'


def logout_user(request):
    logout(request)
    return redirect('login')


class Search(ListView):
    template_name = 'web_site/catalog_movies.html'
    context_object_name = 'movies'
    paginate_by = 1

    def get_queryset(self):
        return Movie.objects.filter(title__icontains=self.request.GET.get('q').title())

    def get_context_data(self, *args, **kwargs):
        context = super(Search, self).get_context_data(*args, **kwargs)
        context["q"] = f'q={self.request.GET.get("q")}&'
        return context


def about_us(request):
    return render(request, 'web_site/about.html')


def faq_page(request):
    return render(request, 'web_site/help_page.html')
