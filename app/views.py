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

def booking_schedule(request):
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
        "09:00-10:00", "10:00-11:00", "11:00-12:00", "12:00-13:00",
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

    return render(request, "booking/schedule.html", context)



def send_booking_confirmation(email, first_name, last_name, booking_details):
    subject = 'Booking Confirmation'
    message = f"Dear {first_name} {last_name},\n\nYour booking has been confirmed. Here are the details:\n\n{booking_details}\n\nThank you for booking with us."
    from_email = 'jlxxily@gmail.com'  # Replace with your actual sender email
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt #TODO
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

            # TODO null checking
            booking_details = [selected_slots[0][2]]
            total = 0

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

                booking_details.append(f"{court_name},  {start_time_obj} - "
                                       f"{end_time_obj}, ${price} ")
                total = total + float(price)
            booking_details_str = "\n".join(booking_details)
            booking_details_str = booking_details_str + '\nTotal: $' + str(total)
            send_booking_confirmation(email, first_name, last_name, booking_details_str)

            # TODO only after payment we confirm booking and send email
            # Redirect to payment form
            # return redirect(reverse('payment_form') ) #+ f'?booking_id={booking.id}')

            url = reverse('booking_schedule')
            query_params = {'date': booking_date}  # Using the booking_date from the loop above
            url_with_query = f"{url}?{urlencode(query_params)}"

            return redirect(url_with_query)


    print("got here")
    return booking_schedule(request)
@csrf_exempt #TODO
def payment_form(request):
    # booking_id = request.GET.get('booking_id')
    # return render(request, 'payment_form.html', {'booking_id': booking_id})

    return render(request, 'booking/payment_form.html')
@csrf_exempt #TODO
def process_payment(request):
    print("processing payment...")
    if request.method == 'POST':
        booking_id = request.POST['booking_id']
        card_number = request.POST['card_number']
        expiry_date = request.POST['expiry_date']
        cvv = request.POST['cvv']
        billing_address = request.POST['billing_address'] # Optional

        print("booking_id: ", booking_id)
        print("card_number: ", card_number)
        print("expiry_date: ", expiry_date)
        print("cvv: ", cvv)
        print("billing_address: ", billing_address)
        # TODO Ning: Process payment (implement your payment gateway logic here)
        # If successful, update booking status

        return redirect('payment_success')  # Redirect to a success page
    return render(request, 'booking/payment_form.html')
@csrf_exempt #TODO
def payment_success(request):
    return render(request, 'booking/payment_success.html')