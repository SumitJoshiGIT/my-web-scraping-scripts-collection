import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd

# Define the URL of the HDFC Bank credit card page


class Browser():  
    def __init__(self):
        self.url='https://www.hdfcbank.com/personal/pay/cards/credit-cards'
        self.output=r'hdfc_credit_cards.csv'
        self.data=[]
        chrome_options=webdriver.ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-notifications")
        #chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("force-device-scale-factor=0.50")
        chrome_options.add_argument("high-dpi-support=0.50")
        prefs = {"profile.`default_content_settings.popups": 0}
        chrome_options.add_experimental_option('prefs', prefs)
        chrome_options.add_experimental_option("excludeSwitches",["enable-logging"])
        self.driver = webdriver.Chrome(ChromeDriverManager().install(),options=chrome_options)
        self.driver.maximize_window()
        self.driver.set_page_load_timeout(15)
        self.wait=WebDriverWait(self.driver,10,poll_frequency=0.5)  
        self.action = ActionChains(self.driver)
        try:self.driver.get(self.url)
        except Exception as e:print(e)
        
        self.stime=time.time()
   
    def parse_credit_cards(self):
            
            self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,'div[class="card-offer-contr"]')))
            
            self.driver.execute_script("window.scrollBy(0,700);")
            time.sleep(3)
            cards = self.driver.find_elements(By.CSS_SELECTOR,'div[class="card-offer-contr"]')
            print(len(cards))
                
            for card in cards:
                name = card.find_element(By.CSS_SELECTOR,'h2[class="cardTitle"]').text.strip()
                print(name)
                fee = card.find_element(By.CSS_SELECTOR,'div[class= "fee"]').text.strip()
                print(fee)
                points = card.find_element(By.CSS_SELECTOR,'span[class="reward-points"]').text.strip()
                lounge = card.find_element(By.CSS_SELECTOR,'div[class="lounge-access"]').text.strip()
                milestone=card.find_element(By.CSS_SELECTOR,'div[class="milestone-benefit"]').text.strip()
                reversal = card.find_element(By.CSS_SELECTOR,'div[class="fee-reversa"l').text.strip() 
                self.data.append([name, fee, points, lounge, milestone, reversal])
                self.driver.execute_script("window.scrollBy(0,1000);")
                time.sleep(2)
                
            df=pd.DataFrame(self.data, columns=['Card Name', 'Card fee', 'Reward points', 'Lounge access', 'Milestone benefit', 'Card fee reversal'])
            print("Data_Scraped--------------------------->\n")
            print(df)
            df.to_csv('hdfc_credit_cards.csv', index=False)

    def close_browser(self):
        print(f"-----------------------------\nTime Taken:{time.time()-self.stime}")
        self.driver.close()


if __name__=='__main__':
        browser=Browser()
        browser.parse_credit_cards()
        time.sleep(10000)      
        browser.close_browser()     


# Create a pandas DataFrame from the scraped data

# Export the DataFrame to a CSV file
