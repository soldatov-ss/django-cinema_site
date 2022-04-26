from django_filters import rest_framework as filters

from web_site.models import Movie, Actor


class CharFieldInFilter(filters.BaseInFilter, filters.CharFilter):
    pass

class MovieFilter(filters.FilterSet):
    genres = CharFieldInFilter(field_name='genres__name', lookup_expr='in')
    year = filters.RangeFilter()

    class Meta:
        model = Movie
        fields = ['genres', 'year']
