// Add these functions at the start of the file
function showSpinner() {
    document.getElementById('spinnerOverlay').style.display = 'flex';
    document.getElementById('dates').classList.add('processing');
}

function hideSpinner() {
    document.getElementById('spinnerOverlay').style.display = 'none';
    document.getElementById('dates').classList.remove('processing');
}

// Add this variable to track if a request is in progress
let isProcessing = false;

document.addEventListener("DOMContentLoaded", () => {
    const today = new Date().toISOString().split('T')[0];
    const datesContainer = document.getElementById('dates');
    const buttons = datesContainer.querySelectorAll("button");
    const separatorStyle = datesContainer.dataset.separatorStyle || 'line'; // 'line' or 'pipe'

    // Get the selected date from URL query parameter
    const urlParams = new URLSearchParams(window.location.search);
    const selectedDate = urlParams.get('date');

    buttons.forEach((button, index) => {
        const dateStr = button.getAttribute("data-date");
        const dateParts = dateStr.split(" "); // Split into ["Sun", "2024-12-29"]
        const date = new Date(dateParts[1]);
        
        // Get day of week (0 = Sunday, 1 = Monday, ..., 6 = Saturday)
        const dayOfWeek = date.getDay();

        // Add separator before Sunday, but not for the first button
        if (dayOfWeek === 0 && index > 0) {
            if (separatorStyle === 'pipe') {
                const pipe = document.createElement('span');
                pipe.className = 'week-pipe';
                pipe.textContent = ' | ';
                button.parentNode.insertBefore(pipe, button);
            } else {
                const separator = document.createElement('div');
                separator.className = 'week-separator';
                button.parentNode.insertBefore(separator, button);
            }
        }

        // Check if the day is Saturday (5) or Sunday (6)
        if (dayOfWeek === 5 || dayOfWeek === 6) {
            button.classList.add("weekend");
        }

        // Check if this is the selected date (after weekend class)
        if (selectedDate && dateParts[1] === selectedDate) {
            button.classList.add("selected");
        } else if (!selectedDate && dateParts[1] === today) {
            button.classList.add("selected");
        }

        // Debug log to see the dates and their days
        console.log(`Date: ${dateParts[1]}, Day: ${dayOfWeek} (${['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'][dayOfWeek]})`);
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
    // Remove selected class from all buttons
    const buttons = document.querySelectorAll("#dates button");
    buttons.forEach(btn => btn.classList.remove("selected"));
    
    // Add selected class to clicked button
    const selectedButton = document.getElementById("dateButton_" + date);
    if (selectedButton) {
        selectedButton.classList.add("selected");
    }
    
    // Redirect to the new date
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

function bookCourt() {
    if (isProcessing) {
        console.log('Request already in progress');
        return;
    }

    var info = document.getElementById("info").value;
    console.log("info: ", info);

    // Split the info string into its components
    var parts = info.split(',');
    var start_time = parts[0];     // Start time (09:00)
    var end_time = parts[1];       // End time (10:00)
    var booking_date = parts[2];   // Booking date (2024-09-08)
    var price = parts[3];          // Price (30)

    var first_name = document.getElementById("first_name").value;
    var last_name = document.getElementById("last_name").value;
    var email = document.getElementById("email").value;
    var phone = document.getElementById("phone").value;
    var court_name = document.getElementById("court_name").value;

    if (!first_name || !last_name || !phone) {
        document.getElementById('formErrors').textContent = 'Please fill in all required fields.';
        return;
    }

    isProcessing = true;
    showSpinner();

    // Now create FormData and append the extracted values
    var formData = new FormData();
    formData.append('first_name', first_name);
    formData.append('last_name', last_name);
    formData.append('email', email);
    formData.append('phone', phone);
    formData.append('start_time', start_time);   // Pass the start_time
    formData.append('end_time', end_time);       // Pass the end_time
    formData.append('court_name', court_name);   // Pass the court_name
    formData.append('booking_date', booking_date); // Pass the booking_date
    formData.append('money', price);             // Pass the price

    // Get the CSRF token from the form
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    // Make the fetch request
    fetch('/book_slot/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken
        },
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.reload();
            } else if (data.error) {
                document.getElementById('formErrors').textContent = data.error;
                hideSpinner();
            }
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('formErrors').textContent = 'An error occurred. Please try again.';
            hideSpinner();
        })
        .finally(() => {
            isProcessing = false;
        });
}

function cancelBooking() {
    if (isProcessing) {
        console.log('Request already in progress');
        return;
    }

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

    isProcessing = true;
    showSpinner();

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
                hideSpinner();
            }
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('formErrors').textContent = 'An error occurred. Please try again.';
            hideSpinner();
        })
        .finally(() => {
            isProcessing = false;
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