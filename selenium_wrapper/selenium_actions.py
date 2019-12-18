from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from distutils.dir_util import mkpath
import time

class SeleniumActions(object):
    def __init__(self, driver):
        self.driver = driver

    def enter_input(self, xpath, value):
        input = self.driver.find_element_by_xpath(xpath)
        input.send_keys(value)

    def click_element(self, xpath):
        self.driver.find_element_by_xpath(xpath).click()

    def wait_for_page_to_load(self):
        current_url = self.driver.current_url
        WebDriverWait(self.driver, 15).until(EC.url_changes(current_url))

    def scroll_down_to_bottom(self, path):
        jsScript = """
                function move_up(element) {
                    element.scrollTop = element.scrollTop - 1000;
                }

                function move_down(element) {
                    element.scrollTop = element.scrollTop + 1000;
                }

                move_down(arguments[0]);
                move_down(arguments[0]);
                """
        centerPanel = self.driver.find_element_by_xpath(path)
        self.driver.execute_script(jsScript, centerPanel)

    def take_page_snapshot(self, path):
        if not os.path.exists(path):
            #mkpath(path)
            os.makedirs(path)

        print "taking snapshot at path {}".format(path)
        path = path + "test.png"
        self.driver.save_screenshot(path)
        time.sleep(2)


