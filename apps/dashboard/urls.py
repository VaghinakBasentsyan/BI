from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from .views import (
    ReportViewSet
)

app_name = "Dashboard"

urlpatterns = [
    url(r"", ReportViewSet.as_view(), name="report"),
    url(r"^report/?", ReportViewSet.as_view(), name="report"),
]
