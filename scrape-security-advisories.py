import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup
import time

# This is not needed if chromedriver is already on your path:
chrome_path = ""
ser = Service(chrome_path)

options = Options()
#options.add_argument("--window-size=1920x1080")
#options.add_argument("--verbose")
options.add_argument("--headless")

driver = webdriver.Chrome(options=options, service=ser)

repoIn = open("clean-package-names.txt", "r")
fo = open("scrape-output.txt", "a")

packageName = repoIn.readline()

while packageName:
    driver.get('https://deps.dev/npm/' + packageName)
    advisoryCount = 0
    timeout = 5
    try:
        WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Security Advisories')]")))
        advisoryDiv = driver.find_element(By.XPATH, "//*[contains(text(), 'Security Advisories')]")
    except Exception:
        pass
    if advisoryDiv is not None:
        try:
            parentDiv = advisoryDiv.find_element(By.XPATH, "..")
            countDiv = parentDiv.find_element(By.XPATH,".//div")
            advisoryCount = countDiv.text
        except Exception:
            pass
    print("{}: {}".format(packageName.strip(), advisoryCount))
    fo.write("\"{}\",{}\n".format(packageName.strip(), advisoryCount))
    packageName = repoIn.readline()
