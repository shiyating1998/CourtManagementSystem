
from django.core.mail import send_mail
from datetime import datetime


def send_booking_confirmation(email, first_name, last_name, booking_details):
    subject = 'Booking Confirmation'
    message = f"Dear {first_name} {last_name},\n\nYour booking has been confirmed. Here are the details:\n\n{booking_details}\n\nThank you for booking with us."
    from_email = 'jlxxily@gmail.com'  # Replace with your actual sender email
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)


def write_log_file(court, action, user, isAdmin):
    file_path = 'output.txt'  # Specify the file name and path

    from datetime import datetime

    # Get the current date and time
    timestamp = datetime.now()  # This gives both date and time
    # Appending to a file
    with open(file_path, 'a') as file:  # Open in append mode
        if isAdmin:
            file.write(f"{court}, {action}, {user}, admin, {timestamp}\n")  # Append a new line
        else:
            file.write(f"{court}, {action}, {user}, Regular User, {timestamp}\n")  # Append a new line
    print(f"Data appended to {file_path}")
