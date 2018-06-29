from django.shortcuts import render
from django.views import generic
from django.views.generic.edit import FormView

from .forms import SearchForm
from .models import Data


def index(request):
    search_form = SearchForm()
    random_data = Data.objects.get_random_data()

    return render(request, 'webapp/index.html', {'form': search_form, 'random_data': random_data})


class DataListView(generic.ListView, FormView):
    template_name = 'webapp/data_list.html'
    model = Data
    form_class = SearchForm
    context_object_name = 'data_list'
    paginate_by = 8

    def get_initial(self):
        if self.request.GET.get('q'):
            initial = {'q': self.request.GET.get('q')}
        else:
            initial = {}

        return initial

    def get_queryset(self):
        data_list = []

        if self.request.GET.get('q'):
            data_list = Data.objects.filter(title__icontains=self.request.GET['q'])

        return data_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DataListView, self).get_context_data(**kwargs)
        get_copy = self.request.GET.copy()
        parameters = get_copy.pop('page', True) and get_copy.urlencode()
        context['parameters'] = parameters
        context['count'] = len(self.get_queryset())

        return context


class DataDetailView(generic.DetailView, FormView):
    model = Data
    form_class = SearchForm
    template_name = 'webapp/data_detail.html'
