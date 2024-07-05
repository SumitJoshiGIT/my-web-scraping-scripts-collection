from requests import post 
import aiohttp
import asyncio
from bs4 import BeautifulSoup
from PIL import Image,ImageFilter,ImageEnhance
import pytesseract
from io import BytesIO
from json import dumps 
import numpy as np
import cv2
import easyocr
import aiofiles
from random import choice 
from aiohttp import FormData
from collections import Counter

proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}

base_url =r"https://bbmptax.karnataka.gov.in/Forms/PrintForms.aspx?rptype=3"

user_agents =([
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"
    ])

application_numbers = [
    "1500000034",
    "1500000037", 
    "1500000070 "
   
]
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'en-US,en;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Referrer-Policy':'strict-origin-when-cross-origin'
    ,'Content-Type': 'application/x-www-form-urlencoded',
    'Host': 'bbmptax.karnataka.gov.in',
    'Origin': 'https://bbmptax.karnataka.gov.in',
    'Referer': 'https://bbmptax.karnataka.gov.in/Forms/PrintForms.aspx?rptype=3',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests':'1'
}
reader=easyocr.Reader(['en'],gpu=False)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
def process_results(pil_image,app_num):
    results=[]
    image = np.array(pil_image)
    results.append(reader.readtext(image,allowlist ='0123456789')[0])  
    image = image[:, :, ::-1].copy()
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    results.append(reader.readtext(image,allowlist ='0123456789')[0])  
    _,image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    results.append(reader.readtext(image,allowlist ='0123456789')[0])  
    image=cv2.equalizeHist(image)
    results.append(reader.readtext(image,allowlist ='0123456789')[0])  
    image = cv2.GaussianBlur(image, (3, 3), 0)
    results.append(reader.readtext(image,allowlist ='0123456789')[0])  
    kernel = np.ones((3, 3), np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    results.append(reader.readtext(image,allowlist ='0123456789')[0])  
    image = cv2.erode(image, kernel, iterations=1)
    results.append(reader.readtext(image,allowlist ='0123456789')[0])  
   
    cv2.imwrite(f"{app_num}.jpg",image)
    
    return results

async def process_captcha(session,captcha_,name):
        async with(session.get(r"https://bbmptax.karnataka.gov.in/Forms//"+captcha_)) as captcha_img:
                if(captcha_img.headers.get('Content-Type')=='image/jpeg'):
                    image = Image.open(BytesIO(await captcha_img.read())) 
                    results=process_results(image,name)
                    r=''
                    m=0
                    for x in results:
                       if len(x[1])==5 and x[2]>m:
                         m=x[2]
                         r=x[1]
                    if not r:return pytesseract.image_to_string(image,config=r'--oem 1 --psm 8 -c tessedit_char_whitelist=0123456789')       
                    return r
                print('Captcha Error')
                return ""
        
        
async def process_application(app_num, session):
    print("[BEGIN]:",app_num) 
    agent=choice(user_agents)
    session.headers.update({"User-Agent":agent})
    
    form_data={}
    async with session.get(base_url) as response:
        soup = BeautifulSoup(await response.text(), 'html.parser')
        form_data.update({x.get('name'):x.get('value') or '' for x in soup.find_all('input') if x })    
        
    
    form_data.update({'__SCROLLPOSITIONX':"0"
                          ,'__SCROLLPOSITIONY':"0",
                          '__EVENTTARGET': 'ctl00$ctl00$Conten0tPlaceHolder1$ContentPlaceHolder1$txtApp',
                          'ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolder1$txtApp':str(app_num)
                          })
    
    form_data.pop('ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolder1$Button1')
    form_data.pop('ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolder1$txtCaptcha')
    await asyncio.sleep(1)

    async with session.post(base_url,headers=headers,data=form_data) as response:
        soup = BeautifulSoup(await response.text(), 'html.parser')
        form_data.update({x.get('name'):x.get('value') or '' for x in soup.find_all('input') if x})    
        captcha_=soup.select_one('img[src^="Ca"]').get("src" )  
    captcha_=(await process_captcha(session,captcha_,app_num))
    form_data.update({'ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolder1$txtCaptcha':captcha_, 
                      'ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolder1$ddlAsses':'2023-2024',     
                      'ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolder1$Button1':'submit',
                      'ctl00$ctl00$ContentPlaceHolder1$ddlLanguages': 'en-us',
                      '__EVENTTARGET':''
                      })   
    
    print("[CAPTCHA]:",captcha_)
    await asyncio.sleep(5)
    
    async with session.post(base_url,headers=headers,data=(form_data)) as pdf_response:
           if pdf_response.headers.get('Content-Type') == 'application/pdf':
            print("[COMPLETED]:",app_num,"\n")
            pdf_content = await pdf_response.read()
            
            async with aiofiles.open(f"{app_num}.pdf", "wb") as f:
                await f.write(pdf_content)
           else: 
               print("[FAILED]:",app_num,"\n")
               return False
    return True           
                
         
async def main():
    async def session_launcher(tasks):
     async with aiohttp.ClientSession() as session:
            for task_number in tasks: 
             await  process_application(task_number, session)

    tasks = [session_launcher([app_num,]) for app_num in application_numbers]
    await asyncio.gather(*tasks)


"""
async def batch_requests(numbers): 
    async with aiohttp.ClientSession() as session:
         asyncio.gather([process_application(app_num, session) for app_num in numbers])
          
async def main():
        number_of_tasks=10

        tasks = [process_application(app_num, session) for app_num in application_numbers]
        await asyncio.gather(*tasks)
"""
if __name__ == "__main__":
    asyncio.run(main())
