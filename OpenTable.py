from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import csv 
import time
import pandas as pd
from bs4 import BeautifulSoup

# Open Driver Path

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--blink-settings=imagesEnabled=false")
chrome_options.add_argument("--high-dpi-support=0.5")
chrome_options.add_argument("--force-device-scale-factor=0.2") 
driver = webdriver.Chrome(r"C:\Users\ucsss\Downloads\chromedriver\chromedriver.exe",chrome_options=chrome_options)
# Add in time/date/#party values
looptime = ['18']
loopdate = ['2023-11-26']
loopparty = ['2']
scroll_script = "window.scrollBy(0,500);"

def fetch_links():
 # Create Empty Lists to append in loop
 url = []
 # Create a set to store unique restaurant URLs
 unique_urls = {}
 counter=0
 for p in loopparty:
    for d in loopdate:
        for i in looptime:
            url = f'https://www.opentable.com/s?dateTime={d}+{i}-+{i}&covers={p}&metroId=72&shouldUseLatLongSearch=false&sortBy=web_conversion&queryUnderstandingType=none&latitude=&longitude=&suppressPopTable=false&corrid=2a4aa82d-72a3-4cca-854a-0f52e92a0248'
            driver.get(url)
            purl=""
            while True:
                # Allow some time for the page to load
                time.sleep(7)
                try:
                 next_page_button = driver.find_element(By.CSS_SELECTOR, "a[aria-label='Go to the next page']")
                except:
                    driver.get(url)
                    continue 

                counter=0
                while  counter<7:    
                        driver.execute_script(scroll_script)
                        time.sleep(0.2)  
                        counter+=0.2

                restaurant_tags = driver.find_elements(By.CSS_SELECTOR,"a[data-test='res-card-name']")
                for restaurant_tag in restaurant_tags:
                    restaurant_url = restaurant_tag.get_attribute("href")
                    restaurant_name = restaurant_tag.get_attribute("aria-label")
                    unique_urls[restaurant_url]=restaurant_name
                    #print(f"Name: {restaurant_name}, URL: {restaurant_url}")

                print("Page Scrapped,Entries:",len(restaurant_tags))    
                 
                if(purl==driver.current_url):break 
                purl=driver.current_url
                # Check for the next page button
                if not next_page_button:break
                # Click the next page button
                try:next_page_button.click()
                except:pass
                break       
            print(unique_urls.values(),len(unique_urls))  
 return unique_urls

def crawl_urls(unique_urls):
 output = []
 for url in unique_urls:
  driver.get(url)
  time.sleep(5)
  menu=driver.find_element(By.CSS_SELECTOR,"li[aria-label='Menu']")
  menu.click()
  menus=driver.find_elements(By.CSS_SELECTOR,'button[data-test="menu-tabs-button"]')
  items={}
  heading=""
  main_dict={"Menus":{},"longitude":None,"latitude":None,"Location":None,"Cuisine":None,"Style":None}
  item_dict={}
  menutype=""
  menu_dict={}
  if not menus:
     menutype="External"
     item_dict=driver.find_element(By.CSS_SELECTOR,'section[id="menu"] a').get_attribute('href')
  
  for x in menus:
    sides=""
    price=""
    sub_heading=""
    try:
      x.click()   
      time.sleep(2)
      expand=driver.find_element(By.CSS_SELECTOR,'article [data-test="expansion-button"]')
      expand.click()
    except Exception as e:pass
    items=driver.find_elements(By.CSS_SELECTOR,'article[data-test="menu-section"] ')
    for x in items:
       heading=x.find_element(By.TAG_NAME,'h3').text
       item_dict.update({heading:{}})
       sub_items=x.find_elements(By.TAG_NAME,'li')
       
       for y in sub_items:
          sub_heading=y.find_element(By.CSS_SELECTOR,'span[data-test="item-title"]').text
          try:
           price=y.find_element(By.CSS_SELECTOR,'[data-test="item-price"]').text
          except Exception as e:
             try:
                price=y.find_element(By.CSS_SELECTOR,'span[data-test="variation-price"]').text
                price+=" "
                price+=y.find_element(By.CSS_SELECTOR,'span[data-test="variation-title"]').text
             except:pass
          try:         
           sides=y.find_element(By.CSS_SELECTOR,'[data-test="item-title"]').text
          except:
           try:
            sides=(y.find_element(By.TAG_NAME,'h4').text).split('\n',1)
            sides=sides[0]
            price=price or sides[1]
           except:pass    
            
          item_dict[heading].update({sub_heading:{"price":price,"sides":sides}})  
          menutype=x.text
  menu_dict.update({menutype:item_dict})

  try: 
            longitude=driver.find_element(By.CSS_SELECTOR,'meta[property="place:location:longitude"]').get_attribute("content")
            latitude=driver.find_element(By.CSS_SELECTOR,'meta[property="place:location:latitude"]').get_attribute("content")
  except:
            longitude=""
            latitude=""   
  try:
            location=driver.find_element(By.CSS_SELECTOR,'[data-testid="icLocation"] + div a')
            location_link=location.get_attribute('href')
            location=location.get_attribute('innerHTML')
      
  except:
            location=""
            location_link=""
  try:     
            style=driver.find_element(By.CSS_SELECTOR,'[data-test="icDiningStyle"] + div div').get_attribute('innerHTML')
            cuisine=driver.find_element(By.CSS_SELECTOR,'[data-test="icCuisine"] + div div:first-of-type').get_attribute('innerHTML')     
  except :
        style=""
        cuisine=""
     
      
  output.append([unique_urls[url],str(menu_dict),longitude,latitude,location,location_link,cuisine,style])
  print(output[-1])
  if(len(output)>10):
     yield output
     output={}
 if output:yield output    

def save_into_csv(row_gen,path="output.csv"):
    with open(path, mode='w', newline='') as file:
     writer = csv.writer(file) 
     for rows in row_gen:     
      print(rows)
      writer.writerows(rows)



url="https://www.opentable.com/r/americana-southern-hospitality-london?originId=414a935d-6a6a-4775-a871-f2466124497a&corrid=414a935d-6a6a-4775-a871-f2466124497a&avt=eyJ2IjoyLCJtIjoxLCJwIjoxLCJzIjowLCJuIjowfQ"

save_into_csv(crawl_urls({url:"ru"} or fetch_links()))
driver.quit()
