from webapp.generics import CreateAPIView
from .serializers import DataSerializer


class DataCreateView(CreateAPIView):
    """
    API endpoint that allows all users to add new page.
    """
    serializer_class = DataSerializer
