from selenium_wrapper import SeleniumActions

xpath_map = {
    "views_link" : '//*[@id="views-nav-anchor"]/cog-nav-item/mat-list-item/div/div[3]/span',
}

class View(SeleniumActions):
    def __init__(self, driver):
        super(View, self).__init__(driver)

    def go_to_views(self):
        self.click_element(xpath_map["views_link"])


    def is_view_page(self):
        path = "/tmp/views"
        self.take_page_snapshot(path)
        ## add code here to query the model and verify if the page is dashboard page
        pass