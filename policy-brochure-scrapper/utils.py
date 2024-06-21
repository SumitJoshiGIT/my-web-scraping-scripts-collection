from difflib import SequenceMatcher
import datetime as dt

def uniquify(products):#extracts unique keywords out of products
  for x in ("aegon","life","insurance","brochure"," ","plan"): 
    try:
         products.remove(x)
    except:continue
  return products 


def match_name(brochure_name,products,mode=0):#filters out unmatched instances of 
      if mode==0:#mode one for non-rigorous check 
       for name in brochure_name:
        if name!=' ':  
         for product in products:
           if SequenceMatcher(None,name.lower(),product).ratio()>0.7:
             return True
         else:pass
      if mode==1:#for rigorous check
        for product in products:
         name=brochure_name.lower().replace(' ',"").strip()
         product=product.replace(' ',"" ).lower()
         if  SequenceMatcher(None,name,product).ratio()>0.7:return  True
         product=product.replace('aegonlife','')
         if  SequenceMatcher(None,name,product).ratio()>0.7:return  True
      return False  
                       
class Logger:       
 
 def log(self,data):
   time=dt.datetime.now()
   time=time.isoformat()
   print(time,">>",data)
 
 
 def Log(self,func):
   def inner_func(*a):
     try: 
      func(*a)
     except Exception as e :
         time=dt.datetime.now()
         time=time.isoformat()
         print(time+">>"+e)
   return inner_func

