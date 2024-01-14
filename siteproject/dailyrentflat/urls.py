from dailyrentflat import views, converters  # импортируем модуль views текущего пакета.
from django.urls import path, re_path, register_converter  # импортируем функцию path, которая и связывает URL c функциями представления.

register_converter(converters.FourDigitYearConverter, "yyyy")

# в списке urlpatterns вызываем функцию path,
# первым параметром указываем пустую строку, а вторым функцию index.
urlpatterns = [
    path('', views.index, name='home'),  # http://127.0.0.1:8000
    path('cities/<slug:cities_slug>/', views.cities, name='cities'),  # http://127.0.0.1:8000/cities/
    path('about/', views.about, name='about'),
    path('addpage/', views.addpage, name='add_page'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    path('post/<slug:post_slug>/', views.show_post, name='post'),
    path('tag/<slug:tag_slug>/', views.show_tag_postlist, name='tag'),

]