# Create your models here.
from datetime import date

from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField("Категория", max_length=150)
    description = models.TextField("Описание", blank=True)
    slug = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Actor(models.Model):
    name = models.CharField("Имя", max_length=100)
    age = models.PositiveSmallIntegerField("Возраст", default=0)
    description = models.TextField("Описание", blank=True)
    image = models.ImageField("Изображение", upload_to="actors/", blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('actor_detail', kwargs={"slug": self.name})

    class Meta:
        verbose_name = "Актеры и режиссеры"
        verbose_name_plural = "Актеры и режиссеры"


class Genre(models.Model):
    name = models.CharField("Имя", max_length=100)
    description = models.TextField("Описание", blank=True)
    slug = models.SlugField(max_length=160, unique=True)

    def get_absolute_url(self):
        return reverse('catalog_list', kwargs={'slug': self.name})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class Movie(models.Model):
    title = models.CharField("Название", max_length=100)
    tagline = models.CharField("Слоган", max_length=100, blank=True, default='')
    description = models.TextField("Описание")
    poster = models.ImageField("Постер", upload_to="movies/")
    year = models.PositiveSmallIntegerField("Дата выхода", default=2019)
    country = models.CharField("Страна", max_length=30)
    directors = models.ManyToManyField(Actor, verbose_name="режиссер", related_name="film_director")
    actors = models.ManyToManyField(Actor, verbose_name="актеры", related_name="film_actor")
    genres = models.ManyToManyField(Genre, verbose_name="жанры")
    world_premiere = models.DateField("Премьера в мире", default=date.today)
    budget = models.PositiveIntegerField("Бюджет", default=0, help_text="сумма в долларах")
    kinopoisk_rating = models.FloatField(verbose_name='Рейтинг Кинопоиск', default=0)
    running_time = models.FloatField('Продолжительность', default=0)
    fees_in_usa = models.PositiveIntegerField("Сборы в США", default=0, help_text="сумма в долларах")
    fess_in_world = models.PositiveIntegerField("Сборы в мире", default=0, help_text="сумма в долларах")
    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.SET_NULL, null=True)
    slug = models.SlugField(max_length=130, unique=True)
    draft = models.BooleanField("Черновик", default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("movie_detail", kwargs={"slug": self.slug})

    def get_review(self):
        return self.reviews_set.filter(parent__isnull=True)

    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"


class MovieShots(models.Model):
    title = models.CharField("Заголовок", max_length=100)
    description = models.TextField("Описание", blank=True)
    image = models.ImageField("Изображение", upload_to="movie_shots/")
    movie = models.ForeignKey(Movie, verbose_name="Фильм", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Кадр из фильма"
        verbose_name_plural = "Кадры из фильма"


class Rating(models.Model):
    ip = models.CharField("IP адрес", max_length=15)
    count_reviews = models.IntegerField('Кол-во оценок', default=0)
    sum_rating = models.BigIntegerField('Кол-во звезд', default=0)
    avg_rating = models.FloatField('Средняя оценка', default=0)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name="фильм", related_name="ratings")

    def __str__(self):
        return f"{self.avg_rating} - {self.movie}"

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"


class Reviews(models.Model):
    email = models.EmailField()
    name = models.CharField("Имя", max_length=100)
    text = models.TextField("Сообщение", max_length=5000)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    rating = models.IntegerField('Оценка пользователя', blank=True)
    parent = models.ForeignKey('self', verbose_name="Родитель", on_delete=models.SET_NULL, blank=True, null=True)
    movie = models.ForeignKey(Movie, verbose_name="фильм", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.movie} -{self.name}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
