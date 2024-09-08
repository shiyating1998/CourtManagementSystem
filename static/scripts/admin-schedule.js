var selectedCells = [];

const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;




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
                // Hide button and remove from layout
    document.getElementById("btnCancelBooking").style.display = "none";
    console.log('Selected Slots for Booking:', slots);
}

function closeForm() {
    document.getElementById("bookingForm").style.display = "none";
}

function showSchedule(date) {
    window.location.href = "?date=" + date;
}

