import requests
from infi.systray import SysTrayIcon
from PIL import Image, ImageDraw,ImageFont

#windows tray icon
# @see https://github.com/Infinidat/infi.systray
#open weather API
# @see https://openweathermap.org/api
# api-endpoint 
#variables
city = "{CITY HERE}"
country = "US" #two digit code
units = "metric" #testing or imperial
#api key
weatherapi_key = "{API_KEY_HERE}"

#build API URL
URL = "https://api.openweathermap.org/data/2.5/weather?q="+city+","+country+"&units="+units+"&appid="+weatherapi_key

# defining a params dict for the parameters to be sent to the API 
PARAMS = "" 

HEADERS = {'Content-type': 'application/json', 'Accept': 'text/plain'}

def checkWeather():
    # sending get request and saving the response as response object 
    r = requests.post(url = URL, json = PARAMS, headers = HEADERS) 

    # extracting data in json format 
    data = r.json() 

    # extracting latitude, longitude and formatted address  
    # of the first matching location    
    return int(data['main']['temp'])

#draw icon
image= "icon.ico"
n=1
while True:
    #check weather
    temp = checkWeather()
    # create image
    img = Image.new('RGBA', (50, 50), color = (255, 255, 255, 0))  # color background =  white  with transparency
    d = ImageDraw.Draw(img)

    #add text to the image
    font_type  = ImageFont.truetype("arial.ttf", 40)
    d.text((5,5), str(temp)+"°", fill=(255,255,255), font = font_type)

    img.save(image)

    # display image in systray 
    if n==1:
        systray = SysTrayIcon(image, city+" weather")
        systray.start()
    else:
        systray.update(icon=image)
    time.sleep(120)
    n+=1
systray.shutdown()

