from dailyrentflat import views, converters  # импортируем модуль views текущего пакета.
from django.urls import path, re_path, register_converter  # импортируем функцию path, которая и связывает URL c функциями представления.

register_converter(converters.FourDigitYearConverter, "yyyy")

# в списке urlpatterns вызываем функцию path,
# первым параметром указываем пустую строку, а вторым функцию index.
urlpatterns = [
    path('', views.index, name='home'),  # http://127.0.0.1:8000
    path('cities/<slug:cities_slug>/', views.cities, name='cities'),  # http://127.0.0.1:8000/cities/
    path('about/', views.about, name='about'),

    path("cats/<slug:cat_slug>/", views.categories_by_slug, name='cats'),
    # re_path(r"^articles/(?P<year>[0-9]{4})/$", views.year_articles),
    re_path(r"^articles/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$", views.year_articles2, name='articles_2'),
    path("articles/<yyyy:year>/", views.year_articles, name='articles'),
]
