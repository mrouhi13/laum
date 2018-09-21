from api.generics import CreateAPIView
from web.utils.email import NewPageEmail, ReportEmail
from .serializers import PageSerializer, ReportSerializer


class PageCreateView(CreateAPIView):
    """
    API endpoint that allows all users to add new page.
    """
    serializer_class = PageSerializer

    def perform_create(self, serializer):
        page = serializer.save()

        to = page.author

        if to is not None:
            page_title = page.title
            page_pid = page.pid

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
            page_title = serializer.validated_data['page'].title
            page_pid = serializer.validated_data['page'].pid

            context = {
                'page_title': page_title,
                'page_pid': page_pid,
            }

            ReportEmail(self.request, context).send([to])
