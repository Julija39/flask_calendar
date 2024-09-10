from flask import Flask, request, jsonify
import datetime

app = Flask(__name__)

class Event:
    def __init__(self, id, date, title, text):
        self.id = id
        self.date = date
        self.title = title
        self.text = text

class EventLogic:
    def __init__(self):
        self.events = []
        self.next_id = 1

    def create(self, event):
        if any(e.date == event.date for e in self.events):
            raise ValueError("Event already exists for this date")
        event.id = self.next_id
        self.next_id += 1
        self.events.append(event)
        return event.id

    def list(self):
        return self.events

    def read(self, event_id):
        for event in self.events:
            if event.id == event_id:
                return event
        raise ValueError("Event not found")

    def update(self, event_id, updated_event):
        for i, event in enumerate(self.events):
            if event.id == event_id:
                self.events[i] = updated_event
                return
        raise ValueError("Event not found")

    def delete(self, event_id):
        for i, event in enumerate(self.events):
            if event.id == event_id:
                del self.events[i]
                return
        raise ValueError("Event not found")

_event_logic = EventLogic()

def validate_event_data(data):
    try:
        date, title, text = data.split('|')
        date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        if len(title) > 30 or len(text) > 200:
            raise ValueError("Invalid data length")
        return date, title, text
    except ValueError:
        raise ValueError("Invalid data format")

API_ROOT = "/api/v1"
CALENDAR_API_ROOT = API_ROOT + "/calendar"

@app.route(CALENDAR_API_ROOT + "/", methods=["POST"])
def create_event():
    try:
        data = request.get_data().decode('utf-8')
        date, title, text = validate_event_data(data)
        event = Event(None, date, title, text)
        event_id = _event_logic.create(event)
        return jsonify({'id': event_id}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@app.route(CALENDAR_API_ROOT + "/", methods=["GET"])
def list_events():
    events = _event_logic.list()
    return jsonify([event.__dict__ for event in events])

@app.route(CALENDAR_API_ROOT + "/<int:event_id>", methods=["GET"])
def read_event(event_id):
    try:
        event = _event_logic.read(event_id)
        return jsonify(event.__dict__)
    except ValueError as e:
        return jsonify({'error': str(e)}), 404

@app.route(CALENDAR_API_ROOT + "/<int:event_id>", methods=["PUT"])
def update_event(event_id):
    try:
        data = request.get_data().decode('utf-8')
        date, title, text = validate_event_data(data)
        updated_event = Event(event_id, date, title, text)
        _event_logic.update(event_id, updated_event)
        return jsonify({'message': 'Event updated'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@app.route(CALENDAR_API_ROOT + "/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    try:
        _event_logic.delete(event_id)
        return jsonify({'message': 'Event deleted'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404

if __name__ == '__main__':
    app.run(debug=True)