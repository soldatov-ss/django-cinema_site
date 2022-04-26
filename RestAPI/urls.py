from django.urls import path

from . import views

urlpatterns = [
    path('actors/', views.ActorsListView.as_view()),
    path('actor/<int:pk>', views.ActorListView.as_view()),
    path('genres/', views.GenresListView.as_view()),
    path('genre/<str:name>', views.GenreListView.as_view()),
    path('categories/', views.CategoriesListView.as_view()),
    path('movies/', views.MoviesListView.as_view()),
    path('movie/<int:kinopoisk_id>/', views.MovieListView.as_view()),
    path('review/', views.ReviewCreateView.as_view())
]