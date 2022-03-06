from django.urls import path
from .views import *

urlpatterns = [
    path('', MoviesView.as_view(), name='home'),
    path('catalog/<int:page>/', CatalogView.as_view(), name='catalog'),
    path('filter/', FilterMoviesView.as_view(), name='filter'),
    path('search/', Search.as_view(), name='search'),
    path('about/', about_us, name='about'),
    path('help/', faq_page, name='help_page'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('catalog/<slug:slug>/<int:page>/', CatalogView.as_view(), name='genre_catalog'),
    path('/<slug:slug>/', SingleMovieView.as_view(), name='movie_detail'),
    path("review/<int:pk>/", AddReview.as_view(), name="add_review"),
    path("actor/<str:slug>/", ActorDetailView.as_view(), name="actor_detail"),
    path("producer/<str:slug>/<int:page>/", DirectorDetailView.as_view(), name="director_detail"),
]
