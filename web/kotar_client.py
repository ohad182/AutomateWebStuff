import time
from web import WebClient
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys


def get_events_names(events):
    events_names = []
    for event in events:
        header = event.find_element(By.TAG_NAME, 'h2')
        if header is not None:
            events_names.append(header.text)
        else:
            print("Error! cannot find event name for {}".format(str(event)))

    return events_names


class KotarClient(WebClient):

    def get_report_content(self, **kwargs):
        pass

    def __init__(self, **kwargs):
        super(KotarClient, self).__init__(**kwargs)
        self.url = "https://www.kotar-rishon-lezion.org.il/events-category/%D7%90%D7%99%D7%A8%D7%95%D7%A2%D7%99%D7%9D-%D7%95%D7%A4%D7%A2%D7%99%D7%9C%D7%99%D7%95%D7%AA/%D7%9B%D7%95%D7%AA%D7%A8-%D7%98%D7%A3-%D7%94%D7%A6%D7%92%D7%95%D7%AA/"

    def has_tickets(self, event_name_part):
        sold_out = True
        try:
            self.open(self.url)
            attempts = 1
            max_attempts = 200000
            while sold_out and attempts < max_attempts:
                print("Checking for tickets #{}".format(attempts))
                events = self.driver.find_elements(By.CLASS_NAME, 'event-inner')
                print("Found {} events".format(len(events)))
                events_names = get_events_names(events)

                for event_name in events_names:
                    if "אזלו" not in event_name:
                        print("Tickets available for {}".format(event_name))
                        if event_name_part in event_name:
                            sold_out = False
                            print("Event '{}' found".format(event_name_part))
                            break
                if sold_out:
                    print("Waiting for 10 seconds")
                    attempts = attempts + 1
                    time.sleep(10)
                    self.driver.refresh()
            if not sold_out:
                self.new_tab('https://youtu.be/QB8NuvDML2I?t=60')
                time.sleep(30)
        except Exception as ex:
            print("Error! {}".format(str(ex)))
            time.sleep(5)
            raise ex
        finally:
            self.close()
        return sold_out
