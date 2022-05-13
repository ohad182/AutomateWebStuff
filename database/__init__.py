# should implement high level db init sequence

def abort_flush(*args, **kwargs):
    """
    The terrible consequences for trying to flush the database
    """
    print("Called abort_flush")
    return


class Database(object):
    def __init__(self, **kwargs):
        self.session = None
        self.url = None

    def _get_alchemy(self):
        pass

    def _get_sqlite(self):
        pass
