from collections import deque
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from selenium.webdriver.common.keys import Keys
import pickle

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
        #Clear()
        self.chrome_options = webdriver.ChromeOptions()
        self.driver = uc.Chrome() #options=self.chrome_options
        self.wait = WebDriverWait(self.driver, 20)
        self.keys = Keys
        #Clear()
    
    def Click(self, xpath: str) -> None:
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

    def GetText(self, xpath: str) -> str:
        """
        Parameters:
            xpath (str): XPath to element

        Finds the first element matching the XPath and returns the extracted text.
        Returns an empty string if the element is not found or parsing fails.
        """
        #try:
        elements = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath)))
        html_content = elements[0].get_attribute('innerHTML')
        soup = BeautifulSoup(html_content, features="lxml")
        return soup.get_text()
        #except Exception as e:
        #    print(f"Could not locate or parse element with XPath '{xpath}': {e}")
        #    return ""

    def GetTextFromElement(self, element) -> str:
        """
        Parameters:
            element (WebElement): A Selenium WebElement.

        Returns the extracted visible text from the given WebElement.
        Returns an empty string if the element is None or parsing fails.
        """
        if element is None:
            return ""
        
        try:
            html_content = element.get_attribute('innerHTML')
            soup = BeautifulSoup(html_content, features="lxml")
            return soup.get_text()
        except Exception:
            return ""

    def SendKeys(self, xpath: str, *values) -> None:
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
    
    def OpenPage(self, url: str) -> None:
        """
        Parameters:
            url (str): URL to website
        Navigates the browser to the specified URL.
        """
        try:
            self.driver.get(url)
        except Exception as e:
            print(f"Failed to open page '{url}': {e}")

    def CountChildren(self, xpath: str) -> int:
        """
        Parameters:
            xpath (str): XPath to element

        Counts the number of direct child elements of the element located by the given XPath.
        Returns:
            int: Number of direct children, or -1 if element not found or error occurs.
        """
        try:
            return len(self.GetChildren(xpath))
        except Exception as e:
            print(f"Error counting direct children for element with XPath '{xpath}': {e}")
            return -1
    
    def GetAttribute(self, xpath: str, attribute: str) -> str:
        """
        Parameters:
            xpath (str): XPath to element 
            attribute (str): Name of the attribute to read (e.g. 'href', 'src')
        
        Returns:
            The value of the requested attribute, or an empty string if not found.
        """
        try:
            elem = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            return elem.get_attribute(attribute) or ""
        except Exception as e:
            print(f"Error getting attribute '{attribute}' from element {xpath}: {e}")
            return ""

    def GetAttributeFromElement(self, element, attribute: str) -> str:
        """
        Parameters:
            element (WebElement): The Selenium WebElement to read from.
            attribute (str): Name of the attribute to retrieve (e.g. 'href', 'src', 'data-id').

        Returns:
            str: The value of the requested attribute, or an empty string if not found or an error occurs.
        """
        try:
            if element is None:
                return ""
            return element.get_attribute(attribute) or ""
        except Exception as e:
            print(f"Error getting attribute '{attribute}' from element: {e}")
            return ""

    def GetChildren(self, xpath: str):
        """
        Parameters:
            xpath (str): XPath to element 

        Returns a list of elements for every direct child of the element located by xpath.
        """
        try:
            parent = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            return parent.find_elements(By.XPATH, './*')
        except Exception as e:
            print(f"Error retrieving children for element with XPath '{xpath}': {e}")
            return []
        
    def GetChildrenFromElement(self, element):
        """
        Parameters:
            xpath (str): XPath to element 

        Returns a list of elements for every direct child of the element located by xpath.
        """
        try:
            if element is None:
                return None
            
            return element.find_elements(By.XPATH, './*')
        except Exception as e:
            print(f"Error retrieving children for element '{element}': {e}")
            return []
    
    def FindFirstTagFromElement(self, element, tag: str):
        """
        Breadth-first search for the first child element with the specified tag.

        Parameters:
            element (WebElement): The root element to search under.
            tag (str): Tag name to search for.

        Returns:
            WebElement if found, None otherwise.
        """
        try:
            if not hasattr(element, 'find_elements'):
                raise TypeError(f"Expected WebElement, got {type(element).__name__}")

            queue = deque([element])

            while queue:
                current = queue.popleft()
                children = current.find_elements(By.XPATH, './*')

                for child in children:                    
                    if child.tag_name.lower() == tag.lower():
                        return child
                    queue.append(child)

            return None
        except Exception as e:
            print(f"Error in BFS tag search from element for tag '{tag}': {e}")
            return None
    
    def GetElement(self, xpath: str):
        """
        Parameters:
            xpath (str): XPath to the element.

        Returns:
            The first matching WebElement if found, or None otherwise.
        """
        try:
            return self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        except Exception as e:
            print(f"Error locating element with XPath '{xpath}': {e}")
            return None
    
    def GetOuterHTMLFromElement(self, element) -> str:
        """
        Parameters:
            element (WebElement): A Selenium WebElement.

        Returns:
            A string containing the full HTML of the element, including its own tag and all child content.
            Returns an empty string if the element is None or an error occurs.
        """
        try:
            if not hasattr(element, 'get_attribute'):
                raise TypeError(f"Expected WebElement, got {type(element).__name__}")
            return element.get_attribute('outerHTML')
        except Exception as e:
            print(f"Error extracting outer HTML: {e}")
            return ""
    
    def GetChildByIndex(self, parent, index: int):
        """
        Parameters:
            parent (WebElement): The parent element to get the child from.
            index (int): The zero-based index of the child.

        Returns:
            WebElement of the child at the given index, or None if out of bounds or error occurs.
        """
        try:
            if parent is None:
                return None
            children = parent.find_elements(By.XPATH, './*')
            if 0 <= index < len(children):
                return children[index]
            else:
                print(f"Index {index} is out of range. Found {len(children)} children.")
                return None
        except Exception as e:
            print(f"Error getting child at index {index}: {e}")
            return None

    def SaveCookies(self):
        pickle.dump(self.driver.get_cookies(), open("cookies.pkl", "wb"))
    
    def LoadCookies(self):
        """
        Loads cookies from a pickle file and adds valid ones to the browser session.
        Filters out problematic attributes.
        """
        try:
            cookies = pickle.load(open("cookies.pkl", "rb"))
            for cookie in cookies:
                # Remove attributes that may cause issues
                cookie.pop('sameSite', None)
                cookie.pop('secure', None)
                cookie.pop('httpOnly', None)
                cookie.pop('expiry', None)
                try:
                    self.driver.add_cookie(cookie)
                except Exception as e:
                    print(f"Skipping cookie: {cookie.get('name', '?')} - {e}")
        except Exception as e:
            print(f"Error loading cookies: {e}")

    def RefreshPage(self) -> None:
        """
        Refreshes the current page in the browser.
        """
        try:
            self.driver.refresh()
        except Exception as e:
            print(f"Failed to refresh the page: {e}")
