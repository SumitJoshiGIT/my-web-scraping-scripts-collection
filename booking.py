from requests import get
from bs4 import BeautifulSoup as bs
import pandas as pd
from random import choice

agents=[
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.37",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 11; Pixel 4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36",
]

def gen_user_agent():
  while(True):
    yield choice(agents)

user_agent=gen_user_agent()
filters="&nflt=ht_id%3D206%3Bht_id%3D204"

def get_data(hotel_list):   
  data=[]
  for link in hotel_list:
    data.extend(scrape_link(link+filters))
  return data

def scrape_link(link):
  data=[]
  cval=0
  values=True

  headers={
'User-Agent':next(user_agent), 
'Origin':
  'https://www.booking.com',
'Referer':
  'https://www.booking.com/'}
  
  while(values):
   soup=bs(get(link+f"&offset={cval}",headers=headers).text,'html.parser')
   values=scrape_soup(soup)
   data.extend(values)
   
   cval+=25
  return data 

def scrape_soup(soup):
  hotels_data=[]
  hotels = soup.findAll('div', {'data-testid': 'property-card'})
  for hotel in hotels:
    name_element = hotel.find('div', {'data-testid': 'title'})
    name = name_element.text.strip() if name_element else ""
    stars=hotel.select_one('div div[aria-label$="of 5"]')
    stars=stars.get("aria-label")[0] if stars else "No stars"
    link=hotel.select_one("div h3 a") 
    link=link.get("href") if link else ''
    hotels_data.append((
     name,
     link,
     stars
    ))
  return hotels_data 


def test():
 output=get_data(["https://www.booking.com/searchresults.en-gb.html?ss=Lucknow&ssne=Lucknow&ssne_untouched=Lucknow"])
 print(output)
 df=pd.DataFrame(output,columns=["name","link","type"])
 print(df)
test()
#hotel_list=[]
#output=get_data(hotel_list)
#df=pd.DataFrame(output,columns=["name","link","type"])
#df.to_csv("output.csv")