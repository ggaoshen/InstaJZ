import re

from django import template
from django.urls import NoReverseMatch, reverse
from Insta.models import Like


register = template.Library()

@register.simple_tag
def is_following(current_user, background_user): # current_user: you, or currently logged in user; background_user: whoever you're checking profile details for
    return background_user.get_followers().filter(creator=current_user).exists() # check if I'm currently following this person

@register.simple_tag
def has_user_liked_post(post, user): 
    try:
        like = Like.objects.get(post=post, user=user) # return all objects from Like class on condition
        return "fa-heart"
    except:
        return "fa-heart-o"

@register.simple_tag(takes_context=True)
def active(context, pattern_or_urlname):
    try:
        pattern = reverse(pattern_or_urlname)
    except NoReverseMatch:
        pattern = pattern_or_urlname
    path = context['request'].path
    if re.search(pattern, path):
        return 'active'
    return ''