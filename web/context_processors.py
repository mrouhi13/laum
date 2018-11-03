from django.conf import settings


def site_info(request):
    info = {
        'site_title': settings.SITE_TITLE,
        'site_slogan_1': settings.SITE_SLOGAN_1,
        'site_slogan_2': settings.SITE_SLOGAN_2,
        'site_url': settings.SITE_URL,
        'contact_email': settings.CONTACT_EMAIL,
        'language_code': settings.LANGUAGE_CODE,
        'google_analytics_id': settings.GOOGLE_ANALYTICS_ID
    }

    return info
