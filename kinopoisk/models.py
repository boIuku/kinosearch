from django.db import models
from django.urls import reverse

class Kinopoisk(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    content = models.TextField(blank=True)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d')
    time_added = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    watched = models.BooleanField(default=False)
    cat = models.ForeignKey('Category', on_delete=models.PROTECT)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    class Meta:
        verbose_name = 'Films'
        verbose_name_plural = 'Films'
        ordering = ['time_added']


class Category(models.Model):
    name = models.CharField(max_length=100,  db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        ordering = ['id']

