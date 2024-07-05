from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException as clickerror
from bs4 import BeautifulSoup as bs
import pandas as pd
from random import choice
from selenium.webdriver.chrome.service import Service
import undetected_chromedriver as uc
import time
from selenium.webdriver.common.action_chains import ActionChains


from selenium.webdriver.common.keys import Keys
 
agents=[
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.37",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 11; Pixel 4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36",
]
service=Service(r'C:\Users\Maelstorm\Downloads\chromedriver.exe')
options = webdriver.ChromeOptions()
options.add_argument("--disable-notifications")  # Disable notifications
options.add_argument("--disable-popup-blocking")  # Disable pop-up blocking
 
driver =webdriver.Chrome(service=service,options=options)
actions = ActionChains(driver)

driver.maximize_window()
def gen_user_agent():
  while(True):
    yield choice(agents)

user_agent=gen_user_agent()

def change_user_agent(user_agent):
    params = {
        "userAgent": next(user_agent),
        "platform": "Windows"
    }
    command = "Network.setUserAgentOverride"
    driver.execute_cdp_cmd(command, params)


def scrape_link(location,link="https://www.bestwestern.com/en_US/book"):
    
    data = []
    change_user_agent(user_agent)
    driver.get(link+"/hotel-search.html")
    element=driver.find_element(By.CSS_SELECTOR,'.slider')
    element_width = element.size['width']
    element_height = element.size['height']
    end_x = element.location['x'] + element_width
    end_y = element.location['y'] + element_height
    actions.move_to_element_with_offset(element, end_x, end_y).click().perform()
    time.sleep(0.2)
    creds=driver.find_element(By.CSS_SELECTOR,'button[id="btn-modify-stay"]') 
    summary=driver.find_element(By.CSS_SELECTOR,'.summary-loading-hv')
    summary.click()
    time.sleep(2)
    creds.click()
    loc=driver.find_element(By.CSS_SELECTOR,"#destination-input")
    
    #cdate=driver.find_element(By.CSS_SELECTOR,"#checkin")
    #edate=driver.find_element(By.CSS_SELECTOR,"#checkout")
    loc.send_keys(location)
    time.sleep(2)
    loc.send_keys(Keys.DOWN)
    time.sleep(0.1)
    loc.send_keys(Keys.ENTER)
    update=driver.find_element(By.CSS_SELECTOR,"#btn-modify-stay-update")
    update.click()
    time.sleep(2)
    while(summary.is_displayed()):time.sleep(0.5)
    elements=driver.find_elements(By.CSS_SELECTOR,'.sortHotelCard')
    #while():driver.execute_script("document.querySelector.scrollBy()")
    for element in elements:
       pcode=element.get_attribute('data-resort')
       name=(element.find_element(By.CSS_SELECTOR,"div[id^='hotel']").text).lower().replace(' ','-')
       cname=(element.find_element(By.CSS_SELECTOR,"div[id^='city']").text).split(',')[0].lower().replace(' ','-')
       l=f"{link}/hotels-in-{cname.strip()}/{name.strip()}/propertyCode.{pcode.strip()}.html"
       data.append(l)
    print(data,len(data))
    return data 



def test(): 
  scrape_link("london")
  driver.quit()

test()