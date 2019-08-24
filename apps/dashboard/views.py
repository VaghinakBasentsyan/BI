from rest_framework import viewsets


from .serializers import ReportSerializer
from .models import Report


class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
