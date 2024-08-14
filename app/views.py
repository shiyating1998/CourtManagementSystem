import json
from decimal import Decimal
from datetime import datetime, date, timedelta, time
import stripe
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.utils.http import urlencode
from django.views import View
from django.views.generic import TemplateView
from courtManagementSystem import settings
from .models import User, Item, ItemCourt, ItemTime, ItemOrder, ProcessedEvent
from .tasks import process_event
from django.views.decorators.csrf import csrf_exempt

stripe.api_key = settings.STRIPE_SECRET_KEY

import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

def my_view(request):
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
    logger.critical("Critical message")
    # Your view logic here
    return render(request, "booking/schedule.html")

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
    # for order in item_orders:
    # print(order)  # This will print the string representation defined in the __str__ method

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
        "courts": courts,  # TODO
        "time_slots": time_slots  # TODO
    }

    return render(request, "booking/schedule.html", context)

@csrf_exempt  # TODO
def payment_success(request):
    return render(request, 'booking/payment_success.html')

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError:
        # Invalid payload
        return JsonResponse({'success': False}, status=400)
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return JsonResponse({'success': False}, status=400)

    event_id = event['id']

    # Check if the event has already been processed
    if ProcessedEvent.objects.filter(event_id=event_id).exists():
        return JsonResponse({'success': True})

    # Log the event ID to prevent future duplicates
    ProcessedEvent.objects.create(event_id=event_id)

    # add to celery queue
    process_event.delay(event)
    return JsonResponse({'success': True})


class StripeIntentView(View):
    def post(self, request, *args, **kwargs):
        try:
            intent = stripe.PaymentIntent.create(
                amount=500,  # dummy value, will be updated in the UpdatePaymentIntent
                currency='cad',
            )
            return JsonResponse({
                'clientSecret': intent['client_secret']
            })
        except Exception as e:
            return JsonResponse({'error': str(e)})


@csrf_exempt
def update_payment_intent(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        payment_intent_id = data['payment_intent_id']
        selected_slots = data['selected_slots']
        first_name = data['first_name']
        last_name = data['last_name']
        email = data['email']
        phone = data['phone']
        total = data['total']
        # print(f"total $ {total}")
        try:
            intent = stripe.PaymentIntent.modify(
                payment_intent_id,
                amount=int(float(total) * 100),  # amount is in cents
                metadata={
                    'selected_slots': json.dumps(selected_slots),
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email,
                    'phone': phone,
                    'total': float(total)
                }
            )
            # print("update successfully here")
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)
