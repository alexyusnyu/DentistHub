from django import template

register = template.Library()


@register.filter
def get_role(user):
    return user.role if user.is_authenticated else ''
