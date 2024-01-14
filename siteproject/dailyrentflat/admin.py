from django.contrib import admin
from .models import Announcement, Cities, TagPost


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_create', 'time_update', 'status_announcement', 'city')
    list_display_links = ('id', 'title', 'time_create', 'time_update', 'status_announcement', 'city')
# admin.site.register(Announcement, AnnouncementAdmin)  # в замен используется декоратор.

@admin.register(Cities)
class CitiesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'time_create', 'time_update',)
    list_display_links = ('id', 'name', 'slug', 'time_create', 'time_update',)


@admin.register(TagPost)
class TagPostAdmin(admin.ModelAdmin):
    list_display = ('id', 'tag', 'slug', 'time_create', 'time_update',)
    list_display_links = ('id', 'tag', 'slug', 'time_create', 'time_update',)
