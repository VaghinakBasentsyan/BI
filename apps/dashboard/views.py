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
        print(Report.objects.all())
        report = Report.objects.latest(field_name='id')
a        df = pd.read_csv(report.file_path)

        columnsData = df.loc[:, ['date', 'recession']]
        # df = p

        # collect_data()
        return Response(df.to_json())
