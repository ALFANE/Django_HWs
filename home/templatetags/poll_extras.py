from django import template

register = template.Library()

@register.filter
def addition_cut(value):
    return value.replace(' ', '').lower()