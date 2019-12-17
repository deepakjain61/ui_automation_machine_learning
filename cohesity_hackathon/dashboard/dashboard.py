from selenium_wrapper import SeleniumActions
from time import sleep
xpath_map = {
    "file_services_link" : '//*[@id="fileServices-nav-anchor"]/cog-nav-item/mat-list-item/div/div[3]/span',
    "views_link" : '//*[@id="views-nav-anchor"]/cog-nav-item/mat-list-item/div/div[3]/span',
}

class Dashboard(SeleniumActions):
    def __init__(self, driver):
        super(Dashboard, self).__init__(driver)

    def goto_views(self):
        self.click_element(xpath_map["file_services_link"])
        sleep(2)
        self.click_element(xpath_map["views_link"])

    def is_dashboard_page(self):
        path = "/tmp/dashboard"
        self.take_page_snapshot(path)
        ## add code here to query the model and verify if the page is dashboard page
        pass