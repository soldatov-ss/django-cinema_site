from django.urls import path
from .views import *

urlpatterns = [
    path('', CarouselMoviesView.as_view(), name='carousel_home')

]
