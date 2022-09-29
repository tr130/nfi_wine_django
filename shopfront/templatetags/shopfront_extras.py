from django import template

register = template.Library()

@register.filter
def in_basket(id, basket):
    return basket.get(str(id), 0)

