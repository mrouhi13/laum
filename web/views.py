from django.shortcuts import render
from django.views import generic
from django.views.generic.edit import FormView

from .forms import SearchForm
from .models import Page


def index(request):
    search_form = SearchForm()
    random_page = Page.objects.get_random_page()

    return render(request, 'web/index.html', {'form': search_form, 'random_page': random_page})


class PageListView(generic.ListView, FormView):
    model = Page
    form_class = SearchForm
    template_name = 'web/page_list.html'
    context_object_name = 'page_list'
    paginate_by = 8

    def get_initial(self):
        if self.request.GET.get('q', None):
            initial = {'q': self.request.GET.get('q')}
        else:
            initial = {}

        return initial

    def get_queryset(self):
        page_list = []

        if self.request.GET.get('q', None):
            page_list = Page.objects.filter(title__icontains=self.request.GET['q'], is_active=True)

        return page_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PageListView, self).get_context_data(**kwargs)
        get_copy = self.request.GET.copy()
        parameters = get_copy.pop('page', True) and get_copy.urlencode()
        context['parameters'] = parameters
        context['count'] = len(self.get_queryset())

        return context


class PageDetailView(generic.DetailView, FormView):
    model = Page
    slug_field = 'pid'
    form_class = SearchForm
    template_name = 'web/page_detail.html'

    def get_queryset(self):
        pid = self.kwargs.get(self.slug_url_kwarg, None)
        page_detail = Page.objects.filter(pid=pid, is_active=True)

        return page_detail
