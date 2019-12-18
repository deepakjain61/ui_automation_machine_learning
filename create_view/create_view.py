from selenium_wrapper import SeleniumActions
import time
from bs4 import BeautifulSoup
from selenium_wrapper import Xpath_Util
from helper import file_cleanup
from query_model import classify_webpage


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

    def is_create_views_page(self):
        path = "model/create_views/"
        file_cleanup("model/")
        self.take_page_snapshot(path)
        get_web_page_from_classifier = classify_webpage()
        if get_web_page_from_classifier == "Create Views":
            print "Page is successfully classified as Create Views page"
        else:
            print "Page is classified as {} instead of Create Views page".format(get_web_page_from_classifier)

    def generate_xpath_map(self):
        guessable_elements = ['input', 'button']
        known_attribute_list = ['id', 'name', 'text']
        page = self.driver.execute_script("return document.body.innerHTML").encode(
            'utf-8')  # returns the inner HTML as a string
        soup = BeautifulSoup(page, 'html.parser')
        self.map = self.xpath_util.generate_xpath(soup, self.driver, guessable_elements, known_attribute_list, required_labels)
        print "Xpath map generated for create view page is {}".format(self.map)