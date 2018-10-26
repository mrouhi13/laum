from django.http import JsonResponse
from django.shortcuts import get_object_or_404, get_list_or_404, redirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView, TemplateView
from django.views.generic.edit import FormView, FormMixin

from .forms import SearchForm, PageForm, ReportForm
from .models import Page, Report
from .utils.email import SendEmail


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
            print(self.object)
            page = self.object
            reporter = form.cleaned_data.get('reporter')
            author = form.cleaned_data.get('author')
            email_template = None
            to = None
            if reporter:
                email_template = 'email/report.html'
                to = reporter
            elif author:
                email_template = 'email/new_page.html'
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
    context_object_name = 'page_list'
    paginate_by = 8

    def get(self, request, *args, **kwargs):
        q = request.GET.get('q')
        if not q:
            return redirect(reverse('web:index'))
        return super(PageListView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        q = self.request.GET.get('q')
        page_list = get_list_or_404(self.model, title__icontains=q, is_active=True)
        return page_list

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
        page_detail = get_object_or_404(self.model, pid=pid, is_active=True)
        return page_detail

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
