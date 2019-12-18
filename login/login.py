from selenium_wrapper import SeleniumActions
from bs4 import BeautifulSoup
from selenium_wrapper import Xpath_Util
from helper import file_cleanup
from query_model import classify_webpage

xpath_map = {
    "username" : '//input[@id="username"]',
    "password" : '//input[@id="password"]',
    "submit" : "//button[contains(text(),'Sign In')]"
}

required_labels = ["Username", "Password", "Sign In"]

class Login(SeleniumActions):
    def __init__(self, driver):
        super(Login, self).__init__(driver)
        self.xpath_util = Xpath_Util()
        self.generate_xpath_map()

    def login_to_cohesity(self, username, password):
        self.enter_input(self.map["Username"], username)
        self.enter_input(self.map["Password"], password)
        self.click_element(self.map["Sign In"])
        self.wait_for_page_to_load()

    def is_login_page(self):
        path = "model/login/"
        file_cleanup("model/")
        self.take_page_snapshot(path)
        get_web_page_from_classifier = classify_webpage()
        if get_web_page_from_classifier == "Login":
            print "Page is successfully classified as login page"
        else:
            print "Page is classified as {} instead of login page".format(get_web_page_from_classifier)

    def generate_xpath_map(self):
        guessable_elements = ['input', 'button']
        known_attribute_list = ['id', 'name']
        page = self.driver.execute_script("return document.body.innerHTML").encode(
            'utf-8')  # returns the inner HTML as a string
        soup = BeautifulSoup(page, 'html.parser')
        self.map = self.xpath_util.generate_xpath(soup, self.driver, guessable_elements, known_attribute_list, required_labels)
        print "Xpath map generated for login page is {}".format(self.map)




