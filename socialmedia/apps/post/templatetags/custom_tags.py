from django import template
from django.utils.timezone import now

from apps.post.models import Like, Comment

register = template.Library()


# a simple tag for showing post's age
@register.simple_tag(name='p_age')
def p_age(time):
    """
       divide differences between post publishing hour, minute, day, month, year
       and now.
    """
    hour = now().hour - time.hour
    minute = now().minute - time.minute
    day = now().day - time.day
    month = now().month - time.month
    year = now().year - time.year
    """
        Check different conditions for showing the right post age.
        It will return a message which shows post age.
    """
    if year == 1:
        if month < 0:
            month = month + 12
            return '{} months ago'.format(month)
        elif month == 0:
            if day < 0:
                return '11 months ago'
            else:
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


@register.simple_tag(name='count_like')
def count_like(post_id):
    likes = Like.objects.filter(post=post_id)
    return len(likes)


@register.inclusion_tag('post/content.html')
def comment_post(post_id):
    my_comment = Comment.objects.filter(post=post_id)
    return {'my_comment': my_comment}
