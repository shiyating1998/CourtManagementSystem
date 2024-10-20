from django.core.management.base import BaseCommand
from datetime import time
from app.models import ItemCourt, ItemTime
from courtManagementSystem import settings, proj_settings


class Command(BaseCommand):
    help = 'Populate ItemTime for each court from 7am to 11pm in hourly intervals'

    def handle(self, *args, **kwargs):
        ItemTime.objects.all().delete()
        start_hour = proj_settings.start_hour
        end_hour = proj_settings.end_hour
        courts = ItemCourt.objects.all()
        item_times = []

        for court in courts:
            for hour in range(start_hour, end_hour):
                start_time = time(hour=hour)
                end_time = time(hour=hour + 1)
                item_times.append(ItemTime(item_court=court, start_time=start_time, end_time=end_time))

        ItemTime.objects.bulk_create(item_times)
        self.stdout.write(self.style.SUCCESS('Successfully populated ItemTime for each court from 7am to 11pm'))
