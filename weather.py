import requests
from infi.systray import SysTrayIcon
from PIL import Image, ImageDraw,ImageFont
import time
import tkinter as tk

#windows tray icon
# @see https://github.com/Infinidat/infi.systray
#open weather API
# @see https://openweathermap.org/api
# api-endpoint 
#variables

city = ""
country = ""
units = "metric" #testing or imperial
useFeelsLike = "True";

temperature = 0
feelslike = 0

#api key
weatherapi_key = ""

# defining a params dict for the parameters to be sent to the API 
PARAMS = ""

HEADERS = {'Content-type': 'application/json', 'Accept': 'text/plain'}
'''
check for updated weather
'''
def checkWeather():
    global temperature
    global feelslike

    URL = "https://api.openweathermap.org/data/2.5/weather?q="+city+","+country+"&units="+units+"&appid="+weatherapi_key

    # sending get request and saving the response as response object 
    r = requests.post(url = URL, json = PARAMS, headers = HEADERS) 

    # extracting data in json format 
    data = r.json() 

    # extracting latitude, longitude and formatted address  
    # of the first matching location
    temperature = int(round(data['main']['temp']))
    feelslike = int(round(data['main']['feels_like']))

    if useFeelsLike == "True":
        return feelslike
    else:
        return temperature

'''
read database file for user settings
'''
def readDbFile():
    global weatherapi_key, city, country, useFeelsLike
    try:
        filepath = 'weather.db'
        with open(filepath) as fp:
            line = fp.readline().strip()
            weatherapi_key = line
            cnt = 1
            while line:
                line = fp.readline().strip()
                if cnt == 1:
                    city = line
                elif cnt == 2:
                    country = line
                elif cnt == 3:
                    useFeelsLike = line
                cnt += 1
    except Exception as e:
        print("Error: "+e)
        print("Please create 'weather.db' first")
        openSettingsWindow() #not yet working

'''
write settings to db file
'''
def writeToDbFile():
    outputFile = open('weather.db', 'w')
    outputFile.write(e1.get()+'\n')
    outputFile.write(e2.get()+'\n')
    outputFile.write(e3.get()+'\n')
    outputFile.write(str(chkValue.get()))

'''
Open settings window
'''
def openSettingsWindow(systray):
    master = tk.Tk()
    master.title('Settings')
    master.geometry("400x200")

    chkValue = tk.BooleanVar()

    tk.Label(master, 
             text="Openweather.org API Key\t").grid(row=0)
    tk.Label(master, 
             text="Your City\t").grid(row=1)
    tk.Label(master, 
             text="Your Country (2 Letter Abbr)\t").grid(row=2)
    tk.Label(master, 
             text="Use Feels Like Temperature\t").grid(row=3)

    e1 = tk.Entry(master)
    e1.insert(0, weatherapi_key)

    e2 = tk.Entry(master)
    e2.insert(0, city)

    e3 = tk.Entry(master)
    e3.insert(0, country)
    
    e4 = tk.Checkbutton(master, text='Check Box', var=chkValue)
    if useFeelsLike == "True":
        e4.select()

    e1.grid(row=0, column=1)
    e2.grid(row=1, column=1)
    e3.grid(row=2, column=1)
    e4.grid(row=3, column=1)

    tk.Button(master, 
              text='Quit', 
              command=master.quit).grid(row=5, 
                                        column=0, 
                                        sticky=tk.W, 
                                        pady=4)
    tk.Button(master, 
              text='Save Settings', command=writeToDbFile).grid(row=5, 
                                                           column=1, 
                                                           sticky=tk.W, 
                                                           pady=4)
    tk.mainloop()

#read db file
readDbFile()

#draw icon
image= "icon.ico"
n=1
while True:
    #check weather
    temp = checkWeather()

    #text position
    x = 1
    #adjust size of font
    if len(str(temp)) > 3:
        fontSize = 20
        y = 12 #height
    elif len(str(temp)) > 2:
        fontSize = 25
        y = 9 #height
    elif len(str(temp)) > 1:
        fontSize = 35
        y = 5 #height
        x = 3 #center
    else:
        fontSize = 40
        y = 5 #height
        x = 5

    # create image
    img = Image.new('RGBA', (48, 48), color = (255, 255, 255, 0))  # color background =  white  with transparency
    d = ImageDraw.Draw(img)

    #add text to the image
    font_type  = ImageFont.truetype("arial.ttf", fontSize)
    d.text((x,y), str(temp)+"°", fill=(255,255,255), font = font_type)

    img.save(image)

    #generate text for overlay
    hover_text = city+" weather\nCurrent Temperature: "+str(temperature)+"°\nFeels like: "+str(feelslike)+"°"
    
    # display image in systray
    menu_options = (("Settings", None, openSettingsWindow),)
    if n==1:
        systray = SysTrayIcon(image, hover_text, menu_options)
        systray.start()
    else:
        systray.update(icon=image, hover_text=hover_text)
    time.sleep(30)
    n+=1
systray.shutdown()
