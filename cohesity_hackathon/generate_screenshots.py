from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument("--test-type")
#options.add_argument("--start-maximized")
#options.binary_location = "C:\\MyOwnProject"
driver = webdriver.Chrome(chrome_options=options)

driver.get('https://google.com')
driver.save_screenshot("1.png")

driver.close()