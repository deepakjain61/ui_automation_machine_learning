from selenium_wrapper import SeleniumActions
from time import sleep
from bs4 import BeautifulSoup
from selenium_wrapper import Xpath_Util

required_labels = ["File Services", "Views"]

class Dashboard(SeleniumActions):
    def __init__(self, driver):
        super(Dashboard, self).__init__(driver)
        self.xpath_util = Xpath_Util()
        self.generate_xpath_map()

    def goto_views(self):
        self.click_element(self.map["File Services"])
        sleep(2)
        self.generate_xpath_map()
        self.click_element(self.map["Views"])

    def is_dashboard_page(self):
        path = "/tmp/dashboard"
        self.take_page_snapshot(path)
        ## add code here to query the model and verify if the page is dashboard page
        pass

    def generate_xpath_map(self):
        guessable_elements = ['input', 'button', 'span']
        known_attribute_list = ['id', 'name']
        page = self.driver.execute_script("return document.body.innerHTML").encode(
            'utf-8')  # returns the inner HTML as a string
        soup = BeautifulSoup(page, 'html.parser')
        self.map = self.xpath_util.generate_xpath(soup, self.driver, guessable_elements, known_attribute_list, required_labels)
        print "Xpath map generated for dashboard page is {}".format(self.map)