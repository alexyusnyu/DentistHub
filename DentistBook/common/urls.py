from django.urls import path
from DentistBook.common.views import home_page, map_page, search_view, about_page

urlpatterns = [
    path('', home_page, name='home-page'),
    path('map-all-dentistsoffices', map_page, name='map-page'),
    path('search/', search_view, name='search-view'),
    path('about/', about_page, name='about-page')
]