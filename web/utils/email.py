from templated_mail.mail import BaseEmailMessage
from django.conf import settings


class SendNewPageEmail(BaseEmailMessage):
    template_name = 'email/new_page.html'

    def get_context_data(self):
        context = super(SendNewPageEmail, self).get_context_data()
        context['site_title'] = settings.SITE_TITLE
        context['contact_email'] = settings.CONTACT_EMAIL

        return context


class SendReportEmail(BaseEmailMessage):
    template_name = 'email/report.html'

    def get_context_data(self):
        context = super(SendReportEmail, self).get_context_data()
        context['site_title'] = settings.SITE_TITLE
        context['contact_email'] = settings.CONTACT_EMAIL

        return context
