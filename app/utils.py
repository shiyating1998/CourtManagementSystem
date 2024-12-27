from django.core.mail import send_mail

def send_booking_confirmation(email, first_name, last_name, booking_details):
    subject = 'Booking Confirmation'
    message = f"Dear {first_name.capitalize()} {last_name.capitalize()},\n\nYour booking has been confirmed. Here are the details:\n\n{booking_details}\n\nThank you for booking with us."
    from_email = 'jlxxily@gmail.com'  # Replace with your actual sender email
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)


def send_cancellation_confirmation(email, first_name, last_name, booking_details):
    subject = 'Booking Cancellation Confirmation'
    message = f"Dear {first_name.capitalize()} {last_name.capitalize()},\n\nYour booking has been cancelled. Here are the cancelled booking details:\n\n{booking_details}\n\nPlease contact us if you have any questions."
    from_email = 'jlxxily@gmail.com'  # Replace with your actual sender email
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)
