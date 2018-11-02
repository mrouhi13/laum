from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import defaults
from django.views.generic import CreateView, DetailView, ListView, TemplateView
from django.views.generic.edit import FormView, FormMixin

from .forms import SearchForm, PageForm, ReportForm
from .models import Page, Report
from .utils.email import SendEmail

ERROR_404_TEMPLATE_NAME = 'errors/error_404.html'
ERROR_403_TEMPLATE_NAME = 'errors/error_403.html'
ERROR_400_TEMPLATE_NAME = 'errors/error_400.html'
ERROR_500_TEMPLATE_NAME = 'errors/error_500.html'


def page_not_found(request, exception, template_name=ERROR_404_TEMPLATE_NAME):
    return defaults.page_not_found(request, exception, template_name)


def server_error(request, template_name=ERROR_500_TEMPLATE_NAME):
    return defaults.server_error(request, template_name)


def bad_request(request, exception, template_name=ERROR_400_TEMPLATE_NAME):
    return defaults.bad_request(request, exception, template_name)


def permission_denied(request, exception, template_name=ERROR_403_TEMPLATE_NAME):
    return defaults.permission_denied(request, exception, template_name)


class AjaxableResponseMixin(FormMixin):
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
            page = self.object
            reporter = form.cleaned_data.get('reporter')
            author = form.cleaned_data.get('author')
            email_template = None
            to = None
            if reporter:
                email_template = 'emails/report.html'
                to = reporter
            elif author:
                email_template = 'emails/new_page.html'
                to = author

            if email_template:
                context = {'page': page}
                SendEmail(self.request, context, template_name=email_template).send([to])

            return JsonResponse({})
        else:
            return response

    def get_success_url(self):
        pass


class IndexView(TemplateView):
    template_name = 'web/pages/index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
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
        if not q:
            return redirect(reverse('web:index'))
        return super(PageListView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        q = self.request.GET.get('q')
        return Page.objects.filter(title__icontains=q, is_active=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PageListView, self).get_context_data(**kwargs)

        initial = {}
        q = self.request.GET.get('q')
        if q:
            initial = {'q': q}

        context['search_form'] = SearchForm(initial)
        context['page_form'] = PageForm
        return context


class PageDetailView(DetailView, FormView):
    model = Page
    form_class = ReportForm
    slug_field = 'pid'
    template_name = 'web/pages/page_detail.html'

    def get_initial(self):
        initial = {}
        pid = self.kwargs.get(self.slug_url_kwarg)
        if pid:
            initial = {'page': pid}
        return initial

    def get_object(self, queryset=None):
        pid = self.kwargs.get(self.slug_url_kwarg)
        return get_object_or_404(self.model, pid=pid, is_active=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PageDetailView, self).get_context_data(**kwargs)
        context['search_form'] = SearchForm
        context['page_form'] = PageForm
        return context


class PageCreateView(AjaxableResponseMixin, CreateView):
    model = Page
    form_class = PageForm


class ReportCreateView(AjaxableResponseMixin, CreateView):
    model = Report
    form_class = ReportForm
