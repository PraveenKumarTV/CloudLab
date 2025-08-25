from flask import Flask, request, jsonify, render_template_string
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

MONGO_URI = "mongodb+srv://praveenkumartv1:praveen123@praveendb.ac0h0.mongodb.net/?"
client = MongoClient(MONGO_URI)
db = client["test"]
events_collection = db["Events"]

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Event Manager</title>
  <link
    href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"
    rel="stylesheet"
  />
  <style>
    body {
  background-image: url('{{ url_for('static', filename='images1.jpg') }}');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  background-attachment: fixed;
  color: #fff; /* make text readable if image is dark */
}

/* Optional: add a semi-transparent overlay to improve readability */
.container {
  background-color: rgba(0, 0, 0, 0.45);
  padding: 20px;
  border-radius: 8px;
}

  </style>
</head>
<body>
  <div class="container mt-5">
    <h2>Event Manager</h2>
    
    <h4>Create Event</h4>
    <form id="eventForm" class="mb-4">
      <div class="row g-3">
        <div class="col-md-4">
          <input type="text" id="eventName" class="form-control" placeholder="Event Name" required />
        </div>
        <div class="col-md-2">
          <input type="date" id="eventDate" class="form-control" required />
        </div>
        <div class="col-md-2">
          <input type="time" id="eventTime" class="form-control" required />
        </div>
        <div class="col-md-2">
          <input type="text" id="eventLocation" class="form-control" placeholder="Location" required />
        </div>
        <div class="col-md-8 mt-3">
          <textarea id="eventDescription" class="form-control" rows="2" placeholder="Description" required></textarea>
        </div>
        <div class="col-md-2 mt-3">
          <button type="submit" class="btn btn-primary w-100">Create</button>
        </div>
      </div>
    </form>
    
    <h4>Events List</h4>
    <table class="table table-bordered" id="eventsTable">
      <thead>
        <tr>
          <th>Name</th>
          <th>Date</th>
          <th>Time</th>
          <th>Location</th>
          <th>Description</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody id="eventsBody">
        <!-- Events will be loaded here -->
      </tbody>
    </table>
  </div>

<script>
  async function fetchEvents() {
    const res = await fetch('/events');
    const events = await res.json();
    const tbody = document.getElementById('eventsBody');
    tbody.innerHTML = '';
    events.forEach(event => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td><input class="form-control" value="${event.eventName}" id="name-${event._id}" /></td>
        <td><input type="date" class="form-control" value="${event.eventDate}" id="date-${event._id}" /></td>
        <td><input type="time" class="form-control" value="${event.eventTime}" id="time-${event._id}" /></td>
        <td><input class="form-control" value="${event.eventLocation}" id="location-${event._id}" /></td>
        <td><textarea class="form-control" id="desc-${event._id}">${event.eventDescription}</textarea></td>
        <td>
          <button class="btn btn-success btn-sm mb-1" onclick="updateEvent('${event._id}')">Update</button>
          <button class="btn btn-danger btn-sm" onclick="deleteEvent('${event._id}')">Delete</button>
        </td>
      `;
      tbody.appendChild(tr);
    });
  }

  async function updateEvent(id) {
    const data = {
      eventName: document.getElementById(`name-${id}`).value,
      eventDate: document.getElementById(`date-${id}`).value,
      eventTime: document.getElementById(`time-${id}`).value,
      eventLocation: document.getElementById(`location-${id}`).value,
      eventDescription: document.getElementById(`desc-${id}`).value,
    };
    const res = await fetch(`/events/${id}`, {
      method: 'PUT',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(data),
    });
    if(res.ok){
      alert('Event updated');
      fetchEvents();
    } else {
      alert('Update failed');
    }
  }

  async function deleteEvent(id) {
    if(confirm('Are you sure you want to delete this event?')){
      const res = await fetch(`/events/${id}`, {method: 'DELETE'});
      if(res.ok){
        alert('Event deleted');
        fetchEvents();
      } else {
        alert('Delete failed');
      }
    }
  }

  document.getElementById('eventForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const data = {
      eventName: document.getElementById('eventName').value,
      eventDate: document.getElementById('eventDate').value,
      eventTime: document.getElementById('eventTime').value,
      eventLocation: document.getElementById('eventLocation').value,
      eventDescription: document.getElementById('eventDescription').value,
    };
    const res = await fetch('/create-event', {
      method: 'POST',
      headers: {'Content-Type': 'application/x-www-form-urlencoded'},
      body: new URLSearchParams(data),
    });
    if(res.ok){
      alert('Event created');
      e.target.reset();
      fetchEvents();
    } else {
      alert('Create failed');
    }
  });

  // Load events when page loads
  fetchEvents();
</script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_PAGE)


@app.route('/create-event', methods=['POST'])
def create_event():
    event_data = {
        "eventName": request.form.get("eventName"),
        "eventDate": request.form.get("eventDate"),
        "eventTime": request.form.get("eventTime"),
        "eventLocation": request.form.get("eventLocation"),
        "eventDescription": request.form.get("eventDescription"),
    }
    result = events_collection.insert_one(event_data)
    return jsonify({"message": "Event created", "id": str(result.inserted_id)}), 201


@app.route('/events', methods=['GET'])
def get_events():
    events = list(events_collection.find())
    for event in events:
        event["_id"] = str(event["_id"])
    return jsonify(events)


@app.route('/events/<id>', methods=['PUT'])
def update_event(id):
    data = request.json
    update_data = {k: v for k, v in data.items()}
    result = events_collection.update_one({"_id": ObjectId(id)}, {"$set": update_data})
    if result.matched_count:
        return jsonify({"message": "Event updated"})
    else:
        return jsonify({"message": "Event not found"}), 404


@app.route('/events/<id>', methods=['DELETE'])
def delete_event(id):
    result = events_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count:
        return jsonify({"message": "Event deleted"})
    else:
        return jsonify({"message": "Event not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
