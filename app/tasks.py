# myapp/tasks.py
import json

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
        output_data_str = json.dumps(session, indent=4)
        # Open the file in append mode
        with open('sessionInfo.txt', 'a') as file:
            # Write the additional data to the file
            file.write(output_data_str)
        # Fulfill the purchase...
        metadata = session['metadata']
        print("J metadata: ", metadata)
        # TODO 1 send an email
        # TODO 2 update db
        print(f'Payment for {session["amount"]} succeeded!')
    else:
        print('Unhandled event type {}'.format(event['type']))


@shared_task
def simple_task():
    print("Task executed successfully")