var selectedCells = [];

const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;



function toggleSelect(cell, slot, court, date, isBooked, price) {
    console.log("clicked")
    var today = new Date().toISOString().split('T')[0];
    if (date < today) {
        console.log("date:", date)
        console.log("today:", today)
        return;
    }

    if (isBooked) {
        // open a form containing the information from the user
        // TODO: open a booking details form for booked court

        var cellKey = `${slot}_${court}_${date}_${price}`;
        var slots = cellKey.split('_');
        console.log("slots:", slots)

        var details = date + '<br>' + court + ',' + slot + ',$' + price;
        document.getElementById("bookingDetails").innerHTML = details;
        document.getElementById("bookingForm").style.display = "block";
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
    console.log('Selected Slots for Booking:', slots);
}

function closeForm() {
    document.getElementById("bookingForm").style.display = "none";
}

function showSchedule(date) {
    window.location.href = "?date=" + date;
}

