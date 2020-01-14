from django.utils import timezone
from django.core.management.base import BaseCommand, CommandError
from apps.dashboard.utils import collect_fred_data


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("Collecting data")
        collect_fred_data()