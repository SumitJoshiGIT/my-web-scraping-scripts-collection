from playwright.async_api import async_playwright
from playwright_stealth import stealth_async
import motor.motor_asyncio
import aiohttp
import json
from speech_recognition import Recognizer, AudioFile
import datetime as dt
from utils import *
from python_ghost_cursor.playwright_async import create_cursor#only supports python 3.9 or below


class facebook_auto():
    def __init__(self,bot=False):
        self.bot=bot
        token=API_KEYS["bot_key"]
        self.api='https://api.telegram.org/bot'+token 
        self.offset=-1
        self.commands={"/login":self.login,"/resume":self.resume,"/pause":self.pause,
                       "/export":self.export,"/export_all":self.export_all,"/stop":self.shutdown,"/status":self.Status}
        self.flag=True
        self.queue=[]
        self.password=PASSWORDS
        
    def Log(self,level,text):
        
        time=extract(dt.datetime.today())[1]
        levels={"warn":"**WARNING","imp":">>IMPORTANT!!","err":"!![ERROR]:","change":"++CHANGE","basic":"/BASIC","diff":"--ANAMOLY"}
        if level in levels:   
         di={time:(levels[level]+": "+text)}
         
         self.current_log.update(di)
        
    async def change_ip(self,session):
       await session.get(r"https://api.mproxy.top/change_ip/wiwao_30016")    

    async def req_pool(self):
        self.client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017/')
        logs=self.client["FACEBOOK_LOGS"]
        self.Users=self.client["FACEBOOK"]["USERS"]
        args = [
        '--deny-permission-prompts',
        '--no-default-browser-check',
        '--no-first-run',
        '--deny-permission-prompts',
        '--disable-popup-blocking',
        '--ignore-certificate-errors',
        '--no-service-autorun',
        '--password-store=basic',
        '--window-size=640,480',
        '--disable-audio-output'
          ]
        i=iphone()
        self.Accounts=self.client["FACEBOOK"]["ACCOUNTS"]
        def viewport():
          while True: 
            v=((1366,768),(1280,1024),(1280,800),(1024,768),(1536,864),(1920,1080),(1280,720))
            for l in v:
                yield {'width':l[0],'height':l[1]}
            shuffle(v)
            
        vw=viewport()    
        async with async_playwright() as p:
         
          async with aiohttp.ClientSession() as session:
               if self.bot==True:
                print("Bot:True")   
                asyncio.create_task(self.Pool(session))
                
               browser = await p.chromium.launch(channel="chrome",headless=False,proxy=proxy)
             
               while True:
                   await self.change_ip(session)
                   self.current_log={}
                   ref=time()#
                   lang=choice(('ru-mo,en-US;q=0.9','ru-mo,ru;q=0.9','ru-mo,ro-mo;q=0.9','ru-mo,ro;q=0.9'))
                   browser_= await browser.new_context(viewport=next(vw),ignore_https_errors=True,locale=lang,timezone_id=choice(['Europe/Chisinau',"Europe/Lisbon","Etc/Universal"]))#**next(i))#)#,    
                   val=None
                   #try:
                   
                   val=await self.register_account(
                                             browser_,
                                             human=fake_human(self.client["FACEBOOK"]),
                                             session=session,
                                             UA=ChromeAgent(173))
                   
                   print(val)  
                  
                   self.Log('imp',"Done :"+str(time()-ref))
                   if self.bot:                 
                     message="----------LOGS---------\n"+('\n'.join([f"{l}:{self.current_log[l]}" for l in self.current_log]))
                   try: pass   
                   #await logs[self.date].insert_one(self.current_log)
                   except Exception as e:
                       print("LOGGING ERROR",e)
                   print("Done :"+str(time()-ref))  
                   print("------------------------------------------------")
                   #await self.fetch_tokens(browser_)
                   await browser_.close()
                   while self.flag==False:
                       if self.flag=="quit":
                        self.Log("imp","quit flag raised.")
                        quit()
                       
                       await asyncio.sleep(2)  
                   if self.flag=="quit":
                       self.Log("imp","quit flag raised.")
                       quit()
                   
                   
    async def register_account(self, browser,human,session,UA):
      print(UA[0])
      await browser.set_extra_http_headers({"User-Agent":UA[0]})
      
      datetime=extract(dt.datetime.today())
      date=datetime[0]
      self.date=date
      await human.human()
      status=None
      mynumber=number()
      pin=False
      contact="fasafe"#await mynumber.get_number(session=session)
      
      page = await browser.new_page()
      client = await page.context.new_cdp_session(page)
      await client.send('Network.setUserAgentOverride',UA[1])
      await stealth_async(page)

      page.set_default_timeout(20000)
      #cursor=create_cursor(page)
  

      
      self.Log("basic",date+","+datetime[1]+"////"+str(mynumber.current_number))  
      delay_patt=choice([(50,150),(60,120),(80,200),(30,120)])
    
      async def timeout(selector,timeout=15,vis=False):
          ref=time()
          timer=0 
          while await page.is_visible(selector)==vis and timer<timeout:
              timer=time()-ref  
              await asyncio.sleep(1)
          else:return False    
          return True
        
      async def inputs(selector, input_=None, selection="click"):
        t=await timeout(selector)
        element=page.locator(selector+">>visible=true")
        await asyncio.sleep(uniform(0.1,0.3))
        await page.tap(selector)
        if selection == "keyboard":
            await page.keyboard.type(input_,delay=uniform(*delay_patt))
        elif selection == "options":
            
            await asyncio.sleep(uniform(0.6,1.2))
            #coords=await element.bounding_box()
            #coords=((coords['x']+coords['width']/2+randint(1,12)),(coords['y']+coords['height']/2+randint(1,20)))
            #await cursor.move_to(*coords)
            await element.select_option(value=input_)    
            await asyncio.sleep(uniform(1,2))
       
      async def fill_OTP(code_selector,resend_selector,retry=0):    
               OTP=await mynumber.OTP(session,40)
               if OTP:
                  await inputs(code_selector,mynumber.otp,"keyboard")  
                  return True
               else:
                    self.Log("basic","Retrieving OTP(2)")
                    print("Re-Trying...")
                    OTP=await mynumber.OTP(session,40)
                    if OTP:
                       await inputs(code_selector,mynumber.otp,"keyboard")
                       return True
                    else:return False
        
   
      async def fetch_tokens(context):

          def get_val(txt,txt2):
             acc_id=txt2.split('=')[1].split('&')[0]  
             for element in txt.split('"'):
              if "EAA" in element:return (acc_id,element)
              else:continue
              
          page = await context.new_page()
          await stealth_async(page)
          try:
           await  page.goto(r'https://www.facebook.com/adsmanager/manage/', wait_until="load",referer="https://www.google.com/",timeout=100000)
          except:
              return True
          a=get_val(page.url,await page.content())
          
      async def dob_fill():
           dob=([('select[id="day"]',human.day),('select[id="year"]',human.year),('select[id="month"]',human.month)])
           shuffle(dob)
           for l in dob:  
            await inputs(l[0],l[1], "options")
           await inputs('button[value="Далее"],button[value="Next"]')  
        
      async def main():
         sub=False
         nonlocal status
        #query=choice(["facebook+reg","facebook+r+.php","facebook signup","signup+for+facebook","join+facebook"])  
        #await  page.goto(r"https://www.google.com/search?q="+choice([query,query.upper()]), wait_until="domcontentloaded",referer="https://www.google.com/",timeout=100000)

         #await page.keyboard.press("Control+Shift+KeyM")
         #await asyncio.sleep(3)
         #await timeout('a[href="https://m.facebook.com/r.php"]',timeout=70)
        # await page.tap('a[href="https://m.facebook.com/r.php"]')
         #try:
         if True:
          await timeout('input[name="firstname"]',timeout=20)   
          await inputs('input[name="firstname"]', human.FN, "keyboard")
          await inputs('input[name="lastname"],input[aria-label="Last name"]', human.LN, "keyboard")
          await inputs('button[value="Далее"],button[value="Next"]')
          await dob_fill()
          await inputs('input[name="reg_email__"]',mynumber.current_number,"keyboard")#
          await inputs('button[value="Далее"],button[value="Next"]')
          await inputs(f'input[value="{human.G}"]') 
          await inputs('button[value="Далее"],button[value="Next"]')
          await inputs('input[id="password_step_input"]', human.password, "keyboard")
          await inputs('button[name="submit"]')
          await timeout('div:has-text("Выполняется создание аккаунта...")',timeout=70)
          try:
              await inputs(choice(['a[role="button"]:has-text("Не сейчас")','button[value="OK"]']))
          except:await asyncio.sleep(100)   
          v=await fill_OTP('input[name="c"]')
          await asyncio.sleep(1000)
          await mynumber.deactivate_current_no(session)
          if v:
              try:
               await cursor.click('button[name="confirm"]')
               await    inputs('a:has-text(Подтвердить)')
               
              except:pass
              status="confirmed"
              human.save_fake(mynumber.current_number,f'{json.dumps(await browser.cookies("https://www.facebook.com/"))}',status,UA,time=self.date)
              
              return True
          else:
              self.Log("imp","Dropped") 
              return False  
      
      try:await main()
      except:await asyncio.sleep(2990)
      
    async def save_to_file(self,txt):
      if os.path.exists(r"\text_files"):pass
      else:
        os.makedirs(r"\text_files")  
      async with aiofiles.open(r"\text_files\\"+str(self.date)+".txt","a",encoding="utf-8") as file:
                await file.write(txt+"\n\n\n\n")
                
        
    async def Pool(self,session):
           
           url=self.api+"GetUpdates?"
           async def updates(allowed_updates):
             asyncio.create_task(self.queue_handler())
             while True:
                [(await self.gen(update,session)) for update in (await (await session.post(url,data={"offset":self.offset})).json())["result"]]
                await asyncio.sleep(0.3)
                  #self.Log("err",e)
                await asyncio.sleep(4)
                continue
           await updates('')

    async def gen(self,update,session):
        
        if update:
         self.offset=update['update_id']+1
         try:   
          message=update["message"]
          if message["chat"]["type"]=="private":
           if 'reply_to_message' in message:self.queue.append(asyncio.create_task(l["reply_to_message"],session))
           else:self.queue.append(asyncio.create_task(self.message_handler(message,session)))
            
         except Exception as e:print(e)#self.Log("err",e)
         
    async def queue_handler(self):
          while True:
            await asyncio.sleep(1000)  
            for l in self.queue: 
             if l==True:
              if l.done():self.queue.remove(l)
       
    async def message_handler(self,message,session):
               
                try:
                  k=message["entities"][0]['type']
                  if k=='bot_command' and message["from"]['is_bot']==False:   
                   t=message['text']
                   c=message["entities"][0]['length']
                   a=t.replace('@ultra_99kbot','')[:c]
                   l=(message,(t[c:]).strip())
                   if await self.Users.find_one({"user":message["from"]["id"]}):
                    if a in self.commands:    
                         self.queue.append(asyncio.create_task(self.commands[a](*l,session=session)))
                   elif a=="/login":await self.login(*l,session=session)
                   else:await self.SendText("PLEASE LOGIN VIA /LOGIN TO ACCESS THE BOT....",message,session,True)
                except exception as e:
                    print("error",e)  
                    #self.Log("err",e)
                 
    async def login(self,message,text,session):
    
             if await self.Users.find_one({"user":message["from"]["id"],"sample":message}): 
              await self.SendText("USER ALREADY ADDED....",message,session,True)
             elif text in self.password:
                   await self.Users.insert_one({"user":message["from"]["id"],"sample":message})
                   await self.SendText("USER ADDED SUCCESSFULLY....",message,session,True) 
             else:await self.SendText("INVALID PASSWORD....",message,session,True)
                  
    async def pause(self,message,text,session):    
                if self.flag==False:  
                 await self.SendText("RESUMING...",message,session,True)
                 self.flag==True
                else:
                 await self.SendText("ALREADY STARTED...",message,session,True)
                 
    async def resume(self,message,text,session):
                if self.flag==False:  
                 await self.SendText("ALREADY PAUSED..",message,session,True)
                else:
                 self.flag=False   
                 await self.SendText("PAUSING...",message,session,True)
                 
    async def shutdown(self,message,text,session):
    
          if text in self.password:  
           self.flag="quit"
           await self.SendText("SERVICE SHUTTING DOWN...",message,session,True)
          else:await self.SendText("PLEASE TRY WITH A VALID PASSWORD...",message,session,True)

    async def SendText(self,text,mess,session,reply=False,pin=False):
           chat_id=mess['chat']['id']
           if reply==True:
              params={"chat_id":chat_id
                      ,"text":text
                      ,"allow_sending_without_reply":True,
                      "reply_to_message_id":mess['message_id']}
              msg=(await (await session.post(self.api+"sendMessage",data=params)).json())["result"]
                  
           else:    
              params={"chat_id":chat_id,"text":text}
              msg=(await (await session.post(self.api+"sendMessage",data=params)).json())["result"]
              
           if pin:
               m=await self.PinMessage(msg,session)  
              
    async def export_all(self,message="",text="",session=None,query={}):
        if await self.Accounts.find_one():
             
          async with aiofiles.open(r"temp_data\Last_Export.txt","w",encoding="utf-8") as file:     
            async for user in self.Accounts.find(query):#{user['account_id']
                
               text=f"{user['contact']}:{user['password']}\n{user['cookie']}\n{user['User-Agent']}\n\n\n" 
               await file.write(text)
            
          if session:    
            async with aiofiles.open(r"temp_data\Last_Export.txt","rb") as file:
             txt=aiohttp.FormData()
             txt.add_field("chat_id",str(message['chat']['id']))
             txt.add_field('document',file,  
                         filename='data.txt',
                         content_type='text/plain')
             txt.add_field("reply_to_message_id",str(message['message_id']))
             r=await session.post(self.api+'sendDocument',data=txt)
        else:await self.SendText("No Accounts made yet.",message,session)   
          
    async def export(self,message,text,session):
        if await self.Accounts.find_one({"time_created":str(self.date)}):
         await self.export(message,text,session,{"time_created":self.date})
        else :await self.SendText("No Accounts made today.",message,session) 
         
    async def PinMessage(self,msg,session):
               params={"chat_id":msg["chat"]["id"],
                       "message_id":msg['message_id']}
               await session.post(self.api+"pinChatMessage",data=params)
    
    async def Status(self,message,text,session):
            
             param = {"api_key": API_KEYS["smshub"],
                     "action": "getBalance",
                     }
             url=r"https://smshub.org/stubs/handler_api.php"
 
             all_=await asyncio.gather( session.post(url, params=param),self.Accounts.estimated_document_count(),self.Accounts.count_documents({"status":"confirmed"}))
             current=await asyncio.gather(self.Accounts.count_documents({"time_created":self.date}),self.Accounts.count_documents({"time_created":self.date,"status":"confirmed"}),)
             try:                  
              response =((await(all_[0]).text()).split(':')[1])
          
              text=f"Status:\nALLTIME-----\nTotal:{all_[1]}\nConfirmed:{all_[2]}\nPending: {all_[1]-all_[2]}\n\nTODAY----\nTotal:{current[0]}\nConfirmed:{current[1]}\nPending:{current[0]-current[1]}\n\nBALANCES----\nSmsHub : {response}"
              await self.SendText(text,message,session,True)           
             except Exception as e:print(e)
             

au = facebook_auto(True)
asyncio.run(au.req_pool())

"""  await asyncio.gather( 
   page.fill('[aria-label="First name"]',"Johan"),#First Name
   page.fill('[aria-label="Surname"]',"Mohan"),
   page.fill('[aria-label="Mobile number or email address"]',+919410906559),
   page.fill(,"Swbwkd%7309"),
   page.select_option('[aria-label="Day"]',"21"),
   page.select_option('[aria-label="Year"]',"2001"),
   page.select_option('[aria-label="Month"]',"11")
  )
  """
# client=motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017/')
# human=fake_human(client["FACEBOOK"])


# <span class="x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x14z4hjw x3x7a5m xngnso2 x1qb5hxa x1xlr1w8 xzsf02u x1yc453h" dir="auto">Help us confirm that it's you</span>
# <div class="recaptcha-checkbox-border" role="presentation" style=""></div>
# <span class="x1lliihq x6ikm8r x10wlt62 x1n2onr6 xlyipyv xuxw1ft">Continue</span>
