import urllib.request 
import urllib.parse 
import requests
 
#url = 'http://openapi.tuling123.com/openapi/api/v2' 
url = 'http://www.tuling123.com/openapi/api'
d1 = {
	"key":"e49d176663464f0dbe04084963af75c5",
    "info":"其实并不，我喜欢前者也喜欢后者"
}
d = {
	"reqType":0,
    "perception": {
        "inputText": {
            "text": "附近的酒店"
        },
        "selfInfo": {
            "location": {
                "city": "北京",
                "province": "北京",
                "street": "信息路"
            }
        }
    },
    "userInfo": {
        #"apiKey": "e49d176663464f0dbe04084963af75c5",
        #"userId": "13070159371"
        "apiKey": "e49d176663464f0dbe04084963af75c5",
        #"userId": "13070159371"
        "userId": "826998892@qq.com"
    }
}
r = requests.post(url, data=d1)
print (r.text)
#f = urllib.request.urlopen(url) 
#print(f.read().decode('utf-8'))  