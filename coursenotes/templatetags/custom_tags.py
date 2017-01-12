from django import template
from django.http import HttpRequest
from django.urls import reverse



register = template.Library()



@register.simple_tag
def route_active(request, route, *args):
    """
    Returns 'active' if the route is active or '' if it is not. Ment for for
    determining the class attributes of navigation bar items.

    Args:
        request -> The page request.
        route -> The route to test activity for.
        *args -> Other args required for the route. So that call is similar to url
                 template tag.
    """
    if request.path == reverse(route, args=args):
        return 'active'
    else:
        return ''
