from django import template

register = template.Library()

@register.filter
def in_basket(id, session):
    if 'shopping_cart' in session:
        return session['shopping_cart'].get(str(id), 0)
    else:
        return 0

