#  Copyright (c) 2021.
#  Julio Cezar Riffel<julioriffel@gmail.com>

from urllib.parse import urlencode

from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.simple_tag
def urlparams(*_, **kwargs):
    safe_args = {k: v for k, v in kwargs.items() if v is not None}
    if safe_args:
        return '?{}'.format(urlencode(safe_args))
    return ''


@register.simple_tag
def relative_url(value, field_name, urlencode=None):
    url = '?{}={}'.format(field_name, value)
    if urlencode:
        querystring = urlencode.split('&')
        filtered_querystring = filter(lambda p: p.split('=')[0] != field_name, querystring)
        encoded_querystring = '&'.join(filtered_querystring)
        url = '{}&{}'.format(url, encoded_querystring)
    return url


@register.filter(name="atras_space")
@stringfilter
def atras_space(value):
    return value.replace('atrás', ' atrás').replace('  ', ' ')
