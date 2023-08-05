from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.middleware.csrf import get_token


@ensure_csrf_cookie
def csrf(request):
    # As django need view to have request option but we don't need it, we need to exclude pylint
    # unused-argument for this method
    # pylint: disable=W0613
    """
    This page is only a empty page to force CSRF token to be send to browser. In case of REST API,
    CSRF can be painful to retrieve as it is not sent on every pages. This page force Django to
    resend a new CSRF Token.

    As django view are generic function with "request" as parameter and we don't use it, we must
    tell to pylint to *not* check W0613 (unused-argument) from this function.

    :param request: full HTTP request from user
    """
    return JsonResponse({'csrf': get_token(request)})
