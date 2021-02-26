from django import template
from django.utils.timezone import now

register = template.Library()


@register.simple_tag(name='p_age')
def p_age(time):
    left = now() - time
    print(left)
    hour = now().hour - time.hour
    minute = now().minute - time.minute
    day = now().day - time.day
    month = now().month - time.month
    year = now().year - time.year
    if year == 1:
        if month < 0:
            month = month + 12
            return '{} months ago'.format(month)
        elif month == 0:
            if day < 0:
                return '11 months ago'
            elif day == 0:
                return '1 year ago'
        else:
            return '1 year ago'
    elif year > 1:
        return '{} years ago'.format(year)
    elif year == 0:
        if month == 0:
            if day == 1:
                return 'yesterday'
            elif day > 1:
                return '{} days ago'.format(day)
            elif day == 0:
                if hour < 0:
                    hour = 24 + hour
                    return '{} hours ago'.format(hour)
                elif hour == 0:
                    return '{} minutes ago'.format(minute)
                elif hour == 1:
                    if minute < 0:
                        minute = minute + 60
                        return '{} minutes ago'.format(minute)
                    return 'an hour ago'
                elif hour > 1:
                    if minute < 0:
                        hour = hour - 1
                        return '{} hours ago'.format(hour)
                    return '{} hours ago'.format(hour)

        elif month > 0:
            return '{} months ago'.format(month)
