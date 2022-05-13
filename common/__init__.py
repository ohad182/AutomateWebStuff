import os
from datetime import datetime

APP_NAME = "Automated Stuff"
APP_DATA = 'APPDATA'
# TODO: set the telegram bot token and the chat id
# TELEGRAM Connection based on
# https://pythoncircle.com/post/265/how-to-create-completely-automated-telegram-channel-with-python/
TELEGRAM_TOKEN = None
TELEGRAM_CHAT_ID = None

NEW_DRIVER_DATE = datetime.strptime('2019-12-09', '%Y-%m-%d').date()


def create_temp_folder(notify: bool):
    app_data = os.getenv(APP_DATA)
    if app_data is not None:
        app_data = os.path.join(app_data, APP_NAME)
        try:
            os.makedirs(app_data)
        except:
            pass

    if notify:
        print("App temp directory: {}".format(app_data))
    return app_data


def rreplace(s: str, old: str, new: str, occurences):
    li = s.rsplit(old, occurences)
    return new.join(li)


def change_file_name(filepath, to):
    path, ext = os.path.splitext(filepath)
    filename = os.path.split(path)[-1]
    new_path = rreplace(filepath, filename, to, -1)
    return new_path


def str_to_bool(value: str) -> bool:
    return value.lower() in ["true", "t", "1", "yes""y"]


def try_parse_int(value):
    """
    Attempts to parse the given value to int and return its value, if fails returns original value
    :param value: the value to parse to int
    :return: int representation for value or value
    """
    try:
        return int(value)
    except ValueError:
        return value


class Config(object):
    """
    A class that should handle all app configurations
    """
    ENV = "environment"
    DB_URL = "DB_URL"

    def __init__(self, **kwargs):
        import configparser
        self.read_ok = False
        self.config = configparser.ConfigParser()
        config_path = kwargs.get("config_path", None)
        if config_path is not None:
            self.read(config_path)

    def get(self, section, option, default):
        if not self.read_ok:
            print("No config file found, working with defaults")
            self.read_ok = True
        return try_parse_int(self.config.get(section, option)) if self.config.has_option(section, option) else default

    def read(self, config_file):
        self.read_ok = len(self.config.read(config_file)) > 0
        print("Reading config file: '{}'".format(config_file))

    def expose_env(self):
        if self.config.has_section(Config.ENV):
            exposed_db_url = False
            for var_name in self.config.options(Config.ENV):
                var_name = var_name.upper()
                var_value = self.config.get(Config.ENV, var_name).replace('"', "").replace("'", '')

                if var_name == Config.DB_URL:
                    if not os.path.isabs(var_value):
                        var_value = os.path.abspath(var_value)
                    exposed_db_url = True

                print("Exposing {} - {}: {}".format(Config.ENV, var_name, var_value))

                os.environ[var_name] = var_value

            if not exposed_db_url:
                print("WARNING! DB_URL is not defined")
        else:
            os.environ["DB_URL"] = os.path.abspath("database.db")
            print("Exposing {} - {}: {}".format(Config.ENV, "DB_URL", os.path.abspath("database.db")))


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class AppDir(object, metaclass=Singleton):
    def __init__(self, **kwargs):
        self.app_directory = self.create_app_dir(True)

    def create_app_dir(self, notify: bool):
        app_dir = os.getenv(APP_DATA)
        if app_dir is not None:
            app_dir = os.path.join(app_dir, APP_NAME)
            try:
                os.makedirs(app_dir)
            except:
                pass

        if notify:
            print("App temp directory: {}".format(app_dir))
        return app_dir
