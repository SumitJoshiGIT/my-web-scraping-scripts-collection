import time
import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager#webdriver manager for selenium(makes life easier)-->open readme for more info
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import utils
print("--------------------------Selenium-------------------------------")
#Setting up chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--headless=new")
Path=r"C:\Users\ucsss\Desktop\Aegon Scraper\files"
print(Path)
prefs = {"profile.`default_content_settings.popups": 0,"download.default_directory":Path,"directory_upgrade": True}


chrome_options.add_experimental_option('prefs', prefs)
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

#variables
Logger=utils.Logger()#Logging system initialization
name=""

#Filtering keywords from excel file

products=set()
product_list=pd.read_excel('template.xlsx')['Name of the Product']
[products.update(product.lower().split(" ")) for product in product_list]#selecting each product from the list and extracting uniquewords from them and lowercasing them
products=utils.uniquify(products)

#Section1>>startup and assignment of all relevant variables ((i.e web driver instance,waits,locators of page elements) 
try:
 browser = webdriver.Chrome(ChromeDriverManager().install(),options=chrome_options)
 wait = WebDriverWait(browser, 40)
 url=r"https://www.aegonlife.com/downloads"
 browser.get(url)
 
 #relevant element locators
 select_plan= wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,"button[class='product-select-button']")))
 radio_buttons=browser.find_elements( By. CSS_SELECTOR,"input[id^='product-'][type='radio']")
 continue_button=browser.find_element(By.XPATH,'//*[@id="product-select-modal"]/div[2]/div[3]/agn-button/button')
 print("---------------------------LOGS-----------------------------") 

except Exception as e:  
  raise e

 
def filter_downloads(downloads):
  flag=1
  if len(downloads)>1:#if only one brochure link is there then dont go through filter step
      for single_download in downloads:#this loop will gather and filter the brochure download links for a plan        
        single_download=single_download.find_element(By.CSS_SELECTOR,'a[target="_blank"]')
        name=single_download.get_attribute('download')[:-4].lower()
        if "brochure" in name:#if brochure is in the name of target then proceed to filter
           try:
            name=name.replace("brochure","")
            name=name.replace("_"," ")

            if utils.match_name(name.split(" "),products):#filter step
              single_download.click()
              flag=0
              Logger.log(name+" downloaded.")
              return 1
           except:continue 
  elif len(downloads)>=0 and flag:
    downloads[0].click()
    name=downloads[0].get_attribute('download')[:-4]
    Logger.log(name+" downloaded.")
    return 1
  return 0    
#Section 2>>Main scraping and cross-checking algorithm 

def corner_case():
     url="https://www.aegonlife.com/online-plans/iterm-prime"
     browser.get(url)

     try:down_button=wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'li[id="agn-iterm-downloads"]')))
     except:pass

     browser.execute_script("arguments[0].scrollIntoView();",down_button)
     browser.execute_script("arguments[0].click();",down_button)

     downloads=browser.find_elements(By.CSS_SELECTOR,'div[class="agn-dcard-icon"]')
    
     return filter_downloads(downloads)
        
def main():
 n_downloads=0#keeps track of no of completed downloads 
 Logger.log("Main function launched")
 n=0
    
 for radio_button in radio_buttons:#this loop is to iterate over each plan available  
    global wait
    #sub-1>>policy selection step setup
    browser.execute_script("arguments[0].scrollIntoView();", select_plan)
    browser.execute_script("arguments[0].click();", select_plan)
    time.sleep(2)
    browser.switch_to.active_element
    wait.until(EC.element_to_be_clickable(radio_button)).click()
    browser.switch_to.active_element
    wait.until(EC.element_to_be_clickable(continue_button)).click()

    if not (utils.match_name(select_plan.text,product_list,1)):continue#checks if policy is in product list 
    n+=1

    #sub-2>>scrapes all download links and filters the correct link and clicks it
    downloads=browser.find_elements(By.CSS_SELECTOR,'div[class="agn-dcard-icon"]')
    n_downloads+=filter_downloads(downloads) 
    browser.switch_to.active_element
 if 'prime' in products:#corner case handler
  n_downloads+=corner_case()
 time.sleep(10)
 Logger.log(f"ALL DOWNLOADS DONE!           Downloaded:{n_downloads}")    

 

main()
        
            



