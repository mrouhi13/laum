from django.conf import settings
from django.http import JsonResponse
from templated_mail.mail import BaseEmailMessage


class AjaxableResponseMixin:
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.is_ajax():
            obj = self.object
            object_type = obj.__class__.__name__.lower()
            context = {object_type: obj}

            # Inform user with a success email
            email_template = f'emails/new_{object_type}.html'
            to = form.cleaned_data.get('reporter') or form.cleaned_data.get(
                'author')
            message = BaseEmailMessage(self.request, context, email_template)
            message.send([to])

            # Inform admins with an email
            message.template_name = \
                f'emails/new_{object_type}_notification.html'
            message.send([a[1] for a in settings.ADMINS])

            return JsonResponse({})
        else:
            return response

    def get_success_url(self):
        pass
