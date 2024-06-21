import asyncio
from playwright.async_api import async_playwright
from aiohttp import request
import time
import pandas as pd
from playwright_stealth import stealth_async


class MapsScrapper():
 def __init__(self,cpu_limit,load_factor):
     self.clim = cpu_limit
     self.tlim= 5000
     if(cpu_limit*load_factor>5):self.tlim=cpu_limit*load_factor*1000
     self.proxy={}

 async def link_scrapper(self,arg):
         links=[]
         await self.page.goto(f"https://www.google.com/maps/search/{arg}")
         #await self.page.evaluate("document.body.style.zoom='50%'")
         feeds=self.page.locator('div[role="feed"]')
         element=self.page.locator("text=You've reached the end of the list")
         while(await element.is_visible()==False):
            await feeds.evaluate('element => element.scrollTop += 2000')
         link_elements=(await feeds.locator('a').all())[1:]
         for link in link_elements:
            lin=await link.get_attribute('href')
            if(r"/reserve" not in lin) : 
             links.append((lin,await link.get_attribute('aria-label')))
         return links
       
 async def info_scrapper(self):
   page=await self.browser.new_page() 
   await stealth_async(page)
   address=""
   menu_link=""
   phone_number=""
   pluscode=""
   website=""
   located_in=""
   rating=""
   timings=""
   latitude=""
   longitude=""
   reviews=""
   price=""
   description=""
   about_dict={
     "service_options":"",
     "no_service_options":"",
     "offerings":"",
     "no_offerings":"",
     "amenities":"",
     "no_amenities":"",
     "atmosphere":"",
     "no_atmosphere":"",
     "crowd":"",
     "no_crowd":"",
     "parking":"",
     "no_parking":"",
     "children":"",
     "no_children":"",
     "popular_for":"",
     "no_popular_for":"",
     "highlights":"",
     "no_highlights":"",
     "pets":"",
     "no_pets":"",
     "dining_options":"",
     "no_dining_options":"",
     "activities":"",
     "no_activities":"",
     "Others":"",
     "no_Others":""     
   }

   while self.queue:
     try:
      link=self.queue.pop() 
      x=link[0]
      try:
         await page.goto(x,wait_until='domcontentloaded')
         f=0
         while(page.url==x or f<3):
           await asyncio.sleep(0.1)
           f+=0.1 
      except:pass
      
      page.set_default_timeout(1300)
     
      try:
         address=await page.locator('[data-item-id="address"]').text_content()
         pluscode=await page.locator('[data-item-id="oloc"]').nth(0).text_content()
      except:pass
      
      try:
         website=await page.locator('[data-item-id="authority"]').nth(0).text_content()
         menu_link=(await page.locator('[data-item-id="menu"]').nth(0).text_content()).replace('Menu','')
      except:pass
      
      try:
         phone_number=(await page.locator('[data-tooltip="Copy phone number"]').nth(0).get_attribute("aria-label")).replace('Phone:',"")   
         try:timings=await page.locator('table[class="eK4R0e fontBodyMedium"]').inner_text()
         except:timings=await page.locator('[data-item-id="oh"]').nth(0).get_attribute("aria-label")
         
      except:pass 

      try:
        rating=(await page.locator('div[aria-label$="stars"]').nth(0).get_attribute("aria-label")).replace('stars',"")
        reviews=(await page.locator('span[aria-label$="reviews"]').nth(0).get_attribute('aria-label')).replace('reviews',"")
        price=(await page.locator('span[aria-label^="Price"]').nth(0).inner_text())  
      except:pass
      
      try:
       url_split=(page.url).split('/@')[1].split(',')
       latitude=url_split[0]
       longitude= url_split[1]
      except:pass

      try:
         try:await page.click('[aria-label^="About"]')
         except:pass
         await asyncio.sleep(1)
         try:description=await page.locator('div[aria-live="polite"][aria-expanded=true]').text_content()
         except:pass    
         data = await page.locator('div[class="iP2t7d fontBodyMedium"]').all()
         buffer=""
         if data:
            for x in data:
               temp = (await x.locator('h2').text_content()).lower().strip().replace(' ','_')                            
               if temp in  about_dict:
                for y in (await x.locator( 'li[class="hpLkke "]').all()):buffer+= await y.text_content() + ","
                about_dict.update({temp:buffer})
                buffer=""
                for y in (await x.locator('li[class="hpLkke WeoVJe"]').all()):buffer+= (await y.text_content() + ",")
                about_dict.update({"no_"+temp:buffer})   
                buffer=""
         else:
            for x in (await page.locator('div[class="CK16pd"]').all()):buffer+=await x.text_content()+","
            about_dict.update({"others":buffer})
            buffer=""
            for x in await (page.locator('div[class="CK16pd fyvs7e"]').all()):buffer+=await x.text_content()+","
            about_dict.update({"no_others":buffer})
            
      except Exception as err:print("Error:",err)
      page.set_default_timeout(self.tlim)
      data_dict=[
         link[1]      ,
         page.url     ,
         rating       ,
         timings      ,
         menu_link    ,
         longitude    ,
         latitude     ,
         website      ,
         phone_number ,
         pluscode     ,
         address      ,
         located_in   ,
         reviews      ,
         price        ,
         description  ,
         about_dict['service_options'],
         about_dict['no_service_options'],
         about_dict['offerings'],
         about_dict['no_offerings'],
         about_dict['amenities'],
         about_dict['no_amenities'],
         about_dict['atmosphere'],
         about_dict['no_atmosphere'],
         about_dict['crowd'],
         about_dict['no_crowd'],
         about_dict['parking'],
         about_dict['no_parking'],
         about_dict['children'],
         about_dict['no_children'],
         about_dict['popular_for'],
         about_dict['no_popular_for'],
         about_dict['highlights'],
         about_dict['no_highlights'],
         about_dict['pets'],
         about_dict['no_pets'],
         about_dict['dining_options'],
         about_dict['no_dining_options'],
         about_dict['activities'],
         about_dict['no_activities'],
         about_dict['Others'],
         about_dict['no_Others']
      ]
      self.results.append(data_dict)
   
     except:pass
   await page.close()


 async def fetch_results(self,search_parameter):
    async with async_playwright() as p:
        args=[
        '--deny-permission-prompts',
        '--no-default-browser-check',
        '--no-nth-run',
        '--disable-features=NetworkService',
        '--deny-permission-prompts',
        '--disable-popup-blocking',
        '--ignore-certificate-errors',
        '--no-service-autorun',
        '--password-store=basic',
        '--disable-audio-output',
        '--blink-settings=imagesEnabled=false'
        '--blink-settings=fonts=!',
        '--disable-javascript',
        "--high-dpi-support=0.50",
        "--force-device-scale-factor=0.50"
        ]
        self.browser = await(await p.chromium.launch(args=args,headless=True)).new_context(viewport={"width": 400, "height": 2800})
        self.browser.set_default_timeout(0)
        print("Started")
        if(type(search_parameter)==str): 
         self.page = await self.browser.new_page()
         await stealth_async(self.page)
         tries=0
         while(True):
          if(tries>3):
            raise TimeoutError("Network too slow.") 
          try:
             self.queue=await self.link_scrapper(search_parameter)
             break
          except:tries+=1
         await self.page.close()
        else:self.queue=search_parameter
          
        self.results=[]
        ctime=time.time()
        tries=len(self.queue)
        print("No of items : ",len(self.queue))
        tasks=[]
        tabs=self.clim
        while tabs:
           tasks.append(asyncio.ensure_future(self.info_scrapper()))
           tabs-=1
        await asyncio.gather(*tasks)
        print("No. of fails: ",tries-len(self.results))
        print("TimeTaken:",time.time()-ctime)
        await self.browser.close()   

if __name__=='__main__':
 search="restaurant in Paris"
 mp=MapsScrapper(10,0.3)
 asyncio.run(mp.fetch_results(search))
 cols=[  "name",
         "gmap_url ",
         "rating",
         "timings",
         "menu_link ",
         "longitude ",
         "latitude ",
         "website",
         "phone_number",
         "pluscode ",
         "address",
         "located_in",
         "reviews",
         "price",
         "description",
         'service_options',
         'no_service_options',
         'offerings',
         'no_offerings',
         'amenities',
         'no_amenities',
         'atmosphere',
         'no_atmosphere',
         'crowd',
         'no_crowd',
         'parking',
         'no_parking',
         'children',
         'no_children',
         'popular_for',
         'no_popular_for',
         'highlights',
         'no_highlights',
         'pets',
         'no_pets',
         'dining_options',
         'no_dining_options',
         'activities',
         'no_activities',
         'Others',
         'no_Others'
        ]
 
 dataframe=pd.DataFrame(mp.results,columns=cols)
 print(dataframe)