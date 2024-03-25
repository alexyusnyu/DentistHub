from django import template

register = template.Library()

WEEKDAYS = {
    0: 'Monday',
    1: 'Tuesday',
    2: 'Wednesday',
    3: 'Thursday',
    4: 'Friday',
    5: 'Saturday',
    6: 'Sunday',
}


@register.filter
def weekday_name(value):
    return WEEKDAYS[value]
