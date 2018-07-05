from templated_mail.mail import BaseEmailMessage
from django.conf import settings


class NewPageEmail(BaseEmailMessage):
    template_name = 'email/new_page.html'

    def get_context_data(self):
        context = super(NewPageEmail, self).get_context_data()
        context['site_title'] = settings.SITE_TITLE
        context['contact_email'] = settings.CONTACT_EMAIL

        return context


class ReportEmail(BaseEmailMessage):
    template_name = 'email/report.html'

    def get_context_data(self):
        context = super(ReportEmail, self).get_context_data()
        context['site_title'] = settings.SITE_TITLE
        context['contact_email'] = settings.CONTACT_EMAIL

        return context
