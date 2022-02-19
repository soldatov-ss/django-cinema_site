from django.contrib import admin

from .models import Actor, Category, Movie, Genre, Reviews, Rating, RatingStar, MovieShots


class ReviewInline(admin.TabularInline):
    model = Reviews
    extra = 1
    readonly_fields = ('name', 'email', 'movie', 'parent')


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('slug',)}
    list_display = ('title', 'category', 'kinopoisk_rating', 'year', 'slug')
    list_filter = ('category', 'kinopoisk_rating', 'year', 'genres')
    search_fields = ('title', 'category__name')
    save_on_top = True
    inlines = [ReviewInline]
    fields = (
        ('title', 'tagline'), ('description'), ('poster'), ('year', 'world_premiere', 'country'),
        ('directors', 'actors', 'genres',),
        ('budget', 'fees_in_usa', 'fess_in_world',), ('likes', 'kinopoisk_rating',), ('category', 'running_time'),
        ('slug', 'draft')
    )


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ('name', 'age')
    list_display_links = ('name', 'age')
    search_fields = ('name',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('slug',)}
    list_display = ('name', 'slug',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug')
    search_fields = ('name',)


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('movie', 'name', 'parent')
    list_filter = ('parent', 'created_at', 'movie')
    readonly_fields = ('movie', 'name', 'email', 'parent')


@admin.register(MovieShots)
class MovieShorts(admin.ModelAdmin):
    list_display = ('title', 'movie')
    list_filter = ('title', 'movie')
    search_fields = ('movie', 'title')


admin.site.register(RatingStar)
admin.site.register(Rating)
