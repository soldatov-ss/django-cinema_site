from django.contrib import admin

from .models import Actor, Category, Movie, Genre, Reviews, Rating, RatingStar, MovieShots

admin.site.register(Category)
admin.site.register(Actor)
admin.site.register(Genre)
admin.site.register(Movie)
admin.site.register(MovieShots)
admin.site.register(RatingStar)
admin.site.register(Rating)
admin.site.register(Reviews)
