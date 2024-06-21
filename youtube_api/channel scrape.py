from fuzzywuzzy import fuzz

from apiclient.discovery import build
from utils import apiKey
import pandas as pd

result_pool=[]
youtube_client =build('youtube','v3',developerKey=apiKey)
threshold_score=60 #

def search_in_items(items,channel_name): 
 result=[0,'']
 
 for item in items:
  if(item['id']['kind']=='youtube#channel'):
  
   Channel=item['snippet']['channelTitle']
   Similarity_score=fuzz.token_sort_ratio(Channel.lower(),channel_name.lower())
   if Similarity_score>result[0]:
    result[0]=Similarity_score
    result[1]=item
   return result  


def search_for_channel(channel_name):
 query_request=youtube_client.search().list(q=channel_name,part='snippet',maxResults=20)
 query_response=query_request.execute()
 items=query_response['items']
 search_result=search_in_items(items,channel_name)
 print("\n",search_result)
 id=search_result[1]['id']['channelId']
 request = youtube_client.channels().list(part='snippet,statistics,contentDetails',id=id)
 response=request.execute() ['items'][0]
 snippet=response['snippet']
 url='https://www.youtube.com/'+snippet['customUrl']

 return url

def main():
  channels=pd.read_excel('input.xlsx')['Field2']
  print(channels)
  
  for channel in channels:
   result=search_for_channel(channel)
   result_pool.append(result)
  
  df=pd.DataFrame(result_pool,columns=['Links']) 
  df.to_excel('data.xlsx')
  print('done')
  
main() 
     