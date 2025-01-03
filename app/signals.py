from decimal import Decimal
import holidays
from django.core.management import call_command
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Venue, Item, ItemCourt, ItemTime, ItemOrder
from datetime import datetime, time, date, timedelta
from courtManagementSystem import proj_settings

# Flag to prevent re-running the command during post_migrate
already_ran = False

@receiver(post_migrate)
def create_initial_data(sender, **kwargs):
    global already_ran

    if already_ran:
        return  # Avoid running again

    # Create the venue if it doesn't exist
    venue, created = Venue.objects.get_or_create(name=proj_settings.VENUE_NAME, status=proj_settings.VENUE_STATUS)

    # Create the item if it doesn't exist
    item, created = Item.objects.get_or_create(name=proj_settings.ITEM_NAME, venue=venue)

    # Create multiple item courts
    courts = proj_settings.COURTS
    for court_name in courts:
        ItemCourt.objects.get_or_create(name=court_name, item=item, nature=1)

    # Now handle the creation of ItemTime for each ItemCourt
    create_item_times()

    # Set the flag to avoid re-running the command
    already_ran = True

    # Now create item orders for 365 days by calling the management command
    try:
        call_command('populate_item_orders')  # Programmatically run the management command
        print("Successfully ran the populate_item_orders command")
    except Exception as e:
        print(f"Error running populate_item_orders command: {e}")

def create_item_times():
    # Retrieve start and end hours from settings
    start_hour = proj_settings.START_HOUR  # Default to 7am if not set
    end_hour = proj_settings.END_HOUR  # Default to 11pm if not set

    courts = ItemCourt.objects.all()
    item_times = []

    for court in courts:
        # Check if ItemTime already exists for this court
        if ItemTime.objects.filter(item_court=court).exists():
            continue  # Skip if time slots are already created

        # Create time slots for the court
        for hour in range(start_hour, end_hour):
            start_time = time(hour=hour)
            end_time = time(hour=hour + 1)
            item_times.append(ItemTime(item_court=court, start_time=start_time, end_time=end_time))

    # Bulk create ItemTime entries
    if item_times:
        ItemTime.objects.bulk_create(item_times)
        print(f"Successfully populated ItemTime for each court from {start_hour} to {end_hour}")
    else:
        print("ItemTime already exists for all courts, no new records created.")
