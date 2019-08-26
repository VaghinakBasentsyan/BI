import pandas as pd

from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import ReportSerializer
from .models import Report
from .utils import collect_data


class ReportViewSet(APIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

    def get(self, request, format=None):
        report = Report.objects.latest(field_name='id')
        df = pd.read_csv(report.file_path)
        df = df[['date', 'recession']]
        return Response(df.to_json(orient='records'))
        # collect_data()
        # return Response()
