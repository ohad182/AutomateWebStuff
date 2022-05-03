from datetime import datetime


class EventDateTime(object):
    def __init__(self, **kwargs):
        self.date: datetime = kwargs.get("date", None)
        self.start_time = kwargs.get("start_time", None)
        self.end_time = kwargs.get("end_time", None)

    def __str__(self):
        return "date: {} between {}-{}".format(self.date.strftime("%d.%m.%Y"), self.start_time, self.end_time)


class Event(object):
    def __init__(self, **kwargs):
        self.name = kwargs.get("name", None)
        self.event_time = kwargs.get("event_time", None)
        self.url = kwargs.get("url", None)

    def __str__(self):
        return "Event: {} at {}\n{}".format(self.name, str(self.event_time), self.url)
