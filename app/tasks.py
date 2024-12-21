# myapp/tasks.py
import json
import logging
from datetime import datetime, date, timedelta
from decimal import Decimal

from celery import shared_task
from django.utils import timezone
from django.db import transaction
from app.models import User, Item, ItemCourt, ItemTime, ItemOrder, Booking
from .utils import send_booking_confirmation
from django.db.utils import OperationalError

# Get an instance of a logger
logger = logging.getLogger('django')

@shared_task
def process_event(event):
    for _ in range(5): 
        try:
            with transaction.atomic():
                logger.info("celery processing event...")
                # Handle the event
                if event['type'] == 'payment_intent.succeeded':
                    session = event['data']['object']
                    logger.info(f'Payment for {session["amount"]} succeeded!')
                    metadata = session['metadata']

                    selected_slots = json.loads(metadata['selected_slots'])

                    first_name = metadata['first_name']
                    last_name = metadata['last_name']
                    email = metadata['email']
                    phone = metadata['phone']
                    total = metadata['total']
                    total = "{:.2f}".format(float(total))

                    user, created = User.objects.get_or_create(
                        email=email,
                        defaults={'first_name': first_name, 'last_name': last_name, 'phone': phone,
                                'username': first_name + '_' + last_name}
                    )
                    logger.info(f"user: {user}")

                    booking_date = selected_slots[0][2]
                    booking_details = [booking_date]

                    # write_log_file(booking_date, selected_slots, "Book", first_name + "_" + last_name, False)

                    for slot in selected_slots:
                        logger.info(f"slot {slot}")
                        start_time, court_name, booking_date, price = slot

                        start_time_obj = datetime.strptime(start_time.split('-')[0], "%H:%M").time()
                        end_time_obj = (datetime.combine(date.today(), start_time_obj) + timedelta(hours=1)).time()
                        booking_date_obj = datetime.strptime(booking_date, "%Y-%m-%d").date()

                        item = Item.objects.get(id=1)

                        item_court = ItemCourt.objects.get(name=court_name, item=item)

                        item_time = ItemTime.objects.get(item_court=item_court, start_time=start_time_obj,
                                                        end_time=end_time_obj)

                        item_order, created = ItemOrder.objects.update_or_create(
                            item_time=item_time,
                            date=booking_date_obj,
                            defaults={
                                'user': user,
                                'money': Decimal(price),
                                'flag': 1,  # Booked
                                'status': False,  # Booked
                                'modification_time': timezone.now()  # Update the modification time
                            }
                        )
                        logger.info(f"order booked: {item_order}" )
                        booking_details.append(f"{court_name},  {start_time_obj.strftime('%H:%M')} - "
                                            f"{end_time_obj.strftime('%H:%M')}, ${price} ")

                        # Save the booking information
                        booking = Booking(
                            date=booking_date_obj,
                            time=start_time,  # Storing the time part
                            court=court_name,  # Storing the court part
                            action='Book',
                            user=user.first_name.capitalize() + " " + user.last_name.capitalize(),
                            user_role=user.first_name.capitalize() + " " + user.last_name.capitalize(),
                            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        )
                        booking.save()
                        #total = total + float(price)
                    booking_details_str = "\n".join(booking_details)
                    booking_details_str = booking_details_str + '\nTotal: $' + str(total)
                    send_booking_confirmation(email, first_name, last_name, booking_details_str)

                    logger.info(f'Payment for {session["amount"]} succeeded!')
                else:
                    logger.info('Unhandled event type {}'.format(event['type']))
            break
                
        except OperationalError as e:
            if "database is locked" in str(e):
                time.sleep(1)  # Wait for a second before retrying
                logger.info("Database is locked, retrying...")
            else:
                raise

    
