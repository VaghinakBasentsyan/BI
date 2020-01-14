import pandas as pd
from datetime import datetime

from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import ReportSerializer
from .models import Report
from .utils import collect_fred_data


class ReportViewSet(APIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

    def get(self, request, format=None):
        report = Report.objects.latest(field_name='id')
        df = pd.read_csv(report.file_path)
        data = {}
        data['recession_data'] = []
        date_rec = df[['date', 'recession']].values
        data['observations'] = date_rec
        elem = {}
        index = 0
        for arr in date_rec:

            if arr[1] and not elem:
                elem['start'] = datetime.strptime(arr[0], "%Y-%m-%d").timestamp()
                elem['start_date'] = arr[0]
            elif not arr[1] and elem:
                elem['end'] = datetime.strptime(date_rec[index-1][0], "%Y-%m-%d").timestamp()
                elem['end_date'] = date_rec[index-1][0]
                data['recession_data'].append(elem)
                elem = {}
            index += 1
        if elem:
            data['recession_data'].append(elem)
        return Response(data)
