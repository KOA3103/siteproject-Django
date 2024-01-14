from django import template
from django.db.models import Count

# import dailyrentflat.views as views

from ..models import Cities, Announcement, TagPost

register = template.Library()


# @register.simple_tag(name='getcats')  # простой тег
# def get_categories():
#     return views.cats_db


@register.inclusion_tag('dailyrentflat/list_of_cities.html')
def show_cities(city_selected=0):
    cities = Cities.objects.annotate(total=Count("posts")).filter(total__gt=0)
    # city = Cities.objects.all()
    count = len(cities)
    # count = Cities.objects.count()
    return {"cities": cities, "city_selected": city_selected, "count": count}


@register.inclusion_tag('dailyrentflat/list_tags.html')
def show_all_tags():
    # return {"tags": TagPost.objects.all()}
    return {"tags": TagPost.objects.annotate(total=Count("tags")).filter(total__gt=0)}
