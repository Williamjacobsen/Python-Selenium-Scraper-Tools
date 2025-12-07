# Selenium Web Scraper Tools

A flexible, reusable web scraping class built with `Selenium`, `undetected-chromedriver`, and `BeautifulSoup`, designed to bypass detection, interact with modern websites, and extract data with ease.

## Features

- Headless browsing with **undetected-chromedriver**
- Robust element interaction: click, input, retrieve text and attributes
- DOM traversal: BFS tag search, child indexing, and more
- Cookie persistence support
- Clean and maintainable codebase with structured methods

---

## Installation

```bash
pip install selenium beautifulsoup4 lxml undetected-chromedriver setuptools
```

## Quick Start

```python
from scraper import Scraper

scraper = Scraper()
scraper.OpenPage("https://example.com")

# Interact with elements
scraper.Click("//button[@id='login']")
scraper.SendKeys("/html/body/div[3]/input", "myusername")
scraper.SendKeys("/html/body/div[4]/input", "mypassword", scraper.keys.ENTER)

# Extract data
title = scraper.GetText("/html/body/div[1]/h4")

# Save session
scraper.SaveCookies()
```

## Cookie Management

```python
# Save current session cookies
scraper.SaveCookies()

# Later or on next session
scraper.LoadCookies()
scraper.RefreshPage()  # Required to apply cookies
```

## Class Methods Overview

| Method                                        | Description                                                                             |
| --------------------------------------------- | --------------------------------------------------------------------------------------- |
| `OpenPage(url)`                               | Navigates the browser to the specified URL.                                             |
| `Click(xpath)`                                | Clicks on an element located by the given XPath.                                        |
| `SendKeys(xpath, *values)`                    | Sends text or special keys to an input element located by XPath.                        |
| `GetText(xpath)`                              | Extracts and returns the visible text of the first element matching the XPath.          |
| `GetTextFromElement(element)`                 | Returns the visible text from a given WebElement.                                       |
| `GetAttribute(xpath, attribute)`              | Gets the value of a specific attribute (e.g., `href`, `src`) from xpath.                |
| `GetAttributeFromElement(element, attribute)` | Gets the value of a specific attribute (e.g., `href`, `src`) from an element.           |
| `GetElement(xpath)`                           | Returns the first matching WebElement for a given XPath.                                |
| `GetChildren(xpath)`                          | Returns a list of direct child elements of an element located by XPath.                 |
| `GetChildrenFromElement(element)`             | Returns a list of direct children from a given WebElement.                              |
| `CountChildren(xpath)`                        | Returns the number of direct child elements for a given XPath.                          |
| `FindFirstTagFromElement(element, tag)`       | Performs a breadth-first search to find the first child element with the specified tag. |
| `GetOuterHTMLFromElement(element)`            | Retrieves the full outer HTML (including the element tag itself) of a WebElement.       |
| `GetChildByIndex(parent, index)`              | Gets a direct child element at the specified index from a parent WebElement.            |
| `SaveCookies()`                               | Saves the current session's cookies to a `cookies.pkl` file.                            |
| `LoadCookies()`                               | Loads cookies from a saved file and injects them into the browser session.              |
| `RefreshPage()`                               | Refreshes the currently loaded webpage.                                                 |

## Notes

- Designed for Chromium-based browsers using `undetected-chromedriver` to bypass bot detection.
- Ensure you use the latest version of `undetected-chromedriver` for maximum compatibility.
- To enhance stealth:
  - Set a custom user agent via ChromeOptions.
  - Use headless mode cautiously (some sites detect it).
- When automating login or form submission, add appropriate delays if needed to mimic human behavior.
- Always respect `robots.txt` directives and the terms of service of the websites you're scraping.
- This tool is intended for ethical and legal scraping use cases only.
