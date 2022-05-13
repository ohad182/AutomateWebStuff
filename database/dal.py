import traceback

from database.base import Session
from database.models import Event


def event_exists(event):
    session = Session()
    existing_event = None
    try:
        relevant_events = session.query(Event).filter(Event.name == event.name, Event.url == event.url)
        existing_event = next((x for x in relevant_events if
                               x.time.start_time == event.time.start_time and
                               x.time.end_time == event.time.end_time),
                              None)
    except Exception as e:
        print("Failed to check event exist {} --- {}".format(str(event), traceback.print_exc()))
    finally:
        session.close()
    return existing_event is not None


def add_event(event):
    session = Session()
    try:
        session.add(event)
        session.commit()
    except Exception as e:
        print("Failed to add event {} --- {}".format(str(event), traceback.print_exc()))
    finally:
        session.close()
