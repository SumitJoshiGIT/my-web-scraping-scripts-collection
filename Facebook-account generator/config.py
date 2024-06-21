#config
from random import randint,choice
user_agents={}

proxy={"server":"http://md1-1.mproxy.top:30016",
                    "username":"wiwao",
                    "password":"4bRhAvmYym"}


API_KEYS={"smshub":"api_key",        
          "recaptcha":"api_key",
          "bot_key":("api_key")#bot token +"/"
          }
countries=[73,""]#Enter country codes in order of preference inside the array currently set to brazil
 
PASSWORDS=["alex899@TG"]

agents={"chromium":{"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
        #"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
        #"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
         "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
        },
        "firefox":{"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0",
                   "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0",
                   "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0"}
        }
iphones=[
    {'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/16.0 Mobile/15A372 Safari/604.1', 'viewport': {'width': 375, 'height': 667}, 'device_scale_factor': 2, 'is_mobile': True, 'has_touch': True, 'default_browser_type': 'webkit'},
{'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/16.0 Mobile/15A372 Safari/604.1', 'viewport': {'width': 414, 'height': 736}, 'device_scale_factor': 3, 'is_mobile': True, 'has_touch': True, 'default_browser_type': 'webkit'},
{'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/16.0 Mobile/15A372 Safari/604.1', 'viewport': {'width': 375, 'height': 667}, 'device_scale_factor': 2, 'is_mobile': True, 'has_touch': True, 'default_browser_type': 'webkit'},
{'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/16.0 Mobile/15A372 Safari/604.1', 'viewport': {'width': 414, 'height': 736}, 'device_scale_factor': 3, 'is_mobile': True, 'has_touch': True, 'default_browser_type': 'webkit'},
{'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/16.0 Mobile/15A372 Safari/604.1', 'viewport': {'width': 375, 'height': 667}, 'device_scale_factor': 2, 'is_mobile': True, 'has_touch': True, 'default_browser_type': 'webkit'},
{'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/16.0 Mobile/15A372 Safari/604.1', 'viewport': {'width': 414, 'height': 736}, 'device_scale_factor': 3, 'is_mobile': True, 'has_touch': True, 'default_browser_type': 'webkit'},
{'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/16.0 Mobile/14E304 Safari/602.1', 'viewport': {'width': 320, 'height': 568}, 'device_scale_factor': 2, 'is_mobile': True, 'has_touch': True, 'default_browser_type': 'webkit'},
{'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/16.0 Mobile/15A372 Safari/604.1', 'viewport': {'width': 375, 'height': 812}, 'device_scale_factor': 3, 'is_mobile': True, 'has_touch': True, 'default_browser_type': 'webkit'},
{'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1', 'viewport': {'width': 414, 'height': 896}, 'device_scale_factor': 3, 'is_mobile': True, 'has_touch': True, 'default_browser_type': 'webkit'},
{'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1', 'viewport': {'width': 414, 'height': 715}, 'device_scale_factor': 2, 'is_mobile': True, 'has_touch': True, 'default_browser_type': 'webkit'},
{'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1', 'viewport': {'width': 375, 'height': 635}, 'device_scale_factor': 3, 'is_mobile': True, 'has_touch': True, 'default_browser_type': 'webkit'},
{'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1', 'viewport': {'width': 414, 'height': 715}, 'device_scale_factor': 3, 'is_mobile': True, 'has_touch': True, 'default_browser_type': 'webkit'},
{'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1', 'viewport': {'width': 390, 'height': 664}, 'device_scale_factor': 3, 'is_mobile': True, 'has_touch': True, 'default_browser_type': 'webkit'},
{'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1', 'viewport': {'width': 390, 'height': 664}, 'device_scale_factor': 3, 'is_mobile': True, 'has_touch': True, 'default_browser_type': 'webkit'},
{'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1', 'viewport': {'width': 428, 'height': 746}, 'device_scale_factor': 3, 'is_mobile': True, 'has_touch': True, 'default_browser_type': 'webkit'},
{'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1', 'viewport': {'width': 375, 'height': 629}, 'device_scale_factor': 3, 'is_mobile': True, 'has_touch': True, 'default_browser_type': 'webkit'},
{'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1', 'viewport': {'width': 390, 'height': 664}, 'device_scale_factor': 3, 'is_mobile': True, 'has_touch': True, 'default_browser_type': 'webkit'},
{'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1', 'viewport': {'width': 390, 'height': 664}, 'device_scale_factor': 3, 'is_mobile': True, 'has_touch': True, 'default_browser_type': 'webkit'},
{'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1', 'viewport': {'width': 428, 'height': 746}, 'device_scale_factor': 3, 'is_mobile': True, 'has_touch': True, 'default_browser_type': 'webkit'},
{'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1', 'viewport': {'width': 832, 'height': 380}, 'device_scale_factor': 3, 'is_mobile': True, 'has_touch': True, 'default_browser_type': 'webkit'},
{'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1', 'viewport': {'width': 375, 'height': 629}, 'device_scale_factor': 3, 'is_mobile': True, 'has_touch': True, 'default_browser_type': 'webkit'}
]


def ChromeAgent(version,platform=""):
 if platform=="Windows" or platform=="":
     platform_="Win64"
     sys="(Windows NT 10.0; Win64; x64)"
 v=(randint(version-2,version+2),randint(0,70),choice((f'.{randint(0,200)}','')))
 print(v,version)
 version=f"{v[0]}.{v[1]}"+v[2]   
 v=version.split(".")[0]

 USER_AGENT = {
    "userAgent": f"Mozilla/5.0{sys}AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{version} Safari/537.36", 
    "platform": platform_,
    "acceptLanguage": "en-US, en",
    "userAgentMetadata": {
        "brands": [
            {"brand": " Not A;Brand", "version": "99"},
            {"brand": "Chromium", "version":v},
            {"brand": "Google Chrome", "version":v},
        ],
        "fullVersion":version,
        "platform": platform,
        "platformVersion": "10.0",
        "architecture": "x64",
        "model": "",
        "mobile": False,
    }}
 return (USER_AGENT["userAgent"],USER_AGENT)
