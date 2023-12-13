from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponsePermanentRedirect
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.template.defaultfilters import slugify
from transliterate import translit

menu = ["О сайте", "Добавить статью", "Обратная связь", "Войти"]

data_db = [
    {'id': 1, 'title': 'Анджелина Джоли', 'content': 'Биография Анджелины Джоли', 'is_published': True},
    {'id': 2, 'title': 'Марго Робби', 'content': 'Биография Марго Робби', 'is_published': False},
    {'id': 3, 'title': 'Джулия Робертс', 'content': 'Биография Джулия Робертс', 'is_published': True},
]

def index(request):
    data = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': data_db,
        # 'url_slugify': slugify(translit("Главная страница", 'ru', reversed=True)),

    }
    return render(request, 'dailyrentflat/index.html', context=data)


def cities(request, cities_slug):
    return HttpResponse(f"<h1>Статьи по городам</h1><p >cities_slug: {cities_slug}</p>")


def about(request):
    data = {
        'title': 'About this site',
        'menu': menu,
    }
    return render(request, 'dailyrentflat/about.html', context=data)


def year_articles(request, year):
    if year > 2023:  # int
        raise Http404()  # Страница не найдена!
    if year < 2015:
        # return redirect('cats', 'category')  # redirect на именованный path "cats", "параметры" (slug = category).
        # другой способ redirect разделить операции вычисления URL и непосредственно перенаправление.
        # и передать этот маршрут и набора аргументов в функцию reverse()
        url_redirect = reverse('cats', args=('music',))
        # return redirect(url_redirect)
        # или в соответствующий класс:
        # HttpResponsePermanentRedirect для редиректа с кодом 301,
        # HttpResponseRedirect – для редиректа с кодом 302:
        return HttpResponsePermanentRedirect(url_redirect)
    return HttpResponse(f'<h1>year_archive: {year}</h1>')


def year_articles2(request, year, month):
    if year > '2023' or month > '12':  # str
        raise Http404()
    return HttpResponse(f'<h1>year_archive: {year}, month: {month}</h1>')


def categories_by_slug(request, cat_slug):
    if request.GET:
        print(request.GET)
    return HttpResponse(f"<h1>Статьи по категориям</h1><p >slug: {cat_slug}</p>")


def page_not_found(request, exception):
    return HttpResponseNotFound(f'<h1>Страница не найдена!</h1>')
