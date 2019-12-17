from selenium_wrapper import SeleniumActions

xpath_map = {
    "username" : '//*[@id="username"]',
    "password" : '//*[@id="password"]',
    "submit" : '//*[@id="login-btn"]'
}

class Login(SeleniumActions):
    def __init__(self, driver):
        super(Login, self).__init__(driver)

    def login_to_cohesity(self, username, password):
        self.enter_input(xpath_map["username"], username)
        self.enter_input(xpath_map["password"], password)
        self.click_element(xpath_map["submit"])
        self.wait_for_page_to_load()

    def is_login_page(self):
        path = "/tmp/login"
        self.take_page_snapshot(path)
        ## add code here to query the model and verify if the page is login page
        pass




