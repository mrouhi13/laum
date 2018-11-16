from django.conf import settings
from templated_mail.mail import BaseEmailMessage


class SendEmail(BaseEmailMessage):
    def get_context_data(self):
        context = super(SendEmail, self).get_context_data()
        base_url = context['protocol'] + '://' + context['domain']
        static_url = base_url + settings.STATIC_URL

        context.update({
            'base_url': base_url,
            'static_url': static_url
        })
        return context
