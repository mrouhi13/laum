from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class WebConfig(AppConfig):
    name = 'web'
    verbose_name = _('Laum Project')
