from django.contrib import admin
from .models import *

class KinopoiskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_added', 'watched')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('watched',)
    list_filter = ('watched', 'time_added')
    prepopulated_fields = {"slug": ("title",)}

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Kinopoisk, KinopoiskAdmin)
admin.site.register(Category, CategoryAdmin)
