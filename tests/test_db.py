from datetime import datetime
from database.models import Event, EventDateTime
from database.base import create_all, Session

create_all()
session = Session()

event_name = 'מפוחית וגיטרה עם יואב'
url = 'https://www.kotar-rishon-lezion.org.il/events-category/%D7%90%D7%99%D7%A8%D7%95%D7%A2%D7%99%D7%9D-%D7%95%D7%A4%D7%A2%D7%99%D7%9C%D7%99%D7%95%D7%AA/%D7%9B%D7%95%D7%AA%D7%A8-%D7%98%D7%A3-%D7%94%D7%A6%D7%92%D7%95%D7%AA/'
start = datetime.strptime("2022-05-30 17:00:00", "%Y-%m-%d %H:%M:%S")
end = datetime.strptime("2022-05-30 18:30:00", "%Y-%m-%d %H:%M:%S")
event_time = EventDateTime(start_time=start, end_time=end)
relevant_events = session.query(Event).filter(Event.name == event_name, Event.url == url)
this_event = next((x for x in relevant_events if x.time.start_time == start and x.time.end_time == end), None)
print("done")
