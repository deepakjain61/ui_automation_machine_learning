from selenium_wrapper import SeleniumActions
import time
from bs4 import BeautifulSoup
from selenium_wrapper import Xpath_Util

required_labels = ["View Name", "Create View"]

class CreateViews(SeleniumActions):
    def __init__(self, driver):
        super(CreateViews, self).__init__(driver)
        self.xpath_util = Xpath_Util()
        self.generate_xpath_map()

    def create_views(self, view_name):
        self.enter_input('//*[@id="view-name-input"]', view_name)
        time.sleep(2)
        self.generate_xpath_map()
        self.scroll_down_to_bottom(self.map["Create View"])
        self.click_element(self.map["Create View"])

    def is_views_page(self):
        path = "/tmp/views"
        self.take_page_snapshot(path)
        ## add code here to query the model and verify if the page is dashboard page
        pass

    def generate_xpath_map(self):
        guessable_elements = ['input', 'button']
        known_attribute_list = ['id', 'name', 'text']
        page = self.driver.execute_script("return document.body.innerHTML").encode(
            'utf-8')  # returns the inner HTML as a string
        soup = BeautifulSoup(page, 'html.parser')
        self.map = self.xpath_util.generate_xpath(soup, self.driver, guessable_elements, known_attribute_list, required_labels)
        print "Xpath map generated for create view page is {}".format(self.map)