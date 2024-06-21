import aiohttp
import os
import asyncio
import re
import aiofiles
async def curl_image(name):
   async with aiohttp.ClientSession() as session: 
    url=r"https://thispersondoesnotexist.com/image"  
    resp = await session.get(url)
    path='images\\'
    if os.path.exists(path):pass
    else:os.makedirs(path)
    path += f'{name}.jpg'
    async with aiofiles.open(path,"wb") as f:
        data = await resp.read()
        await f.write(data)
        print(data)
    return path

with open("testfile.txt") as t:
      l=t.read()
def get_val(txt,txt2):
 acc_id=txt2.split('=')[1].split('&')[0]  
 for element in txt.split('"'):
  if "EAA" in element:return (acc_id,token)
  else:continue
   
txt2="https://www.facebook.com/adsmanager/manage/campaigns?act=1388680614869005&nav_source=no_referrer"  

print(e)
print("o")
print(clean(l))


    

