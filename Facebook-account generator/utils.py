from twocaptcha import TwoCaptcha
import motor.motor_asyncio
import os
from time import time
import aiofiles
import asyncio
from random import randint, uniform,choice,shuffle
import urllib
from config import *
os.environ['PATH']+=r"ffmpeg\bin"
import pydub
from speech_recognition import Recognizer, AudioFile

def iphone():
    while True:
        shuffle(iphones)
        for l in iphones:
            yield l
def user_agent(browser_name):
  while True:
     for l in agents[browser_name]:  
      yield {"User-Agent":l}
    
async def curl_image(session,name):
    url=r"https://thispersondoesnotexist.com/image"   
    resp = await session.get(url)
   
    path='images\\'
    if os.path.exists(path):pass
    else:os.makedirs(path)
    path += f'{name}.jpeg'
    async with aiofiles.open(path,"wb") as f:
        data = await resp.read()
        
        await f.write(data)
    return path

async def change_ip(session):
    await session.get(r"http://api.mproxy.top/change_ip/wiwao_30016")

class fake_human:
    def __init__(self, db):
        self.creds = db["CREDENTIALS"]
        self.acc = db["ACCOUNTS"]

    async def human(self):
        self.fake = await self.creds.find_one({"used": 1})
        
        await self.creds.update_one(self.fake, {"$set": {"used": 0}})
        self.fake.pop("_id")
        self.FN = self.fake["FN"]
        self.LN = self.fake["LN"]
        self.G = self.fake["G"]
        self.password = self.fake["password"]
        self.day = self.fake["day"]
        self.year = self.fake["year"]
        self.month = self.fake["month"]


    async def save_fake(self,contact, cookie, status,user_agent="",account_id=None,token=None,time=""):
        if status=="confirmed":
          self.fake={"time_created":time,"contact": contact,"password":self.password,"account_id":account_id,"token":token,"cookie": cookie,"User-Agent":user_agent,"status":status}
        else:self.fake={"contact": contact,"password":self.password,"account_id":account_id,"token":token,"cookie": cookie,"User-Agent":user_agent,"status":status}  
        self.acc.insert_one(self.fake)
        
class captcha():
    def __init__(self):
        self.solver = TwoCaptcha(API_KEYS["recaptcha"])
        self.key=API_KEYS["recaptcha"]
  
    async def resolve_captcha2(self,page,mode=1):

          print(self.solver.balance())
          frame=page.frame_locator("#captcha-recaptcha")
          inner_frame= frame.frame_locator('[title="reCAPTCHA"]')    
           
          button_= inner_frame.locator('span[id="recaptcha-anchor"]')
          try:
            sitekey = await frame.locator( 'div[data-expired-callback="expiredCallback"]').get_attribute("data-sitekey")
            response=response = self.solver.recaptcha(sitekey=sitekey, url=page.url, version='v3', score='0.9').get('code')
            print(response)     
            await button_.click()
            ref=time()
            timeout=15
            ctime=0  
            while await button_.get_attribute("aria-checked")=='false' and timeout-ctime>0:
             ctime=time()-ref
             await asyncio.sleep(uniform(0.4,1))
             if await page.is_visible('iframe[title="recaptcha challenge expires in two minutes"]'):
              await button_.click()
              await asyncio.sleep(5)
              sitekey = await frame.locator( 'div[data-expired-callback="expiredCallback"]').get_attribute("data-sitekey")
              print(sitekey,page.url)
              response=solve(sitekey,page.url)
              print("res",response)
              break
             else:await asyncio.sleep(uniform(0.6,1))   
            await page.evaluate('document.getElementById(g-recaptcha-response).innerHTML={response}')
            await asyncio.sleep(0.5)
            button_.click()
            return True
          except Exception as e:
            print(e)
            await asyncio.sleep(400)
            
            
class number():
    def __init__(self):
        # self.session=session
        self.key = API_KEYS["smshub"]
        self.url = r"https://smshub.org/stubs/handler_api.php"
        self.current_number=None
        
    async def get_number(self,countries=countries,session=None):
           print("Awaiting available numbers...",end=" ")
           while True:
            for country in countries: 
             param = {"api_key": self.key,
                     "action": "getNumber",
                     "service": "fb",
                     "country": country}
            
             response =(await session.post(self.url, params=param))
             response1=await response.text()
             response=response1.split(':')
             if "ACCESS_NUMBER" in response:
                self.access_no = response[1]
                self.current_number = response[2]
                print(self.current_number)
                return True
            
                                     
      
    async def OTP(self,session,timeout=180):
       params = {
                "action": "getStatus",
                "api_key": self.key,
                "id": self.access_no}
       print("Awaiting OTP.....",end=" ")
       async def get_otp(session):  
           ref = time()
           timer=0
           while timeout - timer > 0: 
            flag=0 
            try:response = await(await session.post(self.url, params=params)).text()
            except:flag=1  
            if flag==1:continue
            timer = (time()-ref)
            if "STATUS_OK" in response:
                 self.otp=response.split(":")[1]
                 print(self.otp)
                 return True
           print("Failed!")     
           return False
       if await get_otp(session)==True:return True    
       else:return False

    async def deactivate_current_no(self,session=None,success=False):
      if success:code="6"
      else:code="8"
      params = {
            "action": "setStatus",
            "api_key": self.key,
            "id": self.access_no,
            "status": code}
      if not session:  
        async with aiohttp.ClientSession() as session: 
         response = await(await session.get(self.url, params=params))
      else:(await session.get(self.url, params=params))
      
    def reset(self):
        self.current_number=None

def extract(o):      
      date=f"{o.day}_{o.month}_{o.year}"
      time=f"{o.hour}_{o.minute}_{o.second}"
      return (date,time) 
        
from playwright.sync_api import sync_playwright, TimeoutError
from playwright_stealth import stealth_sync
import datetime
import json

# for recaptcha
"""
configs = {
    'CHROME_BUNDLE': '/home/binit/driver/chrome-linux/chrome',
    'HEADLESS': 'false',
}

          inner_frame= frame.frame_locator('[title="reCAPTCHA"]')    
           
          button_= inner_frame.locator('span[id="recaptcha-anchor"]')
          try:
            sitekey = await frame.locator( 'div[data-expired-callback="expiredCallback"]').get_attribute("data-sitekey")
            response=response = self.solver.recaptcha(sitekey=sitekey, url=page.url, version='v3', score='0.9').get('code')
            print(response)     
            await button_.click()
            ref=time()
            timeout=15
            ctime=0  
            while await button_.get_attribute("aria-checked")=='false' and timeout-ctime>0:
             ctime=time()-ref
             await asyncio.sleep(uniform(0.4,1))
             if await page.is_visible('iframe[title="recaptcha challenge expires in two minutes"]'):
   """            
class CaptchaSolve:
    def __init__(self, page):
        self.page = page
        self.main_frame = None
        self.recaptcha = None
  
    async def presetup(self):
        await asyncio.sleep(10)
        try:
          await self.page.wait_for_selector("#captcha-recaptcha",timeout=17)
        except:pass
        frame_=self.page.frame_locator("#captcha-recaptcha")
        name = await frame_.locator( "xpath=//iframe[@title='reCAPTCHA']").get_attribute("name")
        
        self.recaptcha = self.page.frame(name=name)

        await self.recaptcha.click("xpath=//div[@class='recaptcha-checkbox-border']")
        await asyncio.sleep(3)
        self.s = self.recaptcha.locator("xpath=//span[@id='recaptcha-anchor']")
        if await self.s.get_attribute("aria-checked") != "false":  # solved already
            return True

        self.main_frame = self.page.frame(name=await frame_.locator("xpath=//iframe[contains(@src,'https://www.google.com/recaptcha/api2/bframe?')]").get_attribute("name"))
    
        await self.main_frame.click("id=recaptcha-audio-button")

    async def start(self):
        val=await self.presetup()
        if val:return True
        tries = 0
        while (tries <= 5):
            await asyncio.sleep(randint(1, 3))

            try:
               await self.solve_captcha()
            except Exception as e:
                print(e)
                await  self.main_frame.locator("id=recaptcha-reload-button").click()
            else:
                await asyncio.sleep(uniform(3,4))
                if await self.s.get_attribute("aria-checked") != "false":
                    return True
            tries += 1    
        print('ded')    
        return False    
    async def save(a):Pass
    async def solve_captcha(self):
 
        #await self.main_frame.locator('button[id="recaptcha-audio-button"]').click()
        await self.main_frame.click(
            "xpath=//button[@aria-labelledby='audio-instructions rc-response-label']")
        href = await self.main_frame.locator( "xpath=//a[@class='rc-audiochallenge-tdownload-link']").get_attribute("href")

        urllib.request.urlretrieve(href, "audio.mp3")
        
        sound = pydub.AudioSegment.from_mp3(
            "audio.mp3").export("audio.wav", format="wav")

        recognizer = Recognizer()

        recaptcha_audio = AudioFile("audio.wav")
        with recaptcha_audio as source:
            audio = recognizer.record(source)

        text = recognizer.recognize_google(audio)
        print(text)
        await self.main_frame.type("id=audio-response", text)
        await self.main_frame.click("id=recaptcha-verify-button")
        await asyncio.sleep(randint(1, 3))


    def __del__(self):
     try: 
      if os.path.exists("audio.mp3"):
        os.remove("audio.mp3")
        os.remove("audio.wav")
     except:pass

