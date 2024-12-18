import csv
import json
from datetime import datetime, date, timedelta
from decimal import Decimal

import pytz
import stripe
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from django.utils import timezone
from django.utils.http import urlencode
from django.views import View
from django.views.decorators.cache import cache_control

from courtManagementSystem import settings, proj_settings
from .models import User, Item, ItemCourt, ItemTime, ItemOrder, ProcessedEvent, Booking
from .tasks import process_event
from .utils import send_booking_confirmation

stripe.api_key = settings.STRIPE_SECRET_KEY

import logging
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from django.contrib import messages

from django.views.decorators.csrf import csrf_exempt

# Get an instance of a logger
logger = logging.getLogger("django")

courts = proj_settings.COURTS
time_slots = proj_settings.TIME_SLOTS


def admin_only_access(request):
    messages.error(request, "Only admin users can access this page.")
    return render(
        request, "error_page.html"
    )  # You can create a template called 'error_page.html'


def is_admin(user):
    return user.is_staff  # Or you could use user.is_superuser if needed


@user_passes_test(is_admin)
def booking_list(request):
    bookings = Booking.objects.all().order_by('date', 'time')  # Fetch all bookings
    return render(request, 'admin/view_log.html', {'bookings': bookings})


@user_passes_test(is_admin)
def download_bookings_csv(request):
    # Create the HttpResponse object with the correct CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="booking_log.csv"'

    # Create a CSV writer object.
    writer = csv.writer(response)

    # Write the header row for the CSV file.
    writer.writerow(['Date', 'Time', 'Court', 'Action', 'User', 'User Role', 'Timestamp'])

    # Query the bookings and write each row to the CSV.
    bookings = Booking.objects.all().order_by('date', 'time')
    for booking in bookings:
        writer.writerow([booking.date, booking.time, booking.court, booking.action, booking.user, booking.user_role,
                         booking.timestamp])

    return response


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def booking_schedule(request):
    # Get the current UTC time
    current_time = datetime.now(pytz.utc)

    # Convert to EST
    est_timezone = pytz.timezone("US/Eastern")
    current_time = current_time.astimezone(est_timezone)
    today = datetime.now().date()
    selected_date = request.GET.get("date", today.strftime("%Y-%m-%d"))

    # TODO make it configuarable
    dates = [(today + timedelta(days=i)).strftime("%a %Y-%m-%d") for i in range(8)]

    # TODO: filter by venue, and filter by item (badminton), filter by date
    #   hardcode to venue = lions
    #   item = badminton
    #   date = today for now

    # Query all ItemOrder instances where the date matches selected_date
    item_orders = ItemOrder.objects.filter(date=selected_date)

    context = {
        "dates": dates,
        "selected_date": selected_date,
        "item_orders": item_orders,
        "today": today.strftime("%a %Y-%m-%d"),
        "courts": courts,
        "time_slots": time_slots,
        "current_time": current_time.strftime("%Y-%m-%d-%H"),  # testing
    }
    return render(request, "booking/schedule.html", context)


@user_passes_test(is_admin)
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_booking_schedule(request):
    # Get the current UTC time
    current_time = datetime.now(pytz.utc)

    # Convert to EST
    est_timezone = pytz.timezone("US/Eastern")
    current_time = current_time.astimezone(est_timezone)

    today = datetime.now().date()
    selected_date = request.GET.get("date", today.strftime("%Y-%m-%d"))

    # TODO make it configuarable
    dates = [(today + timedelta(days=i)).strftime("%a %Y-%m-%d") for i in range(-7, 22)]

    # TODO: filter by venue, and filter by item (badminton), filter by date
    #   hardcode to venue = lions
    #   item = badminton
    #   date = today for now

    # Query all ItemOrder instances where the date matches selected_date
    item_orders = ItemOrder.objects.filter(date=selected_date)

    context = {
        "dates": dates,
        "selected_date": selected_date,
        "item_orders": item_orders,
        "today": today.strftime("%a %Y-%m-%d"),
        "courts": courts,
        "time_slots": time_slots,
        "current_time": current_time.strftime("%Y-%m-%d-%H"),  # testing
    }
    return render(request, "admin/admin-schedule.html", context)


@csrf_exempt  # TODO
def payment_success(request):
    return render(request, "booking/payment_success.html")


@csrf_exempt
def stripe_webhook(request):
    print("stripe_webhook...")
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError:
        # Invalid payload
        return JsonResponse({"success": False}, status=400)
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return JsonResponse({"success": False}, status=400)

    event_id = event["id"]

    # Check if the event has already been processed
    if ProcessedEvent.objects.filter(event_id=event_id).exists():
        return JsonResponse({"success": True})

    # Log the event ID to prevent future duplicates
    ProcessedEvent.objects.create(event_id=event_id)

    # add to celery queue
    process_event.delay(event)
    return JsonResponse({"success": True})


class StripeIntentView(View):
    def post(self, request, *args, **kwargs):
        try:
            intent = stripe.PaymentIntent.create(
                amount=500,  # dummy value, will be updated in the UpdatePaymentIntent
                currency="cad",
            )
            return JsonResponse({"clientSecret": intent["client_secret"]})
        except Exception as e:
            return JsonResponse({"error": str(e)})


@csrf_exempt
def update_payment_intent(request):
    if request.method == "POST":
        data = json.loads(request.body)
        payment_intent_id = data["payment_intent_id"]
        selected_slots = data["selected_slots"]
        first_name = data["first_name"]
        last_name = data["last_name"]
        email = data["email"]
        phone = data["phone"]
        total = data["total"]
        # logger.info(f"total $ {total}")
        try:
            intent = stripe.PaymentIntent.modify(
                payment_intent_id,
                amount=int(float(total) * 100),  # amount is in cents
                metadata={
                    "selected_slots": json.dumps(selected_slots),
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email,
                    "phone": phone,
                    "total": float(total),
                },
            )
            # logger.info("update successfully here")
            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)


def user_exists(email):
    return User.objects.filter(email=email).exists()


def validate_user(email, first_name, last_name):
    # Convert first_name and last_name to lowercase for comparison
    first_name = first_name.lower()
    last_name = last_name.lower()
    print(f"first: {first_name}")
    print(f"last: {last_name}")
    try:
        a = User.objects.get(email=email, first_name=first_name, last_name=last_name)
        return True  # User exists and matches the details
    except ObjectDoesNotExist:
        return False  # No matching user found


def book_slot(request):
    if request.method == "POST":
        # Retrieve data from the form
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        selected_slots = json.loads(request.POST.get("selected_slots"))

        # if email entered check email exists in db and matches firstname and lastname
        # if not match, return error
        # if email not entered
        # create dummy email firstname_lastname@dummy.com
        # get the user if it already exists, otherwise create new

        if not email:
            email = f"{first_name}_{last_name}@dummy.com"

        valid = True
        if user_exists(email):
            valid = validate_user(email, first_name, last_name)
        if not valid:
            # return Error to the front-end
            return JsonResponse(
                {"error": "Email address already registered with another name."}
            )

        logger.info(f"phone: {phone}")
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "first_name": first_name,
                "last_name": last_name,
                "phone": phone,
                "username": first_name + "_" + last_name,
            },
        )
        logger.info(f"user: {user} ")

        booking_date = selected_slots[0][2]
        booking_details = [booking_date]

        for slot in selected_slots:
            start_time, court_name, booking_date, price = slot

            start_time_obj = datetime.strptime(start_time.split("-")[0], "%H:%M").time()
            end_time_obj = (
                    datetime.combine(date.today(), start_time_obj) + timedelta(hours=1)
            ).time()
            booking_date_obj = datetime.strptime(booking_date, "%Y-%m-%d").date()
            item = Item.objects.get(id=1)

            item_court = ItemCourt.objects.get(name=court_name, item=item)

            item_time = ItemTime.objects.get(
                item_court=item_court, start_time=start_time_obj, end_time=end_time_obj
            )

            item_order, created = ItemOrder.objects.update_or_create(
                item_time=item_time,
                date=booking_date_obj,
                defaults={
                    "user": user,
                    "money": Decimal(price),
                    "flag": 1,  # Booked
                    "status": False,  # Booked
                    "modification_time": timezone.now(),  # Update the modification time
                },
            )
            logger.info(f"order booked: {item_order}")

            booking_details.append(
                f"{court_name},  {start_time_obj.strftime('%H:%M')} - "
                f"{end_time_obj.strftime('%H:%M')}, ${price} "
            )

            # Save the booking information
            booking = Booking(
                date=booking_date_obj,
                time=start_time,  # Storing the time part
                court=court_name,  # Storing the court part
                action='Book',
                user=user.first_name.capitalize() + " " + user.last_name.capitalize(),
                user_role=request.user.username,
                timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
            booking.save()

        booking_details_str = "\n".join(booking_details)
        if "@dummy.com" not in email:
            send_booking_confirmation(email, first_name, last_name, booking_details_str)

        url = reverse("admin_booking_schedule")
        query_params = {
            "date": booking_date
        }  # Using the booking_date from the loop above
        url_with_query = f"{url}?{urlencode(query_params)}"
        # return redirect(url_with_query)
        return JsonResponse({"success": True})
    return JsonResponse({"error": "Invalid request method."})


def get_order_info(request):
    if request.method == "POST":
        # Retrieve data from the form
        start_time = request.POST.get("start_time")
        court_name = request.POST.get("court_name")
        booking_date = request.POST.get("booking_date")

        # Parse start_time and booking_date
        start_time_obj = datetime.strptime(start_time.split("-")[0], "%H:%M").time()
        end_time_obj = (
                datetime.combine(date.today(), start_time_obj) + timedelta(hours=1)
        ).time()
        booking_date_obj = datetime.strptime(booking_date, "%Y-%m-%d").date()

        # Retrieve Item and ItemCourt
        item = Item.objects.get(id=1)
        item_court = ItemCourt.objects.get(name=court_name, item=item)

        # Retrieve ItemTime
        item_time = ItemTime.objects.get(
            item_court=item_court, start_time=start_time_obj, end_time=end_time_obj
        )

        # Retrieve ItemOrder
        item_order = ItemOrder.objects.get(item_time=item_time, date=booking_date_obj)

        # Extract the user details from the ItemOrder
        user = item_order.user
        user_data = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "phone": user.phone,
        }

        # Prepare the response data
        response_data = {
            "success": True,
            "user": user_data,
            "money": str(item_order.money),
            "flag": item_order.flag,
            "status": item_order.status,
            "booking_date": str(item_order.date),
        }
        return JsonResponse(response_data)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)


def cancel_booking(request):
    if request.method == "POST":
        # Retrieve data from the form
        start_time = request.POST.get("start_time")
        end_time = request.POST.get("end_time")
        court_name = request.POST.get("court_name")
        booking_date = request.POST.get("booking_date")

        # Parse start_time and booking_date
        start_time_obj = datetime.strptime(start_time, "%H:%M").time()
        end_time_obj = datetime.strptime(end_time, "%H:%M").time()
        booking_date_obj = datetime.strptime(booking_date, "%Y-%m-%d").date()

        # Retrieve Item and ItemCourt
        item = Item.objects.get(id=1)
        item_court = ItemCourt.objects.get(name=court_name, item=item)

        # Retrieve ItemTime
        item_time = ItemTime.objects.get(
            item_court=item_court, start_time=start_time_obj, end_time=end_time_obj
        )

        # Retrieve ItemOrder
        item_order = ItemOrder.objects.get(item_time=item_time, date=booking_date_obj)
        user = item_order.user
        username = user.first_name.capitalize() + " " + user.last_name.capitalize()
        print("username: ", username)
        # court_info = f"{start_time}-{end_time} {court_name}"
        # write_log_file(booking_date, court_info, "Cancel", username, True)
        booking = Booking(
            date=booking_date_obj,
            time=f'{start_time}-{end_time}',  # Storing the time part
            court=court_name,  # Storing the court part
            action='Cancel',
            user=username,
            user_role=request.user.username,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        booking.save()

        # Assuming the same item_time and booking_date_obj are passed in as when booking
        item_order, created = ItemOrder.objects.update_or_create(
            item_time=item_time,
            date=booking_date_obj,
            defaults={
                "user": None,  # Set user to None when canceling the booking
                # 'money': Decimal(0),  # Optionally reset money, depending on your business logic
                "flag": 0,  # Set flag to 0 to indicate it's no longer booked
                "status": True,  # Set status to True to indicate the court is open
                "modification_time": timezone.now(),  # Update the modification time
            },
        )

        # Log and return the response
        logger.info(f"Cancelled successfully")
        return JsonResponse({"success": True})
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def verify_user_and_slots(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")
            first_name = data.get("first_name")
            last_name = data.get("last_name")
            selected_slots = data.get("selected_slots")

            # Step 1: Verify the user details
            valid = True
            if user_exists(email):
                valid = validate_user(email, first_name, last_name)
            if not valid:
                # return Error to the front-end
                return JsonResponse(
                    {"error": "Email address already registered with another name."}
                )

            # Step 2: Check if the selected slots are available
            for slot in selected_slots:
                start_time, court_name, booking_date, _ = slot
                start_time_obj = datetime.strptime(
                    start_time.split("-")[0], "%H:%M"
                ).time()
                end_time_obj = (
                        datetime.combine(date.today(), start_time_obj) + timedelta(hours=1)
                ).time()
                booking_date_obj = datetime.strptime(booking_date, "%Y-%m-%d").date()
                # Check if the slot is already booked
                item_court = ItemCourt.objects.get(name=court_name)
                item_time_booked = ItemOrder.objects.filter(
                    item_time__item_court=item_court,
                    item_time__start_time=start_time_obj,
                    item_time__end_time=end_time_obj,
                    date=booking_date_obj,
                    status=False,  # Booked
                ).exists()

                if item_time_booked:
                    print(
                        ItemOrder.objects.filter(
                            item_time__item_court=item_court,
                            item_time__start_time=start_time_obj,
                            item_time__end_time=end_time_obj,
                            date=booking_date_obj,
                            status=False,
                        )
                    )
                    return JsonResponse(
                        {
                            "error": f"Slot on {booking_date} at {start_time} for {court_name} is already booked."
                        },
                        status=400,
                    )

            return JsonResponse({"success": True})
        except Exception as e:
            print(f"An error occurred: {e}")
            return JsonResponse(
                {"error": "An internal server error occurred."}, status=500
            )
