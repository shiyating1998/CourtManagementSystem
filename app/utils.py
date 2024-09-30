from django.core.mail import send_mail
from datetime import datetime


def send_booking_confirmation(email, first_name, last_name, booking_details):
    subject = 'Booking Confirmation'
    message = f"Dear {first_name} {last_name},\n\nYour booking has been confirmed. Here are the details:\n\n{booking_details}\n\nThank you for booking with us."
    from_email = 'jlxxily@gmail.com'  # Replace with your actual sender email
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)


def write_log_file(date, court, action, user, isAdmin):
    file_path = 'output.txt'  # Specify the file name and path



    # Get the current date and time
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # This gives both date and time
    # Appending to a file
    with open(file_path, 'a') as file:  # Open in append mode
        if isAdmin:
            file.write(f"{date}, {format_bookings(court)}, {action}, {user}, Admin, {timestamp}\n")  # Append a new line
        else:
            file.write(f"{date}, {format_bookings(court)}, {action}, {user}, Regular User, {timestamp}\n")  # Append a new line
    print(f"Data appended to {file_path}")

def format_bookings(bookings):
    if not bookings:
        return ""

    # Extract the date from the first booking (all dates should be the same)
    date = bookings[0][2]

    # Collect formatted time slots and courts
    time_and_court = [f"{time_slot} {court}" for time_slot, court, _, _ in bookings]

    # Join the formatted parts together
    formatted_output = "; ".join(time_and_court)

    return formatted_output