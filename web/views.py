from django.conf import settings
from django.contrib.postgres.aggregates import StringAgg
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import defaults
from django.views.generic import CreateView, DetailView, ListView, TemplateView
from templated_mail.mail import BaseEmailMessage

from .forms import SearchForm, PageForm, ReportForm
from .models import Page, Report

ERROR_400_TEMPLATE_NAME = 'errors/error_400.html'
ERROR_403_TEMPLATE_NAME = 'errors/error_403.html'
ERROR_404_TEMPLATE_NAME = 'errors/error_404.html'
ERROR_500_TEMPLATE_NAME = 'errors/error_500.html'


def bad_request(request, exception, template_name=ERROR_400_TEMPLATE_NAME):
    return defaults.bad_request(request, exception, template_name)


def permission_denied(request, exception, template_name=ERROR_403_TEMPLATE_NAME):
    return defaults.permission_denied(request, exception, template_name)


def page_not_found(request, exception, template_name=ERROR_404_TEMPLATE_NAME):
    return defaults.page_not_found(request, exception, template_name)


def server_error(request, template_name=ERROR_500_TEMPLATE_NAME):
    return defaults.server_error(request, template_name)


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

            # Send email notification to user
            email_template = f'emails/new_{object_type}.html'
            to = form.cleaned_data.get('reporter') or form.cleaned_data.get('author')
            message = BaseEmailMessage(self.request, context, email_template)
            message.send([to])

            # Send email notification to admins
            message.template_name = f'emails/new_{object_type}_notification.html'
            message.send([a[1] for a in settings.ADMINS])

            return JsonResponse({})
        else:
            return response

    def get_success_url(self):
        pass


class IndexView(TemplateView):
    template_name = 'web/pages/index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = SearchForm
        context['page_form'] = PageForm
        context['random_pages'] = Page.objects.get_random_pages()
        return context


class PageListView(ListView):
    model = Page
    template_name = 'web/pages/page_list.html'
    paginate_by = 8

    def get(self, request, *args, **kwargs):
        q = request.GET.get('q')
        if q:
            return super().get(request, *args, **kwargs)
        return redirect(reverse('web:index'))

    def get_queryset(self):
        q = self.request.GET.get('q')
        query = SearchQuery(q, search_type='plain')
        vector = SearchVector('title', weight='A') + \
                 SearchVector('subtitle', weight='B') + \
                 SearchVector(StringAgg('tags__name', delimiter=' '), weight='C') + \
                 SearchVector('content', 'event', 'image_caption', weight='D')
        rank = SearchRank(vector, query)
        return Page.objects.annotate(rank=rank).filter(
            is_active=True, rank__gte=0.01).order_by('-rank')

    def get_context_data(self, *, object_list=None, **kwargs):
        q = self.request.GET.get('q')
        context = super().get_context_data(**kwargs)
        context['search_form'] = SearchForm(initial={'q': q})
        context['page_form'] = PageForm
        return context


class PageDetailView(DetailView):
    model = Page
    slug_field = 'pid'
    template_name = 'web/pages/page_detail.html'

    def get_object(self, queryset=None):
        pid = self.kwargs.get(self.slug_url_kwarg)
        return get_object_or_404(self.model, pid=pid, is_active=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        pid = self.kwargs.get(self.slug_url_kwarg)
        context = super().get_context_data(**kwargs)
        context['search_form'] = SearchForm(initial={'q': None})
        context['report_form'] = ReportForm(initial={'page': pid})
        context['page_form'] = PageForm
        return context


class PageCreateView(AjaxableResponseMixin, CreateView):
    model = Page
    form_class = PageForm


class ReportCreateView(AjaxableResponseMixin, CreateView):
    model = Report
    form_class = ReportForm
