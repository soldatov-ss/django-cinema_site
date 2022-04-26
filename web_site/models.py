# Create your models here.
from datetime import date

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Sum
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
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self, page=1):
        return reverse('actor_detail', kwargs={"slug": self.slug, 'page': page})

    class Meta:
        verbose_name = "Актеры и режиссеры"
        verbose_name_plural = "Актеры и режиссеры"


class Genre(models.Model):
    name = models.CharField("Имя", max_length=100)
    description = models.TextField("Описание", blank=True)
    slug = models.SlugField(max_length=160, unique=True)

    def get_absolute_url(self, page=1):
        return reverse('genre_catalog', kwargs={'slug': self.slug, 'page': page})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class Movie(models.Model):
    title = models.CharField("Название", max_length=100)
    tagline = models.CharField("Слоган", max_length=100, blank=True, default='')
    kinopoisk_id = models.IntegerField('Кинопоиск ID', default=0, unique=True)
    description = models.TextField("Описание")
    poster = models.ImageField("Постер", upload_to="movies/")
    year = models.PositiveSmallIntegerField("Дата выхода", default=2019)
    country = models.CharField("Страна", max_length=30)
    directors = models.ManyToManyField(Actor, verbose_name="режиссер", related_name="film_director")
    actors = models.ManyToManyField(Actor, verbose_name="актеры", related_name="film_actor")
    genres = models.ManyToManyField(Genre, verbose_name="жанры")
    world_premiere = models.DateField("Премьера в мире", default=date.today)
    budget = models.PositiveIntegerField("Бюджет", default=0, help_text="сумма в долларах", blank=True)
    kinopoisk_rating = models.FloatField(verbose_name='Рейтинг Кинопоиск', default=0)
    running_time = models.FloatField('Продолжительность', default=0)
    fess_in_world = models.PositiveIntegerField("Сборы в мире", default=0, help_text="сумма в долларах", blank=True)
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
    ip = models.CharField("IP адрес", max_length=15, default=0)
    name = models.CharField("Имя", max_length=100)
    text = models.TextField("Сообщение", max_length=5000)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    rating = models.IntegerField('Оценка пользователя', blank=True, default=0)
    parent = models.ForeignKey('self', verbose_name="Родитель", on_delete=models.SET_NULL, blank=True, null=True, related_name='children')
    movie = models.ForeignKey(Movie, verbose_name="фильм", on_delete=models.CASCADE, related_name='reviews')
    votes = GenericRelation('LikeDislike', related_query_name='reviews')

    def __str__(self):
        return f"{self.movie} -{self.name}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"


class LikeDislikeManager(models.Manager):
    use_for_related_fields = True

    def likes(self):
        # Забираем queryset с записями больше 0
        return self.get_queryset().filter(vote__gt=0)

    def dislikes(self):
        # Забираем queryset с записями меньше 0
        return self.get_queryset().filter(vote__lt=0)

    def sum_rating(self):
        # Забираем суммарный рейтинг
        return self.get_queryset().aggregate(Sum('vote')).get('vote__sum') or 0


class LikeDislike(models.Model):
    LIKE = 1
    DISLIKE = -1

    VOTES = (
        (DISLIKE, 'Не нравится'),
        (LIKE, 'Нравится')
    )

    vote = models.SmallIntegerField(verbose_name=("Голос"), choices=VOTES)
    user_ip = models.CharField("IP адрес", max_length=15, default=0)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    objects = LikeDislikeManager()

    class Meta:
        verbose_name = "Лайк & Дизлайк"
        verbose_name_plural = "Лайки & Дизлайки"