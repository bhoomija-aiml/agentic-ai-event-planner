
// Get HTML elements
const eventForm = document.getElementById("eventForm");
const eventList = document.getElementById("eventList");

const totalEvents = document.getElementById("totalEvents");
const upcomingEvents = document.getElementById("upcomingEvents");
const totalBudget = document.getElementById("totalBudget");

// Load previously saved events
let events = JSON.parse(localStorage.getItem("eventOrbitEvents")) || [];

// Save events in browser storage
function saveEvents() {
    localStorage.setItem("eventOrbitEvents", JSON.stringify(events));
}

// Format budget
function formatBudget(amount) {
    return "₹" + Number(amount).toLocaleString("en-IN");
}

// Update dashboard statistics
function updateDashboard() {
    totalEvents.textContent = events.length;

    const today = new Date().toISOString().split("T")[0];

    const upcoming = events.filter(function(event) {
        return event.date >= today;
    });

    upcomingEvents.textContent = upcoming.length;

    const budget = events.reduce(function(total, event) {
        return total + Number(event.budget);
    }, 0);

    totalBudget.textContent = formatBudget(budget);
}

// Display all events
function displayEvents() {
    eventList.innerHTML = "";

    if (events.length === 0) {
        eventList.innerHTML = `
            <p class="empty-message">
                No events created yet. Start by creating your first event!
            </p>
        `;
        updateDashboard();
        return;
    }

    events.forEach(function(event) {
        const eventCard = document.createElement("div");
        eventCard.className = "event-item";

        const details = document.createElement("div");

        const title = document.createElement("h3");
        title.textContent = event.name;

        const type = document.createElement("p");
        type.textContent = "Type: " + event.type;

        const date = document.createElement("p");
        date.textContent = "Date: " + event.date;

        const location = document.createElement("p");
        location.textContent = "Location: " + event.location;

        const guests = document.createElement("p");
        guests.textContent = "Expected Guests: " + event.guests;

        const budget = document.createElement("p");
        budget.textContent = "Budget: " + formatBudget(event.budget);

        details.append(title, type, date, location, guests, budget);

        const deleteButton = document.createElement("button");
        deleteButton.className = "delete-btn";
        deleteButton.textContent = "Delete";

        deleteButton.addEventListener("click", function() {
            deleteEvent(event.id);
        });

        eventCard.append(details, deleteButton);
        eventList.appendChild(eventCard);
    });

    updateDashboard();
}

// Create a new event
eventForm.addEventListener("submit", function(e) {
    e.preventDefault();

    const newEvent = {
        id: Date.now(),
        name: document.getElementById("eventName").value.trim(),
        type: document.getElementById("eventType").value,
        date: document.getElementById("eventDate").value,
        location: document.getElementById("eventLocation").value.trim(),
        guests: Number(document.getElementById("attendees").value),
        budget: Number(document.getElementById("eventBudget").value)
    };

    if (
        !newEvent.name ||
        !newEvent.type ||
        !newEvent.date ||
        !newEvent.location ||
        newEvent.guests < 1 ||
        newEvent.budget < 0
    ) {
        alert("Please enter valid event details.");
        return;
    }

    events.push(newEvent);

    saveEvents();
    displayEvents();

    eventForm.reset();

    alert("Event created successfully!");
});

// Delete an event
function deleteEvent(id) {
    const confirmDelete = confirm("Are you sure you want to delete this event?");

    if (confirmDelete) {
        events = events.filter(function(event) {
            return event.id !== id;
        });

        saveEvents();
        displayEvents();
    }
}

// AI planner placeholder
document.getElementById("aiPlannerBtn").addEventListener("click", function() {
    alert("AI Event Planner integration will be added after connecting the FastAPI backend.");
});

// Show saved events when the page loads
displayEvents();
