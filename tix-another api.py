from playwright.async_api import async_playwright
from playwright_stealth import stealth_async
import asyncio,pandas as pd
from random import choice
from json import dumps,loads

import os
from time import time

proxy_base="http://geo.iproyal.com:12321"
links=pd.read_csv("../axs_event_ids.csv")["event_id"]
UA=[
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:97.0) Gecko/20100101 Firefox/97.0",
    "Mozilla/5.0 (X11; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:97.0) Gecko/20100101 Firefox/97.0",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:97.0) Gecko/20100101 Firefox/97.0",
    "Mozilla/5.0 (X11; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0"
]
def write_to_json(context):
     async def write(data):
        context.write(dumps(data)+",")
     return write      


def generate_UA():return choice(UA)


class Interceptor():
  
  def __init__(self,tries=3):
     self.queue=[]
     self.tries=tries
     self.open=1
     self.output="["

  async def main(self,input,tabs=1,proxy={"server": "http://geo.iproyal.com:12321", "username": IPROYAL_USER, "password": IPROYAL_PASS},callback=write_to_json,path="output.json"):
    
    self.inputs=input
    self.path=path
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=False)
        self.context = await browser.new_context(proxy=proxy)
        await(asyncio.gather(*[self.handle_response() for x in range(0,tabs)]))
        while self.queue:
             if self.queue[-1].done():self.queue.pop()
             else :await asyncio.sleep(2)
        await self.context.close()  
        self.output+="]"
        callback(self.output)
    

  async def intercept_requests(self,route,request,page):
    await route.continue_()
    if "/veritix/inventory/v4/" in request.url and "/price" in request.url:
        print("Request Intercepted")
        url = request.url.replace("/veritix/inventory/v4/", "/veritix/inventory/v2/") 
        await route.continue_(url=url)
    
  async def handle_response(self):
        page = await self.context.new_page()
        await page.set_extra_http_headers({
            'User-Agent':(generate_UA())
         })
        await stealth_async(page)
        data=dict()
        
        async def handle(response):
           url=response.url
           if("v2" in url):ver="v2"
           else: ver="v4"
           if ('inventory/' in url and '/price' in url) :
              text=await response.text()
              data["{ver}_price"]=loads(text)
              message = {"type": "FROM_PAGE5", "text":text}
              await page.evaluate(f'window.postMessage({dumps(message)}, "*")')
              print("0")
           elif ("/inventory/" in url) and  ("/sections?" in url):
               text=await response.text()
               data["{ver}_sections"]=loads(text)
               print(text)
               message = { "type": "FROM_PAGE6","text":text }
               await page.evaluate(f'window.postMessage({dumps(message)}, "*")')
               print("1")        
           elif ("/api/event_listings_v2" in url):
               text=await response.text()
               data["listings_{ver}"]=loads(text)
               message = { "type": "FROM_PAGE7","text":text }
               await page.evaluate(f'window.postMessage({dumps(message)}, "*")')
               print("2")         
           elif ("/v3/axs/events" in url):
               text=await response.text()
               message = ({ "type": "FROM_PAGE14","text":text })
               data["v3_events_{ver}"]=loads(text)
               print("3")
               await page.evaluate(f'window.postMessage({dumps(message)}, "*")')
                          
       
        await page.route("**", lambda route,request:self.queue.append(asyncio.create_task(self.intercept_requests(route,request,page))))
        page.on('response',handle)
        tout=0
        while(self.inputs):   
           url=self.inputs.pop()
           print(url)           
           tries=0
           await page.goto(url)
           locator=page.locator('button[id="tickets-search"]')
           ctime=time()
         
           while((not (await locator.is_visible() or data))):
              if(tries>self.tries or (time()-ctime)>20):break
              
              loc2=page.locator('div[class="modal-content"] button')
              cookies=page.locator("button[id='onetrust-accept-btn-handler']")
              notinsale=page.locator('div[id="EXCEPTION_MESSAGE"]')
               #onetrust-accept-btn-handler
              if(await cookies.is_visible()):
                await asyncio.sleep(1)
                try:
                 await cookies.click()
                 self.inputs.append(url)
                except:pass
              if(await page.is_visible('img[class="header-banner"]')):
                 await asyncio.sleep(4)
                 break
              if (await loc2.is_visible()):
                 await loc2.click()
              elif (await notinsale.is_visible()):
               await page.goto(url)
               tries+=1    
           await asyncio.sleep(15)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
               
           self.output+=dumps(data)+","
           self.open=0
           data={}   
    
        
if __name__=="__main__":
   inputs=list(links)
   
   #patterns=[r"inventory/v4",r"inventory/v2"]
   session=Interceptor()                               
   asyncio.run(session.main(input=inputs))
