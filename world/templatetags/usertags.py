from django import template

register = template.Library()


def profile_pic_url(user):
    return user.social_auth.extra()[0].extra_data['picture']['data']['url']

register.filter('profile_pic_url', profile_pic_url)