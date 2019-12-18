from selenium import webdriver
from bs4 import BeautifulSoup

class Xpath_Util:
    def __init__(self):
        self.elements = None

    def generate_xpath(self, soup, driver, guessable_elements, known_attribute_list, required_labels):
        "generate the xpath"
        map = {}
        try:
            for guessable_element in guessable_elements:
                self.elements = soup.find_all(guessable_element)
                for element in self.elements:
                    if (not element.has_attr("type")) or (element.has_attr("type")):
                        for attr in known_attribute_list:
                            if element.has_attr(attr):
                                locator = self.guess_xpath(guessable_element, attr, element)
                                if len(driver.find_elements_by_xpath(locator)) == 1:

                                    new_lc = locator.encode('utf-8') + "/preceding-sibling::label[position() < 2]"
                                    try:
                                        dr = driver.find_element_by_xpath(new_lc)
                                        if dr.text in required_labels:
                                            map[dr.text] = locator.encode('utf-8')
                                    except Exception as e:
                                        if "no such element" in str(e):
                                            continue
                                    break
                            elif guessable_element in ('button', "span") and element.getText():
                                button_text = element.getText()
                                if button_text.strip() in required_labels:
                                    if element.getText() == button_text.strip():
                                        locator = self.guess_xpath_button(guessable_element, "text()",
                                                                               element.getText())
                                    else:
                                        locator = self.guess_xpath_using_contains(guessable_element, "text()",
                                                                                       button_text.strip())
                                else:
                                    continue
                                if len(driver.find_elements_by_xpath(locator)) == 1:
                                    map[button_text.strip()] = locator.encode('utf-8')
                                    break
        except Exception, e:
            print ("Exception when trying to generate xpath for:%s" % guessable_element)
            print ("Python says:%s" % str(e))
        return map

    def guess_xpath(self, tag, attr, element):
        "Guess the xpath based on the tag,attr,element[attr]"
        # Class attribute returned as a unicodeded list, so removing 'u from the list and joining back
        if type(element[attr]) is list:
            element[attr] = [i.encode('utf-8') for i in element[attr]]
            element[attr] = ' '.join(element[attr])
        self.xpath = "//%s[@%s='%s']" % (tag, attr, element[attr])

        return self.xpath

    def guess_xpath_button(self, tag, attr, element):
        "Guess the xpath for button tag"
        self.button_xpath = "//%s[%s='%s']" % (tag, attr, element)

        return self.button_xpath

    def guess_xpath_using_contains(self, tag, attr, element):
        "Guess the xpath using contains function"
        self.button_contains_xpath = "//%s[contains(%s,'%s')]" % (tag, attr, element)

        return self.button_contains_xpath

# -------START OF SCRIPT--------
if __name__ == "__main__":
    print ("Start of %s" % __file__)

    # Initialize the xpath object
    xpath_obj = Xpath_Util()
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    # Get the URL and parse
    #url = input("Enter URL: ")
    url = "https://10.2.37.237/"
    # Create a chrome session
    driver = webdriver.Chrome("/Users/deepak.jain/cohesity_hackathon/chromedriver", chrome_options=options)
    driver.get(url)
    driver.execute_script('return document.readyState;')
    import time
    time.sleep(10)

    # Parsing the HTML page with BeautifulSoup
    page = driver.execute_script("return document.body.innerHTML").encode('utf-8')  # returns the inner HTML as a string
    soup = BeautifulSoup(page, 'html.parser')

    # execute generate_xpath
    if xpath_obj.generate_xpath(soup, driver) is False:
        print ("No XPaths generated for the URL:%s" % url)
    driver.quit()