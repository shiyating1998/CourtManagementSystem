from django.core.mail import send_mail
from datetime import datetime

from app.models import Booking


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
    if action == 'Book':
        court = format_bookings(court)
    with open(file_path, 'a') as file:  # Open in append mode
        if isAdmin:
            file.write(f"{date}, {court}, {action}, {user}, Admin, {timestamp}\n")  # Append a new line
        else:
            file.write(f"{date}, {court}, {action}, {user}, Regular User, {timestamp}\n")  # Append a new line
    print(f"Data appended to {file_path}")

def format_bookings(bookings):
    print(bookings)
    if not bookings:
        return ""

    # Collect formatted time slots and courts
    time_and_court = [f"{time_slot} {court}" for time_slot, court, _, _ in bookings]

    # Join the formatted parts together
    formatted_output = "; ".join(time_and_court)

    return formatted_output


# Function to parse and save the input data to the database
def parse_and_save_bookings(file_path):
    with open(file_path, 'r') as f:
        data = f.readlines()

    for line in data:
        row = line.strip().split(', ')
        time_and_court_segments = row[1].split('; ')

        for segment in time_and_court_segments:
            # Split the segment into time and court
            time, court = segment.split(' Court ')

            # Reconstruct the court number with 'Court' prefix
            court = f"Court {court}"

            # Save the booking information
            booking = Booking(
                date=datetime.strptime(row[0], "%Y-%m-%d").date(),
                time=time,  # Storing the time part
                court=court,  # Storing the court part
                action=row[2],
                user=row[3],
                user_role=row[4],
                timestamp=datetime.strptime(row[5], "%Y-%m-%d %H:%M:%S")
            )
            booking.save()
    print("Bookings successfully saved to the database!")