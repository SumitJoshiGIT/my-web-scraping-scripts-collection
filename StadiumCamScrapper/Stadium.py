import datetime as dt 
import aiohttp
import aiofiles
import asyncio
import os

class image_logger:

 def __init__(self,url): 
    self.latest_time=None
    self.latest_image=''
    self.url=url
    print(f"Executing CamScrapper.py from:\n {os.getcwd()}\n TargetUrl:{url}")

 def Log(self,data):
     print(data[0],data[1])
     
 def main(self):
      async def run():   
        try:   
         async with aiohttp.ClientSession() as Session:
           while True: 
            if await self.time_check(dt.datetime.today(),4.2):
               if self.latest_image:    
                 images=await asyncio.gather(self.curl_img(Session),self.load_last_image())
                 if self.duplicate_check(*images)!=True:
                     await self.save_file(images[0])
                 else:
                     await(asyncio.sleep(60))
               else:
                  images=await self.curl_img(Session)     
                  await self.save_file(images)
        except Exception as error:
          self.Log(("[Error]",error))
      asyncio.run(run())                
                
 async def time_check(self,current_time,difference):
   if self.latest_time: 
    diff=((current_time-self.latest_time).seconds)/60
    if diff>=difference:return True
    else:
       await asyncio.sleep(abs((difference-diff)*60))
       return True
   else:  return True

 def duplicate_check(self,img,response):
    if img==response:
        return True  
 
 async def curl_img(self,Session,url=None):
       if url==None:url=self.url
       else:url=url
       time=dt.datetime.today()
       async with Session.get(url) as resp:
          return await resp.read()
 
 def extract(self,o):      
     date=f"{o.day}_{o.month}_{o.year}"
     time=f"{o.hour}_{o.minute}_{o.second}"
     return (date,time)

 async def save_file(self,response):    
            self.latest_time=dt.datetime.today()
            date,time=self.extract(self.latest_time)
            path=f"images\\{date}\\"
            if os.path.exists(path):pass
            else:
                os.makedirs(path)
                self.Log(("++Created:",path))
            path+=f"{time}.jpg"
            self.latest_image=path
            async with aiofiles.open(path,"wb")  as img:
                await img.write(response)
            self.Log((">>Saved:",path))
            
 async def load_last_image(self):
     async with aiofiles.open(self.latest_image,"rb")  as img:
        return await img.read()
    
obj=image_logger("https://informo.madrid.es/cameras/Camara06306.jpg")
obj.main()

