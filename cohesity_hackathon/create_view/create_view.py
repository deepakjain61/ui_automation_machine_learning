from selenium_wrapper import SeleniumActions
import time

xpath_map = {
    "view_name" : '//*[@id="view-name-input"]',
    "create_view_button" : '//*[@id="update-or-create-view-button"]'
}

class CreateViews(SeleniumActions):
    def __init__(self, driver):
        super(CreateViews, self).__init__(driver)

    def create_views(self, view_name):
        self.enter_input(xpath_map["view_name"], view_name)
        time.sleep(5)
        self.scroll_down_to_bottom(xpath_map["create_view_button"])
        self.click_element(xpath_map["create_view_button"])

    def is_views_page(self):
        path = "/tmp/views"
        self.take_page_snapshot(path)
        ## add code here to query the model and verify if the page is dashboard page
        pass