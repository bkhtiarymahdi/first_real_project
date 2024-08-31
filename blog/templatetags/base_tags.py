from django import template
from common.models import Category

register = template.Library()


@register.inclusion_tag('blog/category_navbar.html')
def category_nav():
    return {
        "categories": Category.objects.all()
    }
