import os
import sys
import shutil
import time
import common

import selenium.webdriver.support.ui as ui
from datetime import datetime
from abc import ABC, abstractmethod
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.keys import Keys
from common.hidden_chrome import HiddenChromeWebDriver


class WebClient(ABC):
    def __init__(self, **kwargs):
        self.update_driver_lock = kwargs.get("driver_update_lock", None)
        # self.report_info = report_info
        self.app_temp_directory = common.AppDir().app_directory
        self.chrome_driver_path = self._update_driver(kwargs.get("driver_path", "assets/chromedriver.exe"))
        self.download_time = kwargs.get("download_time", 20)
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-infobars")
        options.add_argument("download.default_directory={}".format(self.app_temp_directory))
        prefs = {'download.default_directory': self.app_temp_directory}
        options.add_experimental_option("prefs", prefs)
        self.ci = common.str_to_bool(os.environ.get("CI", "False"))

        is_headless = common.str_to_bool(os.environ.get("HEADLESS", "False"))  # if specified headless as true, be true
        if is_headless:
            options.add_argument("--headless")
            self.driver = HiddenChromeWebDriver(executable_path=self.chrome_driver_path, options=options)
        else:
            options.add_argument("--start-maximized")
            self.driver = webdriver.Chrome(executable_path=self.chrome_driver_path, options=options)
        self.wait = ui.WebDriverWait(self.driver, 60)

    def _get_table_content(self):
        content = None
        try:
            content = self.driver.execute_script(
                """
var oReq = window.XMLHttpRequest ? new window.XMLHttpRequest() : new ActiveXObject('MSXML2.XMLHTTP.3.0');
if (oReq != null) { 
    oReq.open('GET', $find($find('m_sqlRsWebPart_ctl00_ReportViewer')._internalViewerId).ExportUrlBase+'CSV', false); 
    oReq.send(null);
    if (oReq.status === 200) {
      console.log(oReq.responseText);
      return oReq.responseText;
    }
} 
else { 
    window.console.log('AJAX (XML_HTTP) not supported'); 
} 
                """)
            # print(f"excute result: {stam}")
        except WebDriverException as e:
            # this is ok exception
            pass
        return content

    @abstractmethod
    def get_report_content(self, **kwargs):
        pass

    # def open_url(self, verbose=True):
    #     self.open(self.report_info.url)

    def open(self, url=None):
        self.driver.get(url)

    def close(self):
        self.driver.close()
        self.driver.quit()

    def get_select_options(self, select_id, ignore_options=None):
        if ignore_options is None:
            ignore_options = []
        plain_select = self.driver.find_element(By.ID, select_id)
        select = ui.Select(plain_select)
        options = [x.text for x in select.options if x.text not in ignore_options]
        return options

    def _update_driver(self, driver_relative_path):
        if self.update_driver_lock is not None:
            self.update_driver_lock.acquire(True)
        app_driver_path = os.path.join(self.app_temp_directory, "chromedriver.exe")
        copy_driver = True
        if os.path.exists(app_driver_path) and os.path.isfile(app_driver_path):
            if datetime.fromtimestamp(os.path.getmtime(app_driver_path)).date() >= common.NEW_DRIVER_DATE:
                copy_driver = False
            else:
                print("Chrome driver requires update!")
        if copy_driver:
            chrome_driver = self.get_resource(driver_relative_path)
            shutil.copy(chrome_driver, app_driver_path)
            print("Copied driver to: {}".format(app_driver_path))
        if self.update_driver_lock is not None:
            self.update_driver_lock.release()
        return app_driver_path

    def get_resource(self, relative_path):
        if getattr(sys, 'frozen', False):
            base_path = getattr(sys, "_MEIPASS", None)
        else:
            base_path = os.path.abspath('.')
        print("Base path: {}".format(base_path))
        return os.path.join(base_path, relative_path)

    def load(self):
        pass

    def get_number_of_open_tabs(self):
        return len(self.driver.window_handles)

    def new_tab(self, url=None):
        handles_before = self.get_number_of_open_tabs()
        ex = None
        try:
            if url is None:
                url = ""
            self.driver.execute_script("window.open(\"{}\");".format(url))
        except Exception as e:
            pass
        handles_after = self.get_number_of_open_tabs()
        if handles_before == handles_after and ex is not None:
            raise ex
        self.driver.switch_to.window(self.driver.window_handles[handles_after - 1])
