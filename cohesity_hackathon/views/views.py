from selenium_wrapper import SeleniumActions
from time import sleep

xpath_map = {
    "create_view" : '//*[@id="createView"]',
}

class Views(SeleniumActions):
    def __init__(self, driver):
        super(Views, self).__init__(driver)

    def goto_create_views(self):
        self.click_element(xpath_map["create_view"])
        sleep(5)

    def is_views_page(self):
        path = "/tmp/views"
        self.take_page_snapshot(path)
        ## add code here to query the model and verify if the page is dashboard page
        pass