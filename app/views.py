import json
from decimal import Decimal
from datetime import datetime, date, timedelta, time
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.utils.http import urlencode

from .models import User, Item, ItemCourt, ItemTime, ItemOrder
from .forms import BookingForm
def get_price(selected_date, slot):
    # Define time slots and prices
    weekday_prices = [
        (time(15, 0), time(18, 0), Decimal('26.00')),
        (time(18, 0), time(22, 0), Decimal('30.00')),
        (time(22, 0), time(23, 0), Decimal('28.00')),
    ]
    weekend_prices = [
        (time(7, 0), time(9, 0), Decimal('28.00')),
        (time(9, 0), time(23, 0), Decimal('30.00')),
    ]
    holiday_price = Decimal('30.00')

    selected_date_obj = datetime.strptime(selected_date, "%Y-%m-%d").date()
    slot_start_time = datetime.strptime(slot.split('-')[0], "%H:%M").time()
    slot_end_time = datetime.strptime(slot.split('-')[1], "%H:%M").time()

    if selected_date_obj.weekday() < 5:  # Monday to Friday
        for start, end, price in weekday_prices:
            if slot_start_time >= start and slot_end_time <= end:
                return price
    else:  # Saturday and Sunday
        for start, end, price in weekend_prices:
            if slot_start_time >= start and slot_end_time <= end:
                return price

    # Holidays
    # (You can add a function to check if a date is a holiday and return holiday_price)

    return None

def get_order(date, start_time, end_time, court):
    # Query the ItemOrder model
    item_orders = ItemOrder.objects.filter(
        date=date,
        item_time__start_time=start_time,
        item_time__end_time=end_time,
        item_time__item_court__name=court
    )
    for order in item_orders:
        print("get_order: ",order)  # This will print the string representation defined in the __str__ method

    return item_orders

def temp(request):
    today = datetime.now().date()
    selected_date = request.GET.get('date', today.strftime('%Y-%m-%d'))
    print("selected date: ", selected_date)

    dates = [(today + timedelta(days=i)).strftime('%a %Y-%m-%d') for i in range(8)]

    # TODO: filter by venue, and filter by item (badminton), filter by date
    #   hardcode to venue = lions
    #   item = badminton
    #   date = today for now

    # Query all ItemOrder instances where the date matches selected_date
    item_orders = ItemOrder.objects.filter(date=selected_date)

    # Now item_orders contains all ItemOrder instances with date equal to specific_date
    #for order in item_orders:
        #print(order)  # This will print the string representation defined in the __str__ method

    # TODO get courts info from db
    courts = [f"Court {i}" for i in range(1, 10)]
    # TODO get time slots from db
    time_slots = [
        "08:00-09:00", "09:00-10:00", "10:00-11:00", "11:00-12:00", "12:00-13:00",
        "13:00-14:00", "14:00-15:00", "15:00-16:00", "16:00-17:00", "17:00-18:00",
        "18:00-19:00", "19:00-20:00", "20:00-21:00", "21:00-22:00", "22:00-23:00"
    ]


    context = {
        "dates": dates,
        "selected_date": selected_date,
        "item_orders": item_orders,
        "today": today.strftime('%a %Y-%m-%d'),
        "courts": courts, #TODO
        "time_slots": time_slots #TODO

    }

    return render(request, "booking/temp.html", context)



def booking_schedule(request):
    today = date.today()
    dates = [(today + timedelta(days=i)).strftime("%A %Y-%m-%d") for i in range(30)]
    selected_date = request.GET.get('date', today.strftime("%Y-%m-%d"))

    time_slots = [f"{hour}:00-{hour + 1}:00" for hour in range(7, 23)]
    courts = ItemCourt.objects.all()
    bookings = ItemOrder.objects.all()

    booking_dict = {}
    for booking in bookings:
        booking_dict[(booking.item_time.start_time.strftime("%H:%M-%H:%M"), booking.item_time.item_court.name,
                      booking.date.strftime("%Y-%m-%d"))] = booking.user

    context = {
        'dates': dates,
        'today': today.strftime("%Y-%m-%d"),
        'selected_date': selected_date,
        'time_slots': time_slots,
        'courts': courts,
        'bookings': booking_dict,
        'get_price': get_price
    }
    return render(request, 'booking/schedule.html', context)


def book_slot2(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            selected_slots = json.loads(form.cleaned_data['selected_slots'])
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']

            user, created = User.objects.get_or_create(
                email=email,
                defaults={'first_name': first_name, 'last_name': last_name, 'phone': phone}
            )
            print("user: ", user)

            # TODO fixed the hard code
            for slot in selected_slots:
                 print("slot", slot)
                 start_time, court_name, booking_date, price = slot
                 print("start:", start_time)
                 print("court: ", court_name)
                 print("booking_date:", booking_date)
                 print("price:", price)
            #     court = ItemCourt.objects.get(name=court_name)
                 start_time_obj = datetime.strptime(start_time.split('-')[0], "%H:%M").time()
                 end_time_obj = (datetime.combine(date.today(), start_time_obj) + timedelta(hours=1)).time()
                 print("start_time:",start_time_obj )
                 print("end_time:", end_time_obj)
                 booking_date_obj = datetime.strptime(booking_date, "%Y-%m-%d").date()
                 print("booking_date_obj:", booking_date_obj)

                 item = Item.objects.get(
                     id = 1
                 )
                 print("item: ", item)

                 item_court = ItemCourt.objects.get(
                     name = court_name,
                     item = item
                 )
                 print("item_court:", item_court)

                 item_time = ItemTime.objects.get(
                    item_court=item_court,
                    start_time=start_time_obj,
                    end_time=end_time_obj
                 )
                 print("item_time object:", item_time)

                 item_order, created = ItemOrder.objects.update_or_create(
                    item_time=item_time,
                    date=booking_date_obj,
                    defaults={
                        'user': user,
                        'money': Decimal(price),
                        'flag': 1,  # Booked
                        'status': False,  # Open
                        'modification_time': timezone.now()  # Update the modification time
                    }
                 )
                 print("order booked:", item_order)
            return redirect(reverse('booking_schedule'))
    else:
        form = BookingForm()

    return render(request, 'booking/book.html', {'form': form})



def send_booking_confirmation(email, first_name, last_name, booking_details):
    subject = 'Booking Confirmation'
    message = f"Dear {first_name} {last_name},\n\nYour booking has been confirmed. Here are the details:\n\n{booking_details}\n\nThank you for booking with us."
    from_email = 'shiyating1998@gmail.com'  # Replace with your actual sender email
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def book_slot(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            selected_slots = json.loads(form.cleaned_data['selected_slots'])
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']

            user, created = User.objects.get_or_create(
                email=email,
                defaults={'first_name': first_name, 'last_name': last_name, 'phone': phone,
                          'username': first_name+'_'+last_name}
            )
            print("user: ", user)

            booking_details = []

            for slot in selected_slots:
                print("slot", slot)
                start_time, court_name, booking_date, price = slot
                print("start:", start_time)
                print("court: ", court_name)
                print("booking_date:", booking_date)
                print("price:", price)

                start_time_obj = datetime.strptime(start_time.split('-')[0], "%H:%M").time()
                end_time_obj = (datetime.combine(date.today(), start_time_obj) + timedelta(hours=1)).time()
                print("start_time:", start_time_obj)
                print("end_time:", end_time_obj)
                booking_date_obj = datetime.strptime(booking_date, "%Y-%m-%d").date()
                print("booking_date_obj:", booking_date_obj)

                item = Item.objects.get(id=1)
                print("item: ", item)

                item_court = ItemCourt.objects.get(name=court_name, item=item)
                print("item_court:", item_court)

                item_time = ItemTime.objects.get(item_court=item_court, start_time=start_time_obj, end_time=end_time_obj)
                print("item_time object:", item_time)

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

                booking_details.append(f"{court_name}, {booking_date}, {start_time_obj} - "
                                       f"{end_time_obj}, ${price} \n")

            booking_details_str = "\n".join(booking_details)
            send_booking_confirmation(email, first_name, last_name, booking_details_str)

            url = reverse('temp')
            query_params = {'date': booking_date}  # Using the booking_date from the loop above
            url_with_query = f"{url}?{urlencode(query_params)}"
            return redirect(url_with_query)
    else:
        form = BookingForm()

    return render(request, 'booking/book.html', {'form': form})
