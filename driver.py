from selenium import webdriver
from login import Login
from dashboard import Dashboard
from views import Views
from create_view import CreateViews
from view import View
import time

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
url = "https://10.2.157.106/"
driver = webdriver.Chrome("/Users/deepak.jain/cohesity_hackathon/chromedriver", chrome_options=options)





driver.get(url)
driver.maximize_window()
driver.execute_script('return document.readyState;')
time.sleep(10)

login_page = Login(driver)
login_page.is_login_page()
login_page.login_to_cohesity("admin", "admin")
# Verify if we are at login page using classifier

time.sleep(5)
dashboard_page = Dashboard(driver)
# Verify if we are at Dashboard page using classifier
dashboard_page.is_dashboard_page()
dashboard_page.goto_views()
"""
Add code here to query the model and verify if the desired page is loaded
"""
time.sleep(5)
view_dashboard = Views(driver)
view_dashboard.is_views_page()
view_dashboard.goto_create_views()

"""
Add code here to query the model and verify if the desired page is loaded
"""
time.sleep(5)
create_view = CreateViews(driver)
create_view.is_create_views_page()
create_view.create_views("test_hackathon")
"""
Add code here to query the model and verify if the desired page is loaded
"""
time.sleep(5)
view = View(driver)
view.go_to_views()

#validate views




