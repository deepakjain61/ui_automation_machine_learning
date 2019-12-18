from selenium_wrapper import SeleniumActions
from time import sleep
from bs4 import BeautifulSoup
from selenium_wrapper import Xpath_Util
from helper import file_cleanup
from query_model import classify_webpage

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
        path = "model/dashboard/"
        file_cleanup("model/")
        self.take_page_snapshot(path)
        get_web_page_from_classifier = classify_webpage()
        if get_web_page_from_classifier == "Dashboard":
            print "Page is successfully classified as Dashboard page"
        else:
            print "Page is classified as {} instead of Dashboard page".format(get_web_page_from_classifier)

    def generate_xpath_map(self):
        guessable_elements = ['input', 'button', 'span']
        known_attribute_list = ['id', 'name']
        page = self.driver.execute_script("return document.body.innerHTML").encode(
            'utf-8')  # returns the inner HTML as a string
        soup = BeautifulSoup(page, 'html.parser')
        self.map = self.xpath_util.generate_xpath(soup, self.driver, guessable_elements, known_attribute_list, required_labels)
        print "Xpath map generated for dashboard page is {}".format(self.map)