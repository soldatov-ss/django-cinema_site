from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions
from rest_framework import generics

from web_site.models import Actor, Movie, Genre, Category
from .serializers import ActorsListSerializer, MoviesListSerializer, MovieListSerializer, ReviewCreateSerializer, \
    ActorListSerializer, GenresListSerializer, GenreListSerializer, CategoriesListSerializer
from .service import MovieFilter


class ReviewCreateView(generics.CreateAPIView):
    serializer_class = ReviewCreateSerializer
    permission_classes = [permissions.IsAdminUser]


class ActorsListView(generics.ListAPIView):
    queryset = Actor.objects.all()
    serializer_class = ActorsListSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'film_actor__title']


class ActorListView(generics.RetrieveUpdateAPIView):
    queryset = Actor.objects.all()
    serializer_class = ActorListSerializer
    permission_classes = [permissions.IsAdminUser]


class GenresListView(generics.ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenresListSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class GenreListView(generics.RetrieveUpdateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreListSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        try:
            obj = queryset.get(name=self.kwargs['name'].title())
            self.check_object_permissions(self.request, obj)
            return obj
        except Genre.DoesNotExist:
            pass


class MoviesListView(generics.ListAPIView):
    serializer_class = MoviesListSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_class = MovieFilter
    search_fields = ['title']
    queryset = Movie.objects.all()


class MovieListView(generics.RetrieveUpdateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieListSerializer
    permission_classes = [permissions.IsAdminUser, permissions.IsAuthenticatedOrReadOnly]

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        try:
            obj = queryset.get(kinopoisk_id=self.kwargs['kinopoisk_id'])
            self.check_object_permissions(self.request, obj)
            return obj
        except Movie.DoesNotExist:
            pass


class CategoriesListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoriesListSerializer
