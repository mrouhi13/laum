from api.generics import CreateAPIView
from web.utils.email import SendNewPageEmail, SendReportEmail
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
            context = {'page': page}

            SendNewPageEmail(self.request, context).send([to])


class ReportCreateView(CreateAPIView):
    """
    API endpoint that allows all users to add report.
    """
    serializer_class = ReportSerializer

    def perform_create(self, serializer):
        super(ReportCreateView, self).perform_create(serializer)

        to = serializer.validated_data['reporter']

        if to is not None:
            context = {'page': serializer.validated_data['page']}

            SendReportEmail(self.request, context).send([to])
