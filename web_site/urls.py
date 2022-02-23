from django.urls import path
from .views import *

urlpatterns = [
    path('', MoviesView.as_view(), name='home'),
    path('catalog/', CatalogView.as_view(), name='catalog'),
    path('catalog/<str:slug>/', CatalogForGenre.as_view(), name='catalog_list'),
    path('<slug:slug>/', SingleMovieView.as_view(), name='movie_detail'),
    path("review/<int:pk>/", AddReview.as_view(), name="add_review"),
    path("actor/<str:slug>/", ActorDetailView.as_view(), name="actor_detail"),
    path("producer/<str:slug>/", DirectorDetailView.as_view(), name="director_detail"),
]
