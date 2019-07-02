from django.contrib.sites.shortcuts import get_current_site

from django.conf import settings


def site_settings(request):
    site = get_current_site(request)
    protocol = 'https' if request.is_secure() else 'http'
    base_url = f'{protocol}://{site.domain}'
    static_url = base_url + getattr(settings, 'STATIC_URL', '')

    site_context = getattr(settings, 'SITE_CONTEXT', {})
    site_context.update({
        'SITE_NAME': site.name,
        'BASE_URL': base_url,
        'STATIC_URL': static_url
    })

    return site_context
