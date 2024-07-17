var selectedCells = [];

function toggleSelect(cell, slot, court, date, isBooked, price) {
    console.log("clicked")
    var today = new Date().toISOString().split('T')[0];
    if (date < today) {
        return;
    }

    if (isBooked) {
        return;
    }

    var cellKey = `${slot}_${court}_${date}_${price}`;
    if (selectedCells.includes(cellKey)) {
        selectedCells = selectedCells.filter(c => c !== cellKey);
        cell.classList.remove('selected');
        console.log("remove selected")
    } else {
        selectedCells.push(cellKey);
        cell.classList.add('selected');
        console.log(" selected")
    }
}

function openForm() {
    if (selectedCells.length === 0) {
        alert("Please select at least one slot.");
        return;
    }

    var slots = selectedCells.map(c => c.split('_'));
    var details = slots.map(s => `${s[1]}, ${s[0]}, ${s[2]}`).join('<br>');

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
