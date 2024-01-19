from datetime import datetime

from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from transliterate import translit


class Cities(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Город")
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name="Слаг")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время добавления")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

    def get_absolute_url(self):
        return reverse('cities', kwargs={'cities_slug': self.slug})

    def __str__(self):
        return self.name


class TagPost(models.Model):
    tag = models.CharField(max_length=100, db_index=True, verbose_name="Оснащение")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="Слаг")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время добавления")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")

    class Meta:
        verbose_name = 'Дополнительная информация'
        verbose_name_plural = 'Дополнительная информация'

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})

    def __str__(self):
        return self.tag


class PublishedModel(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status_announcement=Announcement.Status.PUBLISHED)




class Announcement(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'Draft', 'Черновик'
        MODERATION = 'Moderation', 'На модерации'
        PUBLISHED = 'Published', 'Опубликовано'

    title = models.CharField(max_length=200, verbose_name="Заголовок", validators=[
        MinLengthValidator(5, message="Минимум 5 символов!"),
        MaxLengthValidator(150, message="Максимум 150 символов!")
    ])
    slug = models.SlugField(max_length=255, db_index=True, unique=True)
    content = models.TextField(max_length=5000, verbose_name="Описание")

    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    status_announcement = models.CharField(max_length=10, choices=Status.choices, default=Status.DRAFT, verbose_name="Статус")
    city = models.ForeignKey(Cities, on_delete=models.PROTECT, related_name='posts', verbose_name="Город")
    location = models.CharField(max_length=100, blank=True, verbose_name="Местонахождение")
    address = models.CharField(max_length=100, blank=True, verbose_name="Адрес объекта: Улица, Дом")
    price = models.IntegerField(verbose_name="Цена, в рублях")
    security_deposit = models.IntegerField(blank=True, verbose_name="Залоговая сумма")

    tags = models.ManyToManyField(TagPost, blank=True, related_name='tags', verbose_name='Дополнительная информация')

    objects = models.Manager()  # The default manager.
    published = PublishedModel()  # The specific manager.

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Объявлениe'
        verbose_name_plural = 'Объявления'
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create'])
        ]

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    def save(self, *args, **kwargs):  # Автозаполнение слага 1-ый вариант.
        self.slug = slugify(translit(str(self.title[:30])+"_"+str(datetime.now()), 'ru', reversed=True))
        super().save(*args, **kwargs)


