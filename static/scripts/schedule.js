var selectedCells = [];

function toggleSelect(cell, slot, court, date, isBooked, price) {
    console.log("clicked")
    var today = new Date().toISOString().split('T')[0];
    if (date < today) {
        console.log("date:", date)
        console.log("today:", today)
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
// This is your test publishable API key.
const stripe = Stripe("pk_test_51PfA0tRt3PcgmiF6YXj4ROeapnBMPBd7FqSIGJyGvvMoZrVESulq4n0kTbarADCXxDjQQShUD3GbsaKaustZJut400GUgtILbz");

//TODO
// The items the customer wants to buy
const items = [{ id: "xl-tshirt" }];

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
        },
        body: JSON.stringify({ items }),
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
    //initialize();

     // Collect selected slot data
    var slots = selectedCells.map(c => c.split('_'));
    const firstName = document.getElementById('first_name').value;
    const lastName = document.getElementById('last_name').value;
    const email = document.getElementById('email').value;
    const phone = document.getElementById('phone').value;
    var total = slots.map(s => parseFloat(s[3])).reduce((sum, value) => sum + value, 0);


    console.log("[handleSubmit] selectedSlots: ", slots)
    console.log("[handleSubmit] firstName: ", firstName)
    console.log("[handleSubmit] lastName: ", lastName)
    console.log("[handleSubmit] email: ", email)
    console.log("[handleSubmit] phone: ", phone)
    console.log("[handleSubmit] total: ", total)

    setLoading(true);

    // TODO verify if email exists in db
    // 1) exists: then verify if firstname and lastname match record
    // if it doens't match, prompts an error msg
    // 2) not exists: continue

    // Update PaymentIntent with metadata
    const updateResponse = await fetch('/update_payment_intent/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            payment_intent_id: clientSecret.split('_secret')[0], // Extract payment intent ID from client secret
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
        console.log("error here in update")
        console.error(updateResult.error);
        showMessage(updateResult.error);
        setLoading(false);
        return;
    }

     const { error } = await stripe.confirmPayment({
        elements,
        confirmParams: {
            return_url: 'http://localhost:8000/payment_success', //TODO
            // Make sure to change this to your payment completion page
            receipt_email: email
        },

    });


    // This point will only be reached if there is an immediate error when
    // confirming the payment. Otherwise, your customer will be redirected to
    // your `return_url`. For some payment methods like iDEAL, your customer will
    // be redirected to an intermediate site first to authorize the payment, then
    // redirected to the `return_url`.
    if (error.type === "card_error" || error.type === "validation_error") {
        console.log("error here?")
        showMessage(error.message);
    } else {
        console.log("error here on payment")
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
        document.querySelector("#submit").disabled = true;
        document.querySelector("#spinner").classList.remove("hidden");
        document.querySelector("#button-text").classList.add("hidden");
    } else {
        document.querySelector("#submit").disabled = false;
        document.querySelector("#spinner").classList.add("hidden");
        document.querySelector("#button-text").classList.remove("hidden");
    }
}