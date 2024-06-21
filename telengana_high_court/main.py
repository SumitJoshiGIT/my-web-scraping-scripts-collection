from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager#webdriver manager for selenium(makes life easier)-->open readme for more info
from selenium.webdriver.support.ui import WebDriverWait,Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.keys import Keys
from Filter import cv2,filter,np
from time import sleep
import pytesseract
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from random import randrange
#Setting up chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--start-maximized")
#chrome_options.add_argument("--headless=new")
prefs = {"profile.`defaulct_content_settings.popups": 0,"download.default_directory":r"downloads\\","directory_upgrade": True}

chrome_options.add_experimental_option('prefs', prefs)
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])




class  Scrapper():
  def __init__(self):
   service = Service(executable_path="chromedriver.exe")
   self.driver = webdriver.Chrome(service=service,options=chrome_options) 
   self.driver.maximize_window()
   self.driver.get("https://csis.tshc.gov.in/judgmnt_ts1/#")
   pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
   self.temp=r"temp/img.png"
   self.wait=WebDriverWait(self.driver,20)

  def initialize_form(self):
         self.driver.find_element(By.ID,"link24").click()
         self.fro = self.driver.find_element(By.NAME,"frmdto")  # Replace with the appropriate element locator
         self.to = self.driver.find_element(By.ID,"todto")
         self.status = Select(self.driver.find_element(By.ID,"lrnlrs")) 
         self.captcha = self.driver.find_element(By.ID,"ocaptcha")
         self.image= self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,"img[id='ocapImg']")))
         self.refresh= 'img[src="images/refresh.jpg"]'
  
  def process_captcha(self):
    self.image.screenshot("temp.png")
    image=filter()
    image.save("temp2.png")
    self.c_val = pytesseract.image_to_string(image ,config='--psm 6 --oem 3 -c tessedit_char_whitelist=0123456789').replace(' ','').strip().replace('\n','')
    n=6-len(self.c_val)
    print("val:"+self.c_val)
    if n!=0:
     if n<0:self.c_val=self.c_val[:n]
     else:self.c_val+=str(randrange(10**(n-1),10**(n)-1))
    print(self.c_val) 
    self.captcha.send_keys(self.c_val)

  def get_input(self,status='0',to="13-08-2023",fro="04-07-2023"):
        
        self.to.send_keys(to)
        self.fro.send_keys(fro)
        self.fro.send_keys(Keys.ENTER)
        if not status in {'0','1','2'}:status='2'
        self.status.select_by_index(status)
        print("Processing....")

  def submit_form(self):    
        self.driver.execute_script('let element=document.querySelector("#searchtwofour");element.click();')
        try:
            WebDriverWait(self.driver,7).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            text = alert.text
            alert.accept()
            if 'captcha' in text:
                self.driver.execute_script(f"let ele=document.querySelector('{self.refresh}');ele.click();")
                sleep(3)
                self.captcha.clear()
                self.process_captcha()
                self.submit_form()
        except Exception as e:
            return self.process_result()
              
  def process_result(self):
       table=self.wait.until(EC.visibility_of_element_located((By.ID,"inftable")))
       print("Loading")
       try:
        while('load' in table.text):
           sleep(2)
        if 'no' in table.text.lower():return None   
       except:return None    
       
       df=pd.read_html(table.get_attribute('outerHTML'))  
       index=df.loc[0,:]
       df.columns=index
       df.drop(1)
       df.group_by('Status')
       print(df)      
       if df:
        rows=table.find_elements(By.CSS_SELECTOR,"#inftable > tbody > tr > td >a")
        if not rows:return None
        else:
         links=[]
         for link in rows:links.append(link.get_attribute("href"))
         df["Link"]=np.array(links)
         print(df)
         return df
  
  def execute(self):
      self.initialize_form()
      self.process_captcha()
      self.get_input()
      val=self.submit_form()
      if not val:print("No details found for query!")
      else:
          with open("temp.txt","w") as file:
              file.write(str(val))
              

  def database_check(self):
    pass 
             
  def __del__(self): 
      sleep(60)
      self.driver.quit()

if __name__ == "__main__":
        ins=Scrapper()
        ins.execute()