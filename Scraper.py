import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import undetected_chromedriver as uc

def Clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

class Scraper:
    def __init__(self):
        Clear()
        self.chrome_options = webdriver.ChromeOptions()
        self.driver = uc.Chrome(options=self.chrome_options)
        self.wait = WebDriverWait(self.driver, 20)
        Clear()
    
    def ClickElement(self, xpath):
        try:
            element = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            element.click()

        except Exception:
            self.driver.execute_script("arguments[0].click()", element)

    def LocateElement(self, xpath):
        try:
            element = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath)))
            element = element[0].get_attribute('innerHTML')
            element = BeautifulSoup(element, features="lxml")
            element = element.text
            return element
        except Exception: 
            print("\nCould not locate element\n")
            return ""

    def Send_keysElement(self, xpath, text):
        try:
            element = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            element.send_keys(text)

        except Exception as e:
            print("Couldn't send keys")
            print(e)
    
    def OpenPage(self, url):
        self.driver.get(url)