from .models import Setting


def site_info(request):
    settings = Setting.objects.all()
    info = {}
    for item in settings:
        info.update({item.type: item.content})

    return info
