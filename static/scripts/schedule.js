var selectedCells = [];

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
        return;
    }

    var formattedPrice = parseFloat(price).toFixed(2);
    var cellKey = `${slot}_${court}_${date}_${formattedPrice}`;
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
    // Get the form element by ID
    const form = document.getElementById("payment-form");
    // Reset the form fields
    form.reset();

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



const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
// TODO: This is your test publishable API key.
const stripe = Stripe("pk_test_51PfA0tRt3PcgmiF6YXj4ROeapnBMPBd7FqSIGJyGvvMoZrVESulq4n0kTbarADCXxDjQQShUD3GbsaKaustZJut400GUgtILbz");

let elements;

const paymentIntentUrl = document.getElementById('payment-intent-url').dataset.url;

let clientSecret;

initialize();
checkStatus();

document
    .querySelector("#payment-form")
    .addEventListener("submit", handleSubmit);




// Fetches a payment intent and captures the client secret
async function initialize() {
    console.log("initializing...")
    const response = await fetch(paymentIntentUrl, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            'X-CSRFToken': csrftoken
        }
    });
    //const { clientSecret } = await response.json();
    const data = await response.json();
    clientSecret = data.clientSecret; // Assign the value to the outer variable

    const appearance = {
        theme: 'stripe',
    };
    elements = stripe.elements({ appearance, clientSecret });

    const paymentElementOptions = {
        layout: "tabs",
    };

    const paymentElement = elements.create("payment", paymentElementOptions);
    paymentElement.mount("#payment-element");
}
async function handleSubmit(e) {
    e.preventDefault();

    // Collect selected slot data
    var slots = selectedCells.map(c => c.split('_'));
    const firstName = document.getElementById('first_name').value;
    const lastName = document.getElementById('last_name').value;
    const email = document.getElementById('email').value;
    const phone = document.getElementById('phone').value;
    var total = slots.map(s => parseFloat(s[3])).reduce((sum, value) => sum + value, 0);

    console.log("[handleSubmit] selectedSlots: ", slots);
    console.log("[handleSubmit] firstName: ", firstName);
    console.log("[handleSubmit] lastName: ", lastName);
    console.log("[handleSubmit] email: ", email);
    console.log("[handleSubmit] phone: ", phone);
    console.log("[handleSubmit] total: ", total);

    setLoading(true);

    // Verify email, user details, and slot availability with backend
    const verifyResponse = await fetch('/verify_user_and_slots/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            email: email,
            first_name: firstName,
            last_name: lastName,
            selected_slots: slots
        })
    });

    const verifyResult = await verifyResponse.json();
    if (verifyResult.error) {
        console.error(verifyResult.error);
        showMessage(verifyResult.error);
        setLoading(false);
        return;
    }

    // Proceed with updating PaymentIntent with metadata
    const updateResponse = await fetch('/update_payment_intent/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            payment_intent_id: clientSecret.split('_secret')[0],
            selected_slots: slots,
            first_name: firstName,
            last_name: lastName,
            email: email,
            phone: phone,
            total: total
        })
    });

    const updateResult = await updateResponse.json();
    if (updateResult.error) {
        console.error(updateResult.error);
        showMessage(updateResult.error);
        setLoading(false);
        return;
    }

    const { error } = await stripe.confirmPayment({
        elements,
        confirmParams: {
            return_url: '${window.location.origin}/payment_success',
            receipt_email: email
        }
    });

    if (error.type === "card_error" || error.type === "validation_error") {
        showMessage(error.message);
    } else {
        showMessage("An unexpected error occurred.");
    }

    setLoading(false);
}

// Fetches the payment intent status after payment submission
async function checkStatus() {
    const clientSecret = new URLSearchParams(window.location.search).get(
        "payment_intent_client_secret"
    );

    if (!clientSecret) {
        return;
    }

    const { paymentIntent } = await stripe.retrievePaymentIntent(clientSecret);

    switch (paymentIntent.status) {
        case "succeeded":
            showMessage("Payment succeeded!");
            break;
        case "processing":
            showMessage("Your payment is processing.");
            break;
        case "requires_payment_method":
            showMessage("Your payment was not successful, please try again.");
            break;
        default:
            showMessage("Something went wrong.");
            break;
    }
}

// ------- UI helpers -------

function showMessage(messageText) {
    console.log("show messsage:", messageText);
    const messageContainer = document.querySelector("#payment-message");

    messageContainer.classList.remove("hidden");
    messageContainer.textContent = messageText;

    setTimeout(function () {
        messageContainer.classList.add("hidden");
        messageContainer.textContent = "";
    }, 4000);
}

// Show a spinner on payment submission
function setLoading(isLoading) {
    if (isLoading) {
        // Disable the button and show a spinner
        document.querySelector("#submit").classList.add("hidden");
        document.querySelector("#cancel").classList.add("hidden");
        document.querySelector("#spinner").classList.remove("hidden");
        document.querySelector("#button-text").classList.add("hidden");
    } else {
        document.querySelector("#cancel").classList.remove("hidden");
        document.querySelector("#submit").classList.remove("hidden");
        document.querySelector("#spinner").classList.add("hidden");
        document.querySelector("#button-text").classList.remove("hidden");
    }
}