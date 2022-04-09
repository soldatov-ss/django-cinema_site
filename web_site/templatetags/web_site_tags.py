from django import template
from django.core.exceptions import ObjectDoesNotExist

from web_site.models import Rating

register = template.Library()

@register.simple_tag()
def get_movie_rating(movie_id):
    try:
        movie = Rating.objects.get(movie=movie_id)
        return movie.avg_rating
    except ObjectDoesNotExist:
        return 0

@register.filter
def correct_num(num: int):
    return f'{num:,.0f}'.replace(',', ' ')