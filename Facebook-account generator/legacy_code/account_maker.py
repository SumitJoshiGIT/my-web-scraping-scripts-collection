from playwright.async_api import async_playwright
from playwright_stealth import stealth_async
import motor.motor_asyncio
import aiohttp
import json

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
        
        capt=captcha()
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
        def browser():
           while True :
            for x in ["chromium","firefox"]:
                yield x
        browsers=browser()
        self.Accounts=self.client["FACEBOOK"]["ACCOUNTS"]
               
        async with async_playwright() as p:
          async with aiohttp.ClientSession() as session:
             if self.bot==True:
              print("Bot:True")   
              asyncio.create_task(self.Pool(session))   
             browser = await p['firefox'].launch(headless=False,args=args,proxy=proxy)
             agents=user_agent('firefox')
             
             for agent in agents:
               print(agent)
               await self.change_ip(session)
               self.current_log={}
               ref=time()
               browser_= await browser.new_context(ignore_https_errors=True,locale='ru-mo',timezone_id='Europe/Chisinau',viewport=choice([{"width":1280,"height":720},{"width":1366,"height":768}]))#)#,    
               val=None
               #try:
               
               val=await self.register_account(browser_,
                                         human=fake_human(self.client["FACEBOOK"]),
                                         captcha_=capt,
                                         session=session,                         
                                         UA=agent)
               
               print(val)  
              
               #except Exception as e:print(e)#self.Log("err",e)
               self.Log('imp',"Done :"+str(time()-ref))
               if self.bot:                 
                 message="----------LOGS---------\n"+('\n'.join([f"{l}:{self.current_log[l]}" for l in self.current_log]))
                 try:pass#[await self.SendText(message,user["sample"],session) async for user in self.Users.find()]
                 except Exception as e:print(e)
               try: pass   
               #  await logs[self.date].insert_one(self.current_log)
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
               
               
    async def register_account(self, browser,human,captcha_,session,UA):
     
      await browser.set_extra_http_headers(UA)
      datetime=extract(dt.datetime.today())
      date=datetime[0]
      self.date=date
      await human.human()
      status=None
      mynumber=number()
      pin=False
      #contact=await mynumber.get_number(session=session)
      mynumber.current_number="fdfd"
      page = await browser.new_page()
      await stealth_async(page)
      self.Log("basic",date+","+datetime[1]+"////"+str(mynumber.current_number))  
      cursor=create_cursor(page)
      print(UA)
      async def inputs(selector, input_=None, selection="click"):
        element=await page.wait_for_selector(selector)
        await cursor.click(selector)
        await asyncio.sleep(uniform(0.2,0.5))
        if selection == "keyboard":
            await page.keyboard.type(input_,delay=uniform(40,50))
        elif selection == "options":
            await asyncio.sleep(uniform(0.6,1.2))
            await element.select_option(value=input_)    
            await asyncio.sleep(uniform(1,2))

      async def button(selector,nav=True,n=0,sub1=False):
        element=await page.wait_for_selector(selector) 
        #box=await button_.bounding_box()
        await cursor.click(selector)
        await page.wait_for_load_state("domcontentloaded")
        if sub1==True :
          m=n+1
          await asyncio.sleep(4)

          try:
           while  await page.is_visible(selector): 
                #if n==0:
                 ##    return False      
                if n>0:
                    if await page.is_visible('[id="reg_error"]'): 
                     self.Log("imp","Error occured on fb server end")
                    else:self.Log("err","Submit not working...")
                    return False
                m+=1
                #try:await button(selector,n=m,sub1=True)
                #except:return True
           return True 
          except:return True   
            
      async def fill_OTP(code_selector,resend_selector,retry=0):    
               OTP=await mynumber.OTP(session,40)
               if OTP:
                  await inputs(code_selector,mynumber.otp,"keyboard")  
                  return True
               else:
                    try:
                     await button(resend_selector)
                     await button('a[role="button"]:has-text("OK")')
                    except Exception as e:print(e)
                    self.Log("basic","Retrieving OTP(2)")
                    print("Re-Trying...")
                    OTP=await mynumber.OTP(session,40)
                    if OTP:
                        
                       await inputs(code_selector,mynumber.otp,"keyboard")
                       return True
                    else:
                       await mynumber.deactivate_current_no(session)
                       return False
        
      async def captcha_solve(check=1):
           nonlocal status                   
           path=None
           cap=CaptchaSolve(page)
           if check==1:   
       # if await page.locator('span:has-text("We need more information")').is_visible():
            try:await button('div[aria-label="Продолжить"],div[aria-label="Continue"]')
            except Exception as e:
                if check==1:
                 self.Log("err","No Captcha Found after the first Form...")   
                 raise ValueError("Error to stop the check" )             
                else:await button('[aria-label="Disagree With Decision"],[aria-label="Не согласиться с решением"]')
            await page.wait_for_load_state("domcontentloaded") 
            await asyncio.sleep(uniform(3.4,4.8))
            
            try:
             c=await cap.start()
             if not c:
                 self.Log("err","Captcha Solving Failed...")
                 raise ValueError("Error to stop the check" )
            except Exception as e:
                print(e,"kk")     
            return True
            self.Log("imp","Captcha Resolved!")
            try:    
             await button('div[aria-label="Продолжить"],div[aria-label="Continue"]')
             await inputs('input[name="contactpoint"]',f"{human.FN+human.L+randint(100,900)@gmail.com}","keyboard")#mynumber.current_number
             await button('div[aria-label="Отправить код для входа"],div[aria-label="Send Login Code"]')
             otp=await fill_OTP('input[autocomplete="one-time-code"]','text="Отправить SMS еще раз"')#'text="Resend confirmation code"
             if otp==False:
                 self.Log("err","Dropped due to no otp")
                 return False
             await button('div[aria-label="Далее"]>>nth=1')#div[aria-label="Next"]>>nth=1
             await page.wait_for_load_state("domcontentloaded")
             
            except  Exception as e:print(e)
            await asyncio.sleep(uniform(0.3,3.4))
            
            try:
                  
                b=await button('div[aria-label="Go to Facebook"],div[aria-label="Перейти на Facebook"]')
 
                self.Log("imp","Account Generated after Captcha Check...")
                status="confirmed"
                path=None
                await human.save_fake(mynumber.current_number,f'{json.dumps(await browser.cookies("https://www.facebook.com/"))}',status,UA,time=self.date) 
                return True
            except Exception as e:  
                print(e)
                check=3
                
           if check==3 or check==2:
                try:await button('[aria-label="Disagree with decision"],[aria-label="Не согласиться с решением"]',False)
                except:pass 
                await asyncio.sleep(uniform(2.6,3.8))
                try:
                    await page.wait_for_load_state("domcontentloaded")
                except Exception as e:print(e)
                if check==2:
                   try: 
                    c=await cap.start()
                   except:pass 
                async with page.expect_file_chooser() as fc_info:
                    await button('div[aria-label="Upload Image"],div[aria-label="Загрузить изображение"],div[aria-label="Upload image"]')
                    file_chooser = await fc_info.value
                    self.Log("imp","Account's status is:Pending")
                path=await curl_image(session,mynumber.current_number)    
                try:     
                 await file_chooser.set_files(path)
                 await button('div[aria-label="Продолжить"],div[aria-label="Continue"]')
                except Exception as e:print(e)
                  
                await page.wait_for_load_state("domcontentloaded")
                await asyncio.sleep(12)
                 
                status = "pending"  
                await human.save_fake(mynumber.current_number,f'{json.dumps(await browser.cookies("https://www.facebook.com/"))}',status,UA,time=self.date) 
                
           self.Log("imp","Passed Captcha Check")            
           return True

      async def fetch_tokens(context):

          def get_val(txt,txt2):
             acc_id=txt2.split('=')[1].split('&')[0]  
             for element in txt.split('"'):
              if "EAA" in element:return (acc_id,element)
              else:continue
              
          page = await context.new_page()
          await stealth_async(page) 
          await  page.goto(r'https://www.facebook.com/adsmanager/manage/', wait_until="load",referer="https://www.google.com/",timeout=100000)
          await asyncio.sleep(30)
          a=get_val(page.url,await page.content())
          input()
          print(a)
                
      async def main():
         sub=False
         nonlocal status
         await  page.goto(r'https://www.facebook.com/signup', wait_until="domcontentloaded",referer="https://www.google.com/",timeout=100000)
         try: 
          await inputs('input[name="firstname"]', human.FN, "keyboard")
          await inputs('input[name="lastname"],input[aria-label="Last name"]', human.LN, "keyboard")
          k= f"{choice(['internet','paveman','spiderman','humanly','superhero'])+str(randint(100,900))}@gmail.com" 
          await inputs('input[name="reg_email__"]',k,"keyboard")#mynumber.current_number
          await inputs('input[name="reg_email_confirmation__"]',k,"keyboard")
          await inputs('input[id="password_step_input"]', human.password, "keyboard")
          dob=([('select[id="day"]',human.day),('select[id="year"]',human.year),('select[id="month"]',human.month)])
          shuffle(dob)
          for l in dob:   
            await inputs(l[0],l[1], "options")
            
          await inputs(f'input[value="{human.G}"]')
         except Exception as e:
             print(e)
             try:
                 await page.wait_for_selector('h2:has-text("You’re Temporarily Blocked"),h2:has-text("У вас уже есть аккаунт Facebook?")')
                 self.Log("err","IP BLOCKED")
                 #input("Press any key to continue...")
             except:self.Log("err","Form Failed abruptly")
             await mynumber.deactivate_current_no(session)
             return None
        
         sub=await button('button[name="websubmit"]',sub1=True)
         #await asyncio.sleep(uniform(4.7,6.5))
         
             
         if sub==True:
              #await asyncio.sleep(uniform(1.7,2.5))
              self.Log("imp","First Form Submitted...")
              
              try:
                await captcha_solve(1)  
                self.Log("basic","First Captcha Check....")   
            
              except:
               self.Log("basic","Direct path detected..")  
               try:
                   await page.wait_for_selector('input[id="code_in_cliff"],input[id="code"]')
                   #_1st=await fill_OTP('input[id="code_in_cliff"],input[id="code"]','a:has-text("Send SMS Again")')
                   print("--direct")
                   return True
               except:
                   print("--cap")
                   return False 
               if _1st==True:
                 try: 
                  await cursor.click('button[name="confirm"]')
                 except Exception as e: print(e)       
                 try:
                    await captcha_solve(2)
                    self.Log("basic","Second Captcha Check Passed...")    
                 except Exception as e:
                    print(e)
                    status="confirmed"
                    await human.save_fake(mynumber.current_number,f'{json.dumps(await browser.cookies("https://www.facebook.com/"))}',status,user_agent=UA["User-Agent"],time=self.date)   
                    self.Log("imp","Account Created.")
               else:self.Log("imp","Dropped as no otp recieved")  
         else:
              self.Log("err","First Form failed")
         return True     
         print("status:",status)
         if status=="confirmed" or status=="pending":
          pin=True#:{human.fake["account_id"]}\n{human.fake["token"]}
          message=f'{human.fake["contact"]}:{human.fake["password"]}\n{human.fake["cookie"]}\n{human.fake["User-Agent"]}'    
          await self.save_to_file(message)
          try:
           [await self.SendText(message,user["sample"],session,pin=True) async for user in self.Users.find()]
          except Exception as e:print(e)
          await mynumber.deactivate_current_no(session,True) 
          return True 
         else:
           status="dropped"
           human.fake.update({"status":"dropped"})
           await mynumber.deactivate_current_no(session)
           return False
         print( page.url)    
         await page.close()
         if status=="confirmed":
           info=await fetch_tokens(browser)
           print(info)
            
            
      #try:  
      return await main()
      #except Exception as e:print(e)
      
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
             
   # async def currentStatus(self,)   
      
# CAPTCHA

au = facebook_auto(True)
asyncio.run(au.req_pool())

# client=motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017/')
# human=fake_human(client["FACEBOOK"])


# <span class="x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x14z4hjw x3x7a5m xngnso2 x1qb5hxa x1xlr1w8 xzsf02u x1yc453h" dir="auto">Help us confirm that it's you</span>
# <div class="recaptcha-checkbox-border" role="presentation" style=""></div>
# <span class="x1lliihq x6ikm8r x10wlt62 x1n2onr6 xlyipyv xuxw1ft">Continue</span>
