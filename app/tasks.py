# myapp/tasks.py

from celery import shared_task
import stripe
from app.models import ProcessedEvent

@shared_task
def process_event(event):
    print("celery processing event...")
    # Handle the event
    if event['type'] == 'payment_intent.succeeded':
        session = event['data']['object']
        print("session:", session)
        # Fulfill the purchase...
        print(f'Payment for {session["amount"]} succeeded!')
    else:
        print('Unhandled event type {}'.format(event['type']))


@shared_task
def simple_task():
    print("Task executed successfully")