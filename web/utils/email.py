from django.conf import settings
from templated_mail.mail import BaseEmailMessage


class SendEmail(BaseEmailMessage):
    def get_context_data(self):
        context = super(SendEmail, self).get_context_data()
        context['site_title'] = settings.SITE_TITLE
        context['contact_email'] = settings.CONTACT_EMAIL

        return context
