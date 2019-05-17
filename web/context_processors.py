from django.contrib.sites.shortcuts import get_current_site

from .models import Setting


def site_settings(request):
    settings = Setting.objects.all()
    site = get_current_site(request)
    protocol = 'https' if request.is_secure() else 'http'
    base_url = f'{protocol}://{site.domain}'
    data = {'site_name': site.name, 'base_url': base_url}
    for item in settings:
        data.update({item.type: item.content})

    return data
