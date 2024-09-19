from django.core.management.base import BaseCommand
from datetime import time
from app.models import ItemCourt, ItemTime

#TODO, create starting script for easy config...

class Command(BaseCommand):
    help = 'Populate ItemTime for each court from 9am to 11pm in hourly intervals'

    def handle(self, *args, **kwargs):
        start_hour = 9
        end_hour = 23
        courts = ItemCourt.objects.all()
        item_times = []

        for court in courts:
            for hour in range(start_hour, end_hour):
                start_time = time(hour=hour)
                end_time = time(hour=hour + 1)
                item_times.append(ItemTime(item_court=court, start_time=start_time, end_time=end_time))

        ItemTime.objects.bulk_create(item_times)
        self.stdout.write(self.style.SUCCESS('Successfully populated ItemTime for each court from 9am to 11pm'))
