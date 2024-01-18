from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponsePermanentRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.template.defaultfilters import slugify
from transliterate import translit

from .forms import AddPostForm
from .models import Announcement, Cities, TagPost

menu = [{'title': "Главная страница", 'url_name': 'home'},
        {'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'},
        ]


def index(request):
    # posts = Announcement.published.all()
    data = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': Announcement.published.all().select_related('city'),
        'url_slugify': slugify(translit("Главная страница", 'ru', reversed=True)),
        'city_selected': 0,
    }
    return render(request, 'dailyrentflat/index.html', context=data)


def show_post(request, post_slug):
    post = get_object_or_404(Announcement, slug=post_slug)
    data = {
        'title': post.title,
        'menu': menu,
        'post': post,
        # 'city_selected': 1,
    }
    return render(request, 'dailyrentflat/post.html', context=data)


def cities(request, cities_slug):
    city = get_object_or_404(Cities, slug=cities_slug)
    posts = Announcement.published.filter(city=city.pk).select_related('city')
    data = {
        'title': f'{city.name}',
        'menu': menu,
        'posts': posts,
        'city_selected': city.pk,
    }
    return render(request, 'dailyrentflat/index.html', context=data)


def about(request):
    data = {
        'title': 'About this site',
        'menu': menu,
    }
    return render(request, 'dailyrentflat/about.html', context=data)


def addpage(request):  # добавление данных в бд
    if request.method == 'POST':  # если запрос POST, сохраняем данные
        form = AddPostForm(request.POST)  # Объект класса формы в HTML.
        if form.is_valid():
            cd = form.cleaned_data  # Отчищенные данные от формы в type Dic.
            try:
                # Объект класса модели с полями в которые будем сохранять введенные данные.
                announcement = Announcement(
                    title=cd['title'],
                    content=cd['content'],
                    city=cd['city'],
                    status_announcement=cd['status_announcement'],
                )
                announcement.save()
                #  Для отношения Many to Many получаем список (list) id выбранные tags.
                tag_ids = request.POST.getlist("tags")
                #  Получаем список (list) QuerySet выбранных tag_id.
                tags = TagPost.objects.filter(id__in=tag_ids)
                announcement.tags.set(tags)  # сохраняем данные
                return redirect('home')
            except:
                form.add_error(None, 'Ошибка добавления поста')

    else:
        form = AddPostForm()

    data = {
        'title': 'Подать объявление бесплатно',
        'menu': menu,
        'form': form,
    }

    return render(request, 'dailyrentflat/addpage.html', data)


def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Авторизация")


def page_not_found(request, exception):
    return HttpResponseNotFound(f'<h1>Страница не найдена!</h1>')


def show_tag_postlist(request, tag_slug):
    tag_by_slug = get_object_or_404(TagPost, slug=tag_slug)
    posts = tag_by_slug.tags.filter(status_announcement=Announcement.Status.PUBLISHED).select_related('city')
    data = {
        'title': f'Тег: {tag_by_slug.tag}',
        'menu': menu,
        'posts': posts,
        'cat_selected': None,
    }

    return render(request, 'dailyrentflat/index.html', context=data)
