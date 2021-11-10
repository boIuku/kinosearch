from django import template
from kinopoisk.models import *

register = template.Library()

@register.simple_tag()
def get_categories():
    return Category.objects.all()

@register.inclusion_tag('kinopoisk/list_categories.html')
def show_categories(sort=None, cat_selected=0):
    if not sort:
        cats = Category.objects.all()
    else:
        cats = Category.objects.order_by(sort)
    return {"cats": cats, "cat_selected": cat_selected}

@register.inclusion_tag('kinopoisk/list_menu.html')
def show_menu():
    menu = [{'title': 'About', 'url_name': 'about'},
            {'title': 'Add page', 'url_name': 'add_page'},
            {'title': 'Contact', 'url_name': 'contact'},
            ]
    return {"menu": menu}