import sqlalchemy as db
from database.base import Base
from sqlalchemy.orm import relationship


class EventDateTime(Base):
    __tablename__ = "event_date_time"

    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    start_time = db.Column(db.DATETIME)
    end_time = db.Column(db.DATETIME)

    def __str__(self):
        return "בתאריך {} בין השעות {}-{}".format(self.start_time.strftime("%d.%m.%Y"), self.start_time, self.end_time)
        # return "date: {} between {}-{}".format(self.date.strftime("%d.%m.%Y"), self.start_time, self.end_time)


class Event(Base):
    __tablename__ = "event"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    url = db.Column(db.Text)
    time = relationship("EventDateTime", uselist=False)

    def __str__(self):
        url = "<a href=\"{}\">לחץ כאן</a>".format(self.url)
        return "מצאתי כרטיסים ל{}\n{}\nלהזמנת כרטיסים: {}".format(self.name, str(self.time), url)
        # return "Event: {} at {}\n{}".format(self.name, str(self.event_time), self.url)
