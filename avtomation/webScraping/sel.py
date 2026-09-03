from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

options = Options()
options.binary_location = "/usr/bin/firefox"
browser = Firefox(options=options)

browser.get("http://inventwithpython.com")

try:
    elem = browser.find_element("class name", "bookcover")
    print("Found <%s> element with that calss name!" % (elem.tag_name))
except:
    print("Was not able to find element with that name")
