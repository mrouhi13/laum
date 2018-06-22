from django.views import generic
from django.shortcuts import render

from .models import Data


def index(request):
    return render(request, 'webapp/index.html')


class DataListView(generic.ListView):
    template_name = 'webapp/data_list.html'
    context_object_name = 'data_list'

    def get_queryset(self):
        data_list = []

        if 'q' in self.request.GET and not self.request.GET['q'] == '':
            data_list = Data.objects.filter(title__icontains=self.request.GET['q'])

        return data_list


class DataDetailView(generic.DetailView):
    model = Data
    template_name = 'webapp/data_detail.html'
