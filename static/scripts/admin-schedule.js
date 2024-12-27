document.addEventListener("DOMContentLoaded", () => {
    const buttons = document.querySelectorAll("#dates button");

    buttons.forEach(button => {
        const dateStr = button.getAttribute("data-date");

        const dateParts = dateStr.split(" "); // Split into ["Sun", "2024-12-29"]
        
        // Parse the second part (YYYY-MM-DD) into a Date object
        const date = new Date(dateParts[1]);

        // Check if the day is Saturday (5) or Sunday (6)
        if (date.getDay() === 5 || date.getDay() === 6) {
            button.classList.add("weekend");
        }
    });
});
var selectedCells = [];

const form = document.getElementById('bookingFormId');
const csrfToken = form.querySelector('[name=csrfmiddlewaretoken]').value;
console.log("csrftoken:", csrfToken)
const formURL = document.getElementById('urlId');
// Get URLs from data attributes
const bookUrl = formURL.getAttribute('data-book-url');
const cancelUrl = formURL.getAttribute('data-cancel-url');
const orderInfoUrl = formURL.getAttribute('data-order-info-url');


function openForm() {
    if (selectedCells.length === 0) {
        alert("Please select at least one slot.");
        return;
    }

    var slots = selectedCells.map(c => c.split('_'));

    var details = slots[0][2] + '<br>'
    details = details + slots.map(s => `${s[1]}, ${s[0]}, $${s[3]}`).join('<br>');
    var total = slots.map(s => parseFloat(s[3])).reduce((sum, value) => sum + value, 0);
    total = parseFloat(total).toFixed(2);
    details = details + '<br> Total: $' + total;

    document.getElementById("selected_slots").value = JSON.stringify(slots);
    document.getElementById("bookingDetails").innerHTML = details;
    document.getElementById("bookingForm").style.display = "block";


    document.getElementById("divInput").style.display = "block";

    // Hide button and remove from layout
    document.getElementById("btnCancelBooking").style.display = "none";
    document.getElementById("btnBook").style.display = "block";
    console.log('Selected Slots for Booking:', slots);
}

function closeForm() {
    document.getElementById("bookingForm").style.display = "none";
    //window.location.reload();
}

function showSchedule(date) {
    window.location.href = "?date=" + date;
}

document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('bookingFormId');
    const csrfToken = form.querySelector('[name=csrfmiddlewaretoken]').value;
    console.log("DOMContentLoaded: ", csrfToken)
    form.addEventListener('submit', function (event) {


        event.preventDefault(); // Prevent default form submission
        const formData = new FormData(form);
        fetch(bookUrl, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': csrfToken
            }
        })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    document.getElementById('formErrors').textContent = data.error;
                } else {
                    // Handle success (e.g., show a success message or redirect)
                    //document.getElementById('formErrors').textContent = '';
                    //alert('Booking successful!');
                    // Optionally redirect or close the form
                    // Reload the page
                    //closeForm();
                    window.location.reload();
                }
            })
            .catch(error => {
                console.error('Error:', error);
                document.getElementById('formErrors').textContent = 'An error occurred. Please try again.';
            });
    });
});


function cancelBooking() {
    var info = document.getElementById("info").value;
    console.log("info: ", info);

    // Assuming the format is "start_time-end_time_court_name_date_price"
    // We can split the string by underscores and further split by hyphens for the time
    var parts = info.split('_');
    var timeRange = parts[0].split('-'); // Splitting "20:00-21:00" to get start and end times

    var start_time = timeRange[0]; // Start time (20:00)
    var end_time = timeRange[1];   // End time (21:00)
    var court_name = parts[1];     // Court name (Court 7)
    var booking_date = parts[2];   // Booking date (2024-09-08)
    var price = parts[3];          // Price (30)

    // Now create FormData and append the extracted values
    var formData = new FormData();
    formData.append('start_time', start_time);   // Pass the start_time
    formData.append('end_time', end_time);       // Optionally pass the end_time if needed
    formData.append('court_name', court_name);   // Pass the court_name
    formData.append('booking_date', booking_date); // Pass the booking_date
    formData.append('price', price);             // Optionally pass the price if needed
    fetch(cancelUrl, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': csrfToken
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.reload();
            } else if (data.error) {
                document.getElementById('formErrors').textContent = data.error;
            }
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('formErrors').textContent = 'An error occurred. Please try again.';
        });
}

function toggleSelect(cell, slot, court, date, isBooked, price) {
    console.log("clicked")
    // Convert estDateString to a Date object
    let estDate = new Date(new Date().toLocaleString("en-US", { timeZone: "America/New_York" }));  // This will include time

    let estDateFormatted = estDate.getFullYear() + "-" +
        ("0" + (estDate.getMonth() + 1)).slice(-2) + "-" +
        ("0" + estDate.getDate()).slice(-2);

    // User shouldn't book a previous date
    if (date < estDateFormatted) {
        console.log("User shouldn't book a previous date");
        return;
    }

    if (isBooked) {
        // Deselect all previously selected cells
        selectedCells.forEach(function (cellKey) {
            var cellData = cellKey.split('_'); // Extract the slot, court, and date from cellKey
            var selectedCell = document.querySelector(`[data-slot="${cellData[0]}"][data-court="${cellData[1]}"][data-date="${cellData[2]}"]`);
            if (selectedCell) {
                selectedCell.classList.remove('selected');
            }
        });
        selectedCells = [];
        var cellKey = `${slot}_${court}_${date}_${price}`;
        var slots = cellKey.split('_');
        console.log("slots:", slots);

        var details = date + '<br>' + court + ',' + slot + ',$' + price;
        document.getElementById("bookingDetails").innerHTML = details;
        document.getElementById("bookingForm").style.display = "block";
        document.getElementById("info").value = cellKey;
        document.getElementById("divInput").style.display = "none";
        // Show button and add back to layout
        document.getElementById("btnCancelBooking").style.display = "block";
        document.getElementById("btnBook").style.display = "none";
        // Create a FormData object to send data to the server
        var formData = new FormData();
        formData.append('start_time', slot);   // Pass the start_time
        formData.append('court_name', court);  // Pass the court_name
        formData.append('booking_date', date); // Pass the booking_date

        fetch(orderInfoUrl, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': csrfToken
            }
        })
            .then(response => response.json())
            .then(data => {
    if (data.success) {
        // Function to capitalize the first letter of a string
        function capitalizeFirstLetter(string) {
            return string.charAt(0).toUpperCase() + string.slice(1).toLowerCase();
        }

        // Access user information from the response and capitalize names
        var userInfo = `
            Name: ${capitalizeFirstLetter(data.user.first_name)} ${capitalizeFirstLetter(data.user.last_name)} <br>
            Email: ${data.user.email} <br>
            Phone: ${data.user.phone} <br>
            Amount Paid: $${data.money} <br>
            Booking Date: ${data.booking_date} <br>
            Status: ${data.status ? 'Open' : 'Closed'} <br>
            Flag: ${data.flag} <br>
        `;

        // Display user and booking details in a div
        document.getElementById('bookingDetails').innerHTML = userInfo;
    } else if (data.error) {
        document.getElementById('formErrors').textContent = data.error;
    }
})
            .catch(error => {
                console.error('Error:', error);
                document.getElementById('formErrors').textContent = 'An error occurred. Please try again.';
            });

        return;
    }

    var cellKey = `${slot}_${court}_${date}_${price}`;
    if (selectedCells.includes(cellKey)) {
        selectedCells = selectedCells.filter(c => c !== cellKey);
        cell.classList.remove('selected');
    } else {
        selectedCells.push(cellKey);
        cell.classList.add('selected');
    }

    console.log(selectedCells)
}