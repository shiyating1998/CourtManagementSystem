from django.core.management.base import BaseCommand
from app.models import ItemCourt, ItemTime, ItemOrder, User
from decimal import Decimal
from datetime import datetime, time, date, timedelta

class Command(BaseCommand):
    help = 'Populate ItemOrder with predefined prices based on time slots'

    def handle(self, *args, **kwargs):
        # DANGER the below code removes all entries from ItemOrder
        ItemOrder.objects.all().delete()

        # Define time slots and prices
        weekday_prices = [
            (time(15, 0), time(18, 0), Decimal('26.75')),
            (time(18, 0), time(22, 0), Decimal('30.00')),
            (time(22, 0), time(23, 0), Decimal('28.00')),
        ]

        weekend_prices = [
            (time(7, 0), time(9, 0), Decimal('28.00')),
            (time(9, 0), time(23, 0), Decimal('30.00')),
        ]

        holiday_price = Decimal('30.25')

        # Define date range for the next month
        today = date.today()
        end_date = today + timedelta(days=365)
        current_date = today

        item_courts = ItemCourt.objects.all()
        users = list(User.objects.all())  # Assuming users are already created

        item_orders = []

        while current_date <= end_date:
            if self.is_holiday(current_date):  # Check if current date is a holiday
                item_orders.extend(self.create_item_orders(item_courts, current_date, time(0, 0), time(23, 0), holiday_price))
            elif current_date.weekday() < 5:  # Monday to Friday
                for start, end, price in weekday_prices:
                    item_orders.extend(self.create_item_orders(item_courts, current_date, start, end, price))
            else:  # Saturday and Sunday
                for start, end, price in weekend_prices:
                    item_orders.extend(self.create_item_orders(item_courts, current_date, start, end, price))

            current_date += timedelta(days=1)

        # Bulk create item orders
        ItemOrder.objects.bulk_create(item_orders)
        self.stdout.write(self.style.SUCCESS('Successfully populated ItemOrder with predefined prices'))

    def create_item_orders(self, item_courts, current_date, start_time, end_time, price):
        item_orders = []
        current_time = start_time
        while current_time < end_time:
            next_time = (datetime.combine(date.today(), current_time) + timedelta(hours=1)).time()
            for court in item_courts:
                item_time, created = ItemTime.objects.get_or_create(
                    item_court=court,
                    start_time=current_time,
                    end_time=next_time
                )
                if created:
                    item_time.save()
                item_orders.append(ItemOrder(
                    item_time=item_time,
                    date=current_date,
                    money=price,
                    flag=0,  # Available
                    status=True  # Open
                ))
            current_time = next_time
        return item_orders

    def is_holiday(self, check_date):
        # Implement logic to check if the given date is a holiday
        # For now, let's assume it's a placeholder that returns False
        return False
