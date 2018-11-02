from django.conf import settings


def site_info(request):
    info = {
        'site_title': settings.SITE_TITLE,
        'site_slogan': settings.SITE_SLOGAN,
        'site_url': settings.SITE_URL,
        'contact_email': settings.CONTACT_EMAIL,
        'language_code': settings.LANGUAGE_CODE
    }

    return info
