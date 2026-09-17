const API_URL = "http://127.0.0.1:5000";


// =================================
// GET ALL EVENTS
// =================================

async function loadEvents() {

    try {

        const response = await fetch(`${API_URL}/api/events`);

        const events = await response.json();

        const container = document.getElementById("events");

        container.innerHTML = "";

        if (events.length === 0) {

            container.innerHTML = "<p>No events yet.</p>";

            return;
        }


        events.forEach(event => {

            container.innerHTML += `
                <div class="event">

                    <h3>${event.title}</h3>

                    <p>
                        <strong>Club:</strong>
                        ${event.club}
                    </p>

                    <p>
                        <strong>Date:</strong>
                        ${event.date}
                    </p>

                    <p>
                        <strong>Venue:</strong>
                        ${event.venue}
                    </p>

                    <p>
                        ${event.description}
                    </p>

                    <p>
                        <strong>Registrations:</strong>
                        ${event.registrations}
                    </p>

                    <button onclick="registerEvent(${event.id})">
                        Register
                    </button>

                </div>
            `;
        });

    } catch (error) {

        console.log(error);

        document.getElementById("events").innerHTML =
            "<p>Could not connect to the server.</p>";
    }
}


// =================================
// CREATE EVENT
// =================================

async function submitEvent() {

    const event = {

        title: document.getElementById("title").value,

        club: document.getElementById("club").value,

        date: document.getElementById("date").value,

        venue: document.getElementById("venue").value,

        description: document.getElementById("description").value
    };


    // Check if fields are empty

    if (
        event.title === "" ||
        event.club === "" ||
        event.date === "" ||
        event.venue === ""
    ) {

        alert("Please fill all required fields.");

        return;
    }


    try {

        const response = await fetch(
            `${API_URL}/api/events`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(event)
            }
        );


        if (response.ok) {

            alert("Event created successfully!");

            // Clear form

            document.getElementById("title").value = "";
            document.getElementById("club").value = "";
            document.getElementById("date").value = "";
            document.getElementById("venue").value = "";
            document.getElementById("description").value = "";


            // Reload events

            loadEvents();

        } else {

            alert("Could not create event.");

        }

    } catch (error) {

        console.log(error);

        alert("Could not connect to Flask server.");

    }
}


// =================================
// REGISTER
// =================================

async function registerEvent(id) {

    try {

        const response = await fetch(
            `${API_URL}/api/events/${id}/register`,
            {
                method: "POST"
            }
        );


        if (response.ok) {

            alert("Registration successful!");

            loadEvents();

        } else {

            alert("Registration failed.");

        }

    } catch (error) {

        console.log(error);

        alert("Could not connect to server.");

    }
}


// =================================
// LOAD EVENTS WHEN PAGE OPENS
// =================================

loadEvents();v
