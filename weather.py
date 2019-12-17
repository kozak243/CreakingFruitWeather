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

useFeelsLike = True; #use feels like
temperature = 0
feelslike = 0
#openweathermap.org API key:
weatherapi_key = "{API_KEY_HERE}"

#build API URL
URL = "https://api.openweathermap.org/data/2.5/weather?q="+city+","+country+"&units="+units+"&appid="+weatherapi_key

# defining a params dict for the parameters to be sent to the API 
PARAMS = "" 

HEADERS = {'Content-type': 'application/json', 'Accept': 'text/plain'}

def checkWeather():
    global temperature
    global feelslike
    #threading.Timer(60.0, checkWeather).start()
    # sending get request and saving the response as response object 
    r = requests.post(url = URL, json = PARAMS, headers = HEADERS) 

    # extracting data in json format 
    data = r.json() 

    # extracting latitude, longitude and formatted address  
    # of the first matching location
    temperature = int(round(data['main']['temp']))
    feelslike = int(round(data['main']['feels_like']))

    if useFeelsLike == True:
        return feelslike
    else:
        return temperature

#draw icon
image= "icon.ico"
n=1
while True:
    #check weather
    temp = checkWeather()

    #adjust size of font
    if len(str(temp)) > 3:
        fontSize = 20
    elif len(str(temp)) > 2:
        fontSize = 25
    elif len(str(temp)) > 1:
        fontSize = 35
    else:
        fontSize = 40
        
    # create image
    img = Image.new('RGBA', (50, 50), color = (255, 255, 255, 0))  # color background =  white  with transparency
    d = ImageDraw.Draw(img)

    #add text to the image
    font_type  = ImageFont.truetype("arial.ttf", fontSize)
    d.text((5,5), str(temp)+"°", fill=(255,255,255), font = font_type)

    img.save(image)

    #generate text for overlay
    hover_text = city+" weather\nCurrent Temperature: "+str(temperature)+"°\nFeels like: "+str(feelslike)+"°"
    
    # display image in systray 
    if n==1:
        systray = SysTrayIcon(image, hover_text)
        systray.start()
    else:
        systray.update(icon=image, hover_text=hover_text)
    time.sleep(120)
    n+=1
systray.shutdown()

