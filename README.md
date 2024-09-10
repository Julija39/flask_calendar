# flask_calendar
#Running the Application
export FLASK_APP=app.py  # On Windows: set FLASK_APP=app.py
flask run

#Testing the API using cURL

#1. Create a new event
curl http://127.0.0.1:5000/api/v1/calendar/ -X POST -H "Content-Type: text/plain" -d "2024-09-15|Meeting|Monthly status meeting"

#2. Get a list of events
curl http://127.0.0.1:5000/api/v1/calendar/ -X GET

#3. Get an event by ID
curl http://127.0.0.1:5000/api/v1/calendar/1 -X GET

#4. Update an event
curl http://127.0.0.1:5000/api/v1/calendar/1 -X PUT -H "Content-Type: text/plain" -d "2024-09-16|Updated Meeting|New agenda for the meeting"

#5. Delete an event
curl http://127.0.0.1:5000/api/v1/calendar/1 -X DELETE
