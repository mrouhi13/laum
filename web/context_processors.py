from django.contrib.sites.shortcuts import get_current_site

from .models import WebsiteSetting


def site_settings(request):
    settings = WebsiteSetting.objects.all()
    site = get_current_site(request)
    protocol = 'https' if request.is_secure() else 'http'
    base_url = f'{protocol}://{site.domain}'
    data = {'site_name': site.name, 'base_url': base_url}
    for item in settings:
        data.update({item.setting: item.content})

    return data
