from django.contrib import admin, messages
from .models import Announcement, Cities, TagPost


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ("title",)}  # Автозаполнение слага 2-ой вариант, работает только в админ панели.
    # readonly_fields = ['slug']  # Поля только для чтения.
    list_display = ('id', 'title', 'slug', 'time_create', 'time_update', 'status_announcement', 'city', 'location', 'address', 'price', 'security_deposit', 'brief_info')
    list_display_links = ('id', 'title', 'time_create', 'time_update')
    ordering = ['-time_update', '-time_create', 'title']  # Сортировка
    list_editable = ('status_announcement',)  # Должен быть именно кортеж ('status_announcement', 'city',).
    list_per_page = 15  # Пагинация с указанием максимального числа записей на странице.
    actions = ['set_published', 'set_draft', 'set_moderation']  # Определение пользовательских действий в админ-панели.
    search_fields = ['title', 'city__name', 'content']  # Поиск по полю title, по городам и по описанию.
    list_filter = ['city__name', 'status_announcement']  # Отображение панели фильтрации по заданным критериям.
    filter_horizontal = ['tags']  # Настраивать виджет для типа связи многие ко многим, или filter_vertical = ['tags']
    # radio_fields = {"status_announcement": admin.HORIZONTAL}

    # admin.site.register(Announcement, AnnouncementAdmin)  # В замен используется декоратор @admin.register(Announcement).
    @admin.display(description="В объявлении", ordering='content')  # Декоратор определяет название поля.
    def brief_info(self, obj):  # Определяет собственное пользовательское поле.
        return f'{len(obj.content)} cимволов'

    @admin.action(description="Опубликовать выбранные Объявления")
    def set_published(self, request, queryset):
        count = queryset.update(status_announcement=Announcement.Status.PUBLISHED)
        self.message_user(request, f"Опубликовано {count} объявление(ий).")

    @admin.action(description='Поместить в "Черновик"')
    def set_draft(self, request, queryset):
        count = queryset.update(status_announcement=Announcement.Status.DRAFT)
        self.message_user(request, f'{count} объявление(ий) переведен(ы) в "Черновик"', messages.WARNING)

    @admin.action(description='Поместить "На модерацию"')
    def set_moderation(self, request, queryset):
        count = queryset.update(status_announcement=Announcement.Status.MODERATION)
        self.message_user(request, f'{count} объявление(ий) переведен(ы) "На модерацию"', messages.WARNING)


@admin.register(Cities)
class CitiesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ("name",)}  # Автозаполнение слага 2-й вариант.
    list_display = ('id', 'name', 'slug', 'time_create', 'time_update',)
    list_display_links = ('id', 'name', 'slug', 'time_create', 'time_update',)


@admin.register(TagPost)
class TagPostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ("tag",)}  # Автозаполнение слага 2-ой вариант.
    list_display = ('id', 'tag', 'slug', 'time_create', 'time_update',)
    list_display_links = ('id', 'tag', 'slug', 'time_create', 'time_update',)
