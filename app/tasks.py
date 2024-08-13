# myapp/tasks.py
from celery import shared_task
from app.models import ProcessedEvent, User, Item, ItemCourt, ItemTime, ItemOrder
from .utils import send_booking_confirmation
import json
from decimal import Decimal
from datetime import datetime, date, timedelta, time
from django.utils import timezone


@shared_task
def process_event(event):
    print("celery processing event...")
    # Handle the event
    if event['type'] == 'payment_intent.succeeded':
        session = event['data']['object']
        print("session:", session)
        output_data_str = json.dumps(session, indent=4)
        # Open the file in append mode
        with open('sessionInfo.txt', 'a') as file:
            # Write the additional data to the file
            file.write(output_data_str)
        # Fulfill the purchase...
        metadata = session['metadata']
        print(f'J metadata: {metadata}')
        print(f'Payment for {session["amount"]} succeeded!')

        metadata = session['metadata']


        selected_slots_json = metadata['selected_slots']
        print(f"Type of selected_slots_json: {type(selected_slots_json)}")  # Should be <class 'str'>
        print(f'selected_slots_json: {selected_slots_json}')

        selected_slots = json.loads(metadata['selected_slots'])
        print(f"Type of selected_slots: {type(selected_slots)}")
        print(f'selected_slots: {selected_slots}')

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
        print(f"user: {user}")

        booking_details = [selected_slots[0][2]]


        for slot in selected_slots:
            print(f"slot {slot}")
            start_time, court_name, booking_date, price = slot
            print(f"start: {start_time}" )
            print(f"court: {court_name}" )
            print(f"booking_date: {booking_date}" )
            print(f"price: {price}" )

            start_time_obj = datetime.strptime(start_time.split('-')[0], "%H:%M").time()
            end_time_obj = (datetime.combine(date.today(), start_time_obj) + timedelta(hours=1)).time()
            print(f"start_time: {start_time_obj}" )
            print(f"end_time: {end_time_obj}" )
            booking_date_obj = datetime.strptime(booking_date, "%Y-%m-%d").date()
            print(f"booking_date_obj: {booking_date_obj}")

            item = Item.objects.get(id=1)
            print(f"item: {item}" )

            item_court = ItemCourt.objects.get(name=court_name, item=item)
            print(f"item_court: {item_court}")

            item_time = ItemTime.objects.get(item_court=item_court, start_time=start_time_obj,
                                             end_time=end_time_obj)
            print(f"item_time object: {item_time}" )

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
            print("order booked:", item_order)

            booking_details.append(f"{court_name},  {start_time_obj} - "
                                   f"{end_time_obj}, ${price} ")
            #total = total + float(price)
        booking_details_str = "\n".join(booking_details)
        booking_details_str = booking_details_str + '\nTotal: $' + str(total)
        send_booking_confirmation(email, first_name, last_name, booking_details_str)

        print(f'Payment for {session["amount"]} succeeded!')
    else:
        print('Unhandled event type {}'.format(event['type']))


@shared_task
def simple_task():
    print("Task executed successfully")