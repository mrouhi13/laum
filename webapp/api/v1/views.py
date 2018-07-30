from webapp.generics import CreateAPIView
from webapp.utils.email import NewPageEmail, ReportEmail
from .serializers import DataSerializer, ReportSerializer


class DataCreateView(CreateAPIView):
    """
    API endpoint that allows all users to add new page.
    """
    serializer_class = DataSerializer

    def perform_create(self, serializer):
        data = serializer.save()

        to = data.author

        if to is not None:
            page_title = data.title
            page_pid = data.pid

            context = {
                'page_title': page_title,
                'page_pid': page_pid,
            }

            NewPageEmail(self.request, context).send([to])


class ReportCreateView(CreateAPIView):
    """
    API endpoint that allows all users to add report.
    """
    serializer_class = ReportSerializer

    def perform_create(self, serializer):
        super(ReportCreateView, self).perform_create(serializer)

        to = serializer.validated_data['reporter']

        if to is not None:
            page_title = serializer.validated_data['data'].title
            page_pid = serializer.validated_data['data'].pid

            context = {
                'page_title': page_title,
                'page_pid': page_pid,
            }

            ReportEmail(self.request, context).send([to])
