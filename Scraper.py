import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from selenium.webdriver.common.keys import Keys

def Clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

class Scraper:
    """
    A web scraper class powered by Selenium and Undetected ChromeDriver.

    Provides utility methods for navigating pages, interacting with elements, and extracting content.
    """
    def __init__(self):
        Clear()
        self.chrome_options = webdriver.ChromeOptions()
        self.driver = uc.Chrome(options=self.chrome_options)
        self.wait = WebDriverWait(self.driver, 20)
        self.keys = Keys
        Clear()
    
    def ClickElement(self, xpath):
        """
        Parameters:
            xpath (str): XPath to element
        
        Clicks on an element specified by an XPath.
        """
        try:
            element = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            element.click()
        except Exception:
            try:
                element = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
                self.driver.execute_script("arguments[0].click()", element)
            except Exception as e:
                print(f"Error clicking element for XPath '{xpath}': {e}")

    def LocateElement(self, xpath):
        """
        Parameters:
            xpath (str): XPath to element

        Finds the first element matching the XPath and returns the extracted text.
        Returns an empty string if the element is not found or parsing fails.
        """
        try:
            elements = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath)))
            html_content = elements[0].get_attribute('innerHTML')
            soup = BeautifulSoup(html_content, features="lxml")
            return soup.get_text()
        except Exception as e:
            print(f"Could not locate or parse element with XPath '{xpath}': {e}")
            return ""

    def Send_keysElement(self, xpath, *values):
        """
        Parameters:
            xpath (str): XPath to element
            *values: sequence of strings or Keys constants to send
        
        Sends the specified sequence of values (text and/or special keys) to an input element identified by XPath.
        """
        try:
            element = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            element.send_keys(*values)
        except Exception as e:
            print(f"Failed to send keys to element with XPath '{xpath}'. Values: {values}. Error: {e}")
    
    def OpenPage(self, url):
        """
        Parameters:
            url (str): URL to website
        Navigates the browser to the specified URL.
        """
        try:
            self.driver.get(url)
        except Exception as e:
            print(f"Failed to open page '{url}': {e}")

    def CountChildren(self, xpath):
        """
        Parameters:
            xpath (str): XPath to element

        Counts the number of direct child elements of the element located by the given XPath.
        Returns:
            int: Number of direct children, or -1 if element not found or error occurs.
        """
        try:
            parent = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            children = parent.find_elements(By.XPATH, './*')
            return len(children)
        except Exception as e:
            print(f"Error counting direct children for element with XPath '{xpath}': {e}")
            return -1
