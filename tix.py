from playwright.async_api import async_playwright
from playwright_stealth import stealth_async
import asyncio,pandas as pd
from random import choice
from json import dumps,loads
import aiofiles
import os

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
      await context.write(dumps(data))
     return write      


def generate_UA():return choice(UA)


class Interceptor():
  
  def __init__(self):
     self.queue=[]

  async def main(self,input,tabs=4,proxy={"server": "http://geo.iproyal.com:12321", "username": IPROYAL_USER, "password": IPROYAL_PASS},callback=write_to_json,path="output.json"):
    
    self.inputs=input
    self.path=path
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=False)
        self.context = await browser.new_context(proxy=proxy)
        await(asyncio.gather(*[self.handle_response() for x in range(0,tabs)]))
        while self.queue:
             if self.queue[-1].done():self.queue.pop()
             else :asyncio.sleep(2)
        await self.context.close()  

  async def intercept_requests(self,route,request,page):
    await route.continue_()
    if "/veritix/inventory/v4/" in request.url and "/price" in request.url:
        print("Request Intercepted")
        url = request.url.replace("/veritix/inventory/v4/", "/veritix/inventory/v2/") 
        await route.continue_(url=url)
    
  async def handle_response(self):
        page = await self.context.new_page()
        await stealth_async(page)
        await page.set_extra_http_headers({
            'User-Agent':(generate_UA())
         })
        data=dict()
        
        async def handle(response):
           url=response.url
           if ('inventory/v2' in url and '/price' in url) :
              text=await response.text()
              data["v2_price"]=loads(text)
              message = {"type": "FROM_PAGE5", "text":text}
              await page.evaluate(f'window.postMessage({dumps(message)}, "*")')

           elif ("/inventory/" in url) and  ("/sections?" in url):
               text=await response.text()
               data["v2_sections"]=loads(text)
               message = { type: "FROM_PAGE6","text":text }
               await page.evaluate(f'window.postMessage({dumps(message)}, "*")')
                       
           elif ("/api/event_listings_v2" in url):
               text=await response.text()
               data["listings_v2"]=loads(text)
               message = { type: "FROM_PAGE7","text":text }
               await page.evaluate(f'window.postMessage({dumps(message)}, "*")')
                        
           elif ("/v3/axs/events" in url):
               text=await response.text()
               message = str({ type: "FROM_PAGE14","text":text })
               data["v3_events"]=loads(text)
               print(text," 3")
               await page.evaluate(f'window.postMessage({dumps(message)}, "*")')
                          

        await page.route("**", lambda route,request:self.queue.append(asyncio.create_task(self.intercept_requests(route,request,page))))
        page.on('response',handle)
         
        async with aiofiles.open(self.path,mode='a') as file: 
         callback=write_to_json(context=file)   
         while(self.inputs):   
           url=self.inputs.pop()           
           await page.goto(url)
           locator=page.locator('button[id="tickets-search"]')
           while((not (await locator.is_visible() or data))):await asyncio.sleep(1)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
           await asyncio.sleep(4)
           await callback(data)
           data={}
        await page.close()
    
if __name__=="__main__":
   inputs=[r"https://tix.axs.com/vnAGDAAAAAAkfo6dAwAAAABA%2fv%2f%2f%2fwD%2f%2f%2f%2f%2fA2F4cwD%2f%2f%2f%2f%2f%2f%2f%2f%2f%2fw%3d%3d",r"https://tix.axs.com/vnAGDAAAAAAkfo6dAwAAAABA%2fv%2f%2f%2fwD%2f%2f%2f%2f%2fA2F4cwD%2f%2f%2f%2f%2f%2f%2f%2f%2f%2fw%3d%3d"]
   inputs.append(inputs[0])
   inputs.extend(inputs)
   
   #patterns=[r"inventory/v4",r"inventory/v2"]
   session=Interceptor()                               
   asyncio.run(session.main(input=inputs))
