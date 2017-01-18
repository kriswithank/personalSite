from django import template
from django.http import HttpRequest, QueryDict
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



@register.simple_tag
def url_with_query(route, *args, **kwargs):
    """
    Returns the url to the roue with the appended query string.
    This WILL NOT WORK if the route needs kwargs.

    Args:
        route -> The route in typical django form.
        *args -> Other args required for the route.
        *kwargs -> Keyword args for each query parameter.
    """
    url = reverse(route, args=args)
    querystring = QueryDict(mutable=True)
    querystring.update(kwargs)
    return str(url) + str('?') + querystring.urlencode()
