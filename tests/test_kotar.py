from web.kotar_client import KotarClient


def test_first():
    client = KotarClient()
    client.has_tickets("יואב")


test_first()