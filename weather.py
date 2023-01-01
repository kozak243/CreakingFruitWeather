from infi.systray import SysTrayIcon
from PIL import Image, ImageDraw, ImageFont
from urllib.request import urlopen
import json
import time
import datetime
import tkinter as tk
import tkinter.ttk as ttk

# code inspired by
# @see https://github.com/phpandrew/windowsWeatherTray
# windows tray icon
# @see https://github.com/Infinidat/infi.systray


units = "metric" #metric or imperial

time_offset = 0

timezone = 0
time_cur = 0
temperature = 0
apparent_temperature = 0
windspeed = 0
relativehumidity_2m = 0
dewpoint_2m = 0
precipitation = 0
weathercode = 0
pressure_msl = 0
visibility = 0
windspeed_10m = 0
windgusts_10m = 0

sky_conditions = [
    #00
    "Clear sky ~ Cloud development not observed or not observable - Characteristic change of the state of sky during the past hour",
    #01
    "Mainly clear ~ Clouds generally dissolving or becoming less developed - Characteristic change of the state of sky during the past hour",
    #02
    "Partly cloudy ~ State of sky on the whole unchanged - Characteristic change of the state of sky during the past hour",
    #03
    "Overcast ~ Clouds generally forming or developing - Characteristic change of the state of sky during the past hour",
    #04
    "Visibility reduced by smoke, e.g. veldt or forest fires, industrial smoke or volcanic ashes",
    #05
    "Haze",
    #06
    "Widespread dust in suspension in the air, not raised by wind at or near the station at the time of observation",
    #07
    "Dust or sand raised by wind at or near the station at the time of observation, but no well developed dust whirl(s) or sand whirl(s), and no duststorm or sandstorm seen",
    #08
    "Well developed dust whirl(s) or sand whirl(s) seen at or near the station during the preceding hour or at the time ot observation, but no duststorm or sandstorm",
    #09
    "Duststorm or sandstorm within sight at the time of observation, or at the station during the preceding hour",
    #10
    "Mist",
    #11
    "Patches - shallow fog or ice fog at the station, whether on land or sea, not deeper than about 2 metres on land or 10 metres at sea",
    #12
    "More or less continuous - shallow fog or ice fog at the station, whether on land or sea, not deeper than about 2 metres on land or 10 metres at sea",
    #13
    "Lightning visible, no thunder heard",
    #14
    "Precipitation within sight, not reaching the ground or the surface of the sea",
    #15
    "Precipitation within sight, reaching the ground or the surface of the sea, but distant, i.e. estimated to be more than 5 km from the station",
    #16
    "Precipitation within sight, reaching the ground or the surface of the sea, near to, but not at the station",
    #17
    "Thunderstorm, but no precipitation at the time of observation",
    #18
    "Squalls - at or within sight of the station during the preceding hour or at the time of observation",
    #19
    "Funnel cloud(s) - tornado cloud or water-spout - at or within sight of the station during the preceding hour or at the time of observation",
    #20
    "Drizzle (not freezing) or snow grains - not falling as shower(s)",
    #21
    "Rain (not freezing) - not falling as shower(s)",
    #22
    "Snow - not falling as shower(s)",
    #23
    "Rain and snow or ice pellets - not falling as shower(s)",
    #24
    "Freezing drizzle or freezing rain - not falling as shower(s)",
    #25
    "Shower(s) of rain",
    #26
    "Shower(s) of snow, or of rain and snow",
    #27
    "Shower(s) of hail, or of rain and hail",
    #28
    "Fog or ice fog",
    #29
    "Thunderstorm (with or without precipitation)",
    #30
    "Slight or moderate duststorm or sandstorm - has decreased during the preceding hour",
    #31
    "Slight or moderate duststorm or sandstorm - no appreciable change during the preceding hour",
    #32
    "Slight or moderate duststorm or sandstorm - has begun or has increased during the preceding hour",
    #33
    "Severe duststorm or sandstorm - has decreased during the preceding hour",
    #34
    "Severe duststorm or sandstorm - no appreciable change during the preceding hour",
    #35
    "Severe duststorm or sandstorm - has begun or has increased during the preceding hour",
    #36
    "Slight or moderate blowing snow - generally low (below eye level)",
    #37
    "Heavy drifting snow - generally low (below eye level)",
    #38
    "Slight or moderate blowing snow - generally high (above eye level)",
    #39
    "Heavy drifting snow - generally high (above eye level)",
    #40
    "Fog or ice fog at a distance at the time of observation, but not at the station during the preceding hour, the fog or ice fog extending to a level above that of the observer",
    #41
    "Fog or ice fog in patches",
    #42
    "Fog or ice fog, sky visible - has become thinner during the preceding hour",
    #43
    "Fog or ice fog, sky invisible - has become thinner during the preceding hour",
    #44
    "Fog or ice fog, sky visible - no appreciable change during the preceding hour",
    #45
    "Fog or ice fog, sky invisible - no appreciable change during the preceding hour",
    #46
    "Fog or ice fog, sky visible - has begun or has become thicker during the preceding hour",
    #47
    "Fog or ice fog, sky invisible - has begun or has become thicker during the preceding hour",
    #48
    "Fog, depositing rime, sky visible",
    #49
    "Fog, depositing rime, sky invisible",
    #50
    "Drizzle, not freezing, intermittent - slight at time of observation",
    #51
    "Drizzle, not freezing, continuous - slight at time of observation",
    #52
    "Drizzle, not freezing, intermittent - moderate at time of observation",
    #53
    "Drizzle, not freezing, continuous - moderate at time of observation",
    #54
    "Drizzle, not freezing, intermittent - heavy (dense) at time of observation",
    #55
    "Drizzle, not freezing, continuous - heavy (dense) at time of observation",
    #56
    "Drizzle, freezing, slight",
    #57
    "Drizzle, freezing, moderate or heavy (dence)",
    #58
    "Drizzle and rain, slight",
    #59
    "Drizzle and rain, moderate or heavy",
    #60
    "Rain, not freezing, intermittent - slight at time of observation",
    #61
    "Rain, not freezing, continuous - slight at time of observation",
    #62
    "Rain, not freezing, intermittent - moderate at time of observation",
    #63
    "Rain, not freezing, continuous - moderate at time of observation",
    #64
    "Rain, not freezing, intermittent - heavy at time of observation",
    #65
    "Rain, not freezing, continuous - heavy at time of observation",
    #66
    "Rain, freezing, slight",
    #67
    "Rain, freezing, moderate or heavy (dence)",
    #68
    "Rain or drizzle and snow, slight",
    #69
    "Rain or drizzle and snow, moderate or heavy",
    #70
    "Intermittent fall of snowflakes - slight at time of observation",
    #71
    "Continuous fall of snowflakes - slight at time of observation",
    #72
    "Intermittent fall of snowflakes - moderate at time of observation",
    #73
    "Continuous fall of snowflakes - moderate at time of observation",
    #74
    "Intermittent fall of snowflakes - heavy at time of observation",
    #75
    "Continuous fall of snowflakes - heavy at time of observation",
    #76
    "Diamond dust (with or without fog)",
    #77
    "Snow grains (with or without fog)",
    #78
    "Isolated star-like snow crystals (with or without fog)",
    #79
    "Ice pellets",
    #80
    "Rain shower(s), slight",
    #81
    "Rain shower(s), moderate or heavy",
    #82
    "Rain shower(s), violent",
    #83
    "Shower(s) of rain and snow mixed, slight",
    #84
    "Shower(s) of rain and snow mixed, moderate or heavy",
    #85
    "Snow shower(s), slight",
    #86
    "Snow shower(s), moderate or heavy",
    #87
    "Shower(s) of snow pellets or small hail, with or without rain or rain and snow mixed - slight",
    #88
    "Shower(s) of snow pellets or small hail, with or without rain or rain and snow mixed - moderate or heavy",
    #89
    "Shower(s) of hail, with or without rain or rain and snow mixed, not associated with thunder - slight",
    #90
    "Shower(s) of hail, with or without rain or rain and snow mixed, not associated with thunder - moderate or heavy",
    #91
    "Slight rain at time of observation - Thunderstorm during the preceding hour but not at time of observation",
    #92
    "Moderate or heavy rain at time of observation - Thunderstorm during the preceding hour but not at time of observation",
    #93
    "Slight snow, or rain and snow mixed or hail at time of observation - Thunderstorm during the preceding hour but not at time of observation",
    #94
    "Moderate or heavy snow, or rain and snow mixed or hail at time of observation - Thunderstorm during the preceding hour but not at time of observation",
    #95
    "Thunderstorm, slight or moderate, without hail but with rain and/or snow at time of observation - Thunderstorm at time of observation",
    #96
    "Thunderstorm, slight or moderate, with hail at time of observation - Thunderstorm at time of observation",
    #97
    "Thunderstorm, heavy, without hail but with rain and/or snow at time of observation - Thunderstorm at time of observation",
    #98
    "Thunderstorm combined with duststorm or sandstorm at time of observation - Thunderstorm at time of observation",
    #99
    "Thunderstorm, heavy, with hail at time of observation - Thunderstorm at time of observation"]

window = None
master = None

WC_x_pos = 0
WC_y_pos = 0

alt_mode = 0
color_mode = 0


setting = 0
if (setting == 0):
    lat = "-19.00"
    long = "-50.00"
    tzone = "Europe%2FBerlin"
elif (setting == 1):
    lat = "0.0"
    long = "0.0"
    tzone = "???"




'''
check for updated weather
'''
def checkWeather():

    # hourly
    global time_offset
    global timezone
    global time_cur
    global temperature
    global apparent_temperature
    global windspeed
    global relativehumidity_2m
    global dewpoint_2m
    global precipitation
    global weathercode
    global pressure_msl
    global visibility
    global windspeed_10m
    global windgusts_10m

    #daily
    global time_day
    global temperature_2m_max
    global temperature_2m_min
    global sunrise
    global sunset
    global precipitation_sum
    global windspeed_10m_max
    global windgusts_10m_max

    global alt_mode

    try:
        #raise
        # parameter for urlopen
        url = "https://api.open-meteo.com/v1/forecast?latitude="+ lat +"&longitude=" + long + "&hourly=apparent_temperature,temperature_2m,relativehumidity_2m,dewpoint_2m,precipitation,weathercode,pressure_msl,visibility,windspeed_10m,windgusts_10m&daily=temperature_2m_max,temperature_2m_min,sunrise,sunset,precipitation_sum,windspeed_10m_max,windgusts_10m_max&current_weather=true&windspeed_unit=ms&timezone="+tzone
        
        # store the response of URL
        response = urlopen(url)
        
        # storing the JSON response 
        # from url in data
        data = json.loads(response.read())

        time_now = time.time()
        
        time_offset = int(datetime.datetime.fromtimestamp(time_now).strftime('%H'))

        # extracting
        # hourly
        timezone = data['timezone']
        time_cur = data['current_weather']['time']
        temperature = data['current_weather']['temperature']
        apparent_temperature = data['hourly']['apparent_temperature'][time_offset]
        windspeed = data['current_weather']['windspeed']
        relativehumidity_2m = data['hourly']['relativehumidity_2m'][time_offset]
        dewpoint_2m = data['hourly']['dewpoint_2m'][time_offset]
        precipitation = data['hourly']['precipitation'][time_offset]
        weathercode = data['current_weather']['weathercode']
        pressure_msl = data['hourly']['pressure_msl'][time_offset]
        visibility = data['hourly']['visibility'][time_offset]
        windspeed_10m = data['hourly']['windspeed_10m'][time_offset]
        windgusts_10m = data['hourly']['windgusts_10m'][time_offset]

        # daily
        time_day = data['daily']['time']
        temperature_2m_max = data['daily']['temperature_2m_max']
        temperature_2m_min = data['daily']['temperature_2m_min']
        sunrise = data['daily']['sunrise']
        sunset = data['daily']['sunset']
        precipitation_sum = data['daily']['precipitation_sum']
        windspeed_10m_max = data['daily']['windspeed_10m_max']
        windgusts_10m_max = data['daily']['windgusts_10m_max']

        alt_mode = 0

        return round(temperature)
    except:
        try:
            alt_mode = 1

            # parameter for urlopen
            url = "https://wttr.in/?format=j1"

            # store the response of URL
            response = urlopen(url)

            # storing the JSON response 
            # from url in data
            data = json.loads(response.read())

            time_now = time.time()
            
            time_offset = int(datetime.datetime.fromtimestamp(time_now).strftime('%H'))

            # extracting
            # hourly
            timezone = data['nearest_area'][0]['areaName'][0]['value']
            time_cur = data['current_condition'][0]['localObsDateTime']
            temperature = float(data['current_condition'][0]['temp_C'])
            apparent_temperature = float(data['current_condition'][0]['FeelsLikeC'])
            windspeed = round(float(data['current_condition'][0]['windspeedKmph'])*1000/3600,2)
            relativehumidity_2m = float(data['current_condition'][0]['humidity'])
            dewpoint_2m = float(data['weather'][0]['hourly'][0]['DewPointC'])
            precipitation = float(data['current_condition'][0]['precipMM'])
            weathercode = data['current_condition'][0]['weatherDesc'][0]['value']
            pressure_msl = float(data['current_condition'][0]['pressure'])
            visibility = float(data['current_condition'][0]['visibility'])*100
            windspeed_10m = round(float(data['weather'][0]['hourly'][0]['windspeedKmph'])*1000/3600,2)
            windgusts_10m = round(float(data['weather'][0]['hourly'][0]['WindGustKmph'])*1000/3600,2)
            return round(temperature)

        except:
            print('exception')
            alt_mode = 2
            return 99


'''
converting temperature
'''
def convertTemp(currentTemp):
    if units == "metric":
        return int((currentTemp * 1.8) + 32);
    else:
        return int((currentTemp - 32) * .5556);
    

'''
Quick launch from menu option
'''
def launch_MainWindow(systray):
    global master


    if master is not None:  # Check if the window is already open
        return  # Do nothing if the window is already open

    master = tk.Tk()

    master.title('Creaking Fruit Weather')
    master.protocol("WM_DELETE_WINDOW", on_closing_main)
    master

    if (alt_mode != 2):
        labelHourly(master)
    else:
        labelOOF(master)

    # Get the width and height of the screen
    screen_width = master.winfo_screenwidth()
    screen_height = master.winfo_screenheight()

    # Get the width and height of the window
    window_width = master.winfo_reqwidth()
    window_height = master.winfo_reqheight()

    # Calculate the x position and y position of the window
    x_pos = int(screen_width*0.88 - window_width)
    y_pos = int(screen_height*0.8 - window_height)

    # Set the size and position of the window
    master.geometry("+{}+{}".format(x_pos, y_pos))

    tk.mainloop()

def labelOOF(master):
    ttk.Label(master, text="Big OOF, All sources failed, good luck!", font=("Comic Mono", 12)).grid(sticky=tk.E, row=0, column=0)

def removeLabels(master):
    # Change the text of the Label widgets
    for widget in master.grid_slaves():
        # Destroy the widget
        widget.destroy()

def labelHourly(master):

    global alt_mode
    
    tk.Label(master, text="Zone", font=("Comic Mono", 12)).grid(sticky=tk.E, row=0, column=0)
    tk.Label(master, text="Time", font=("Comic Mono", 12)).grid(sticky=tk.E, row=1, column=0)
    tk.Label(master, text="======================", font=("Comic Mono", 12)).grid(sticky=tk.E, row=2, column=0)
    tk.Label(master, text="Temperature", font=("Comic Mono", 12)).grid(sticky=tk.E, row=3, column=0)
    tk.Label(master, text="Apparent Temperature", font=("Comic Mono", 12)).grid(sticky=tk.E, row=4, column=0)
    tk.Label(master, text="Sky Condition", font=("Comic Mono", 12)).grid(sticky=tk.E, row=5, column=0)
    tk.Label(master, text="Precipitation", font=("Comic Mono", 12)).grid(sticky=tk.E, row=6, column=0)
    tk.Label(master, text="Windspeed (now)", font=("Comic Mono", 12)).grid(sticky=tk.E, row=7, column=0)
    tk.Label(master, text="Relative Humidity", font=("Comic Mono", 12)).grid(sticky=tk.E, row=8, column=0)
    tk.Label(master, text="Windspeed", font=("Comic Mono", 12)).grid(sticky=tk.E, row=9, column=0)
    tk.Label(master, text="Windgusts", font=("Comic Mono", 12)).grid(sticky=tk.E, row=10, column=0)
    tk.Label(master, text="Pressure", font=("Comic Mono", 12)).grid(sticky=tk.E, row=11, column=0)
    tk.Label(master, text="Visibility", font=("Comic Mono", 12)).grid(sticky=tk.E, row=12, column=0)
    tk.Label(master, text="Dewpoint", font=("Comic Mono", 12)).grid(sticky=tk.E, row=13, column=0)
    tk.Label(master, text="======================", font=("Comic Mono", 12)).grid(sticky=tk.E, row=14, column=0)

    tk.Label(master, text=str(timezone), font=("Comic Mono", 12)).grid(sticky=tk.W, row=0, column=1)
    tk.Label(master, text=str(time_cur).replace('T', ' '), font=("Comic Mono", 12)).grid(sticky=tk.W, row=1, column=1)
    tk.Label(master, text="======================", font=("Comic Mono", 12)).grid(sticky=tk.W, row=2, column=1)
    tk.Label(master, text=str(temperature)+"°C", font=("Comic Mono", 12)).grid(sticky=tk.W, row=3, column=1)
    tk.Label(master, text=str(apparent_temperature)+"°C", font=("Comic Mono", 12)).grid(sticky=tk.W, row=4, column=1)
    if (alt_mode == 0):
        tk.Button(master, text=(str(sky_conditions[weathercode])[:18]+"..."), font=("Comic Mono", 12), command=displayWC).grid(sticky=tk.W, row=5, column=1)
    else:
        tk.Label(master, text=str(weathercode), font=("Comic Mono", 12)).grid(sticky=tk.W, row=5, column=1)
    tk.Label(master, text=str(precipitation)+" mm", font=("Comic Mono", 12)).grid(sticky=tk.W, row=6, column=1)
    tk.Label(master, text=str(windspeed)+" m/s", font=("Comic Mono", 12)).grid(sticky=tk.W, row=7, column=1)
    tk.Label(master, text=str(relativehumidity_2m)+" %", font=("Comic Mono", 12)).grid(sticky=tk.W, row=8, column=1)
    tk.Label(master, text=str(windspeed_10m)+" m/s", font=("Comic Mono", 12)).grid(sticky=tk.W, row=9, column=1)
    tk.Label(master, text=str(windgusts_10m)+" m/s", font=("Comic Mono", 12)).grid(sticky=tk.W, row=10, column=1)
    tk.Label(master, text=str(pressure_msl)+" hPa", font=("Comic Mono", 12)).grid(sticky=tk.W, row=11, column=1)
    tk.Label(master, text=str(round(visibility))+" m", font=("Comic Mono", 12)).grid(sticky=tk.W, row=12, column=1)
    tk.Label(master, text=str(dewpoint_2m)+"°C", font=("Comic Mono", 12)).grid(sticky=tk.W, row=13, column=1)
    tk.Label(master, text="======================", font=("Comic Mono", 12)).grid(sticky=tk.W, row=14, column=1)



    if (alt_mode == 0):
        button = tk.Button(master, text="Hourly", font=("Comic Mono", 12), command=lambda: toDaily(master, 0))
        tk.Label(master, text="Mode:", font=("Comic Mono", 12)).grid(sticky=tk.E, row=15, column=0)
        button.grid(sticky=tk.W, row=15, column=1)
    else: 
        tk.Label(master, text="Mode: Error,", font=("Comic Mono", 12)).grid(sticky=tk.E, row=15, column=0)
        tk.Label(master, text="using backup source", font=("Comic Mono", 12)).grid(sticky=tk.W, row=15, column=1)

def labelDaily(master, day):
    tk.Label(master, text="Timezone", font=("Comic Mono", 12)).grid(sticky=tk.E, row=0, column=0)
    tk.Label(master, text="Date", font=("Comic Mono", 12)).grid(sticky=tk.E, row=1, column=0)
    tk.Label(master, text="======================", font=("Comic Mono", 12)).grid(sticky=tk.E, row=2, column=0)
    tk.Label(master, text="Temperature Max", font=("Comic Mono", 12)).grid(sticky=tk.E, row=3, column=0)
    tk.Label(master, text="Temperature Min", font=("Comic Mono", 12)).grid(sticky=tk.E, row=4, column=0)
    tk.Label(master, text="Sunrise", font=("Comic Mono", 12)).grid(sticky=tk.E, row=5, column=0)
    tk.Label(master, text="Sunset", font=("Comic Mono", 12)).grid(sticky=tk.E, row=6, column=0)
    tk.Label(master, text="Precipitation Sum", font=("Comic Mono", 12)).grid(sticky=tk.E, row=7, column=0)
    tk.Label(master, text="Windspeed Max", font=("Comic Mono", 12)).grid(sticky=tk.E, row=8, column=0)
    tk.Label(master, text="Windgusts Max", font=("Comic Mono", 12)).grid(sticky=tk.E, row=9, column=0)
    tk.Label(master, text="======================", font=("Comic Mono", 12)).grid(sticky=tk.E, row=10, column=0)

    tk.Label(master, text=str(timezone), font=("Comic Mono", 12)).grid(sticky=tk.W, row=0, column=1)
    tk.Label(master, text=str(time_day[day]), font=("Comic Mono", 12)).grid(sticky=tk.W, row=1, column=1)
    tk.Label(master, text="======================", font=("Comic Mono", 12)).grid(sticky=tk.W, row=2, column=1)
    tk.Label(master, text=str(temperature_2m_max[day])+"°C", font=("Comic Mono", 12)).grid(sticky=tk.W, row=3, column=1)
    tk.Label(master, text=str(temperature_2m_min[day])+"°C", font=("Comic Mono", 12)).grid(sticky=tk.W, row=4, column=1)
    tk.Label(master, text=str(sunrise[day])[11:], font=("Comic Mono", 12)).grid(sticky=tk.W, row=5, column=1)
    tk.Label(master, text=str(sunset[day])[11:], font=("Comic Mono", 12)).grid(sticky=tk.W, row=6, column=1)
    tk.Label(master, text=str(precipitation_sum[day])+" mm", font=("Comic Mono", 12)).grid(sticky=tk.W, row=7, column=1)
    tk.Label(master, text=str(windspeed_10m_max[day])+" m/s", font=("Comic Mono", 12)).grid(sticky=tk.W, row=8, column=1)
    tk.Label(master, text=str(windgusts_10m_max[day])+" m/s", font=("Comic Mono", 12)).grid(sticky=tk.W, row=9, column=1)
    tk.Label(master, text="======================", font=("Comic Mono", 12)).grid(sticky=tk.W, row=10, column=1)

    if (day == 6):
        button = tk.Button(master, text="First", font=("Comic Mono", 12), command=lambda: toDaily(master, 0))
        tk.Label(master, text="Day:", font=("Comic Mono", 12)).grid(sticky=tk.E, row=11, column=0)
        button.grid(sticky=tk.W, row=11, column=1)

    else:
        button = tk.Button(master, text="Next", font=("Comic Mono", 12), command=lambda: toDaily(master, (day+1)))
        tk.Label(master, text="Day:", font=("Comic Mono", 12)).grid(sticky=tk.E, row=11, column=0)
        button.grid(sticky=tk.W, row=11, column=1)

    button = tk.Button(master, text="Daily", font=("Comic Mono", 12), command=lambda: toHourly(master))
    tk.Label(master, text="Mode:", font=("Comic Mono", 12)).grid(sticky=tk.E, row=12, column=0)
    button.grid(sticky=tk.W, row=12, column=1)

def toDaily(master, day):
    removeLabels(master)
    labelDaily(master, day)

def toHourly(master):
    removeLabels(master)
    labelHourly(master)

def on_closing():
    global window
    window.destroy()
    window = None

def on_closing_main():
    global master
    master.destroy()
    master = None
    if window is None:  # Check if the window is already open
        return  # Do nothing if the window is already open
    on_closing()

def displayWC():
    global window  # Declare the global variable "window"
    if window is not None:  # Check if the window is already open
        return  # Do nothing if the window is already open
    window = tk.Tk()  # Create a new window
    window.title("Weather Code: " + str(weathercode))
    window.protocol("WM_DELETE_WINDOW", on_closing)


    tk.Label(window, text=sky_conditions[weathercode], font=("Comic Mono", 12)).grid(sticky=tk.W, row=0, column=0)

    window.withdraw()


    window.after(5, move_window)

    window.mainloop()

def move_window():
    # Set the new size and position of the window
    window.geometry("+{}+{}".format(master.winfo_x() + master.winfo_reqwidth() - window.winfo_reqwidth(), master.winfo_y() - window.winfo_reqheight()*3 + 15))
    window.deiconify()


def shutdown(systray):
    global n
    n = 0
    if (master != None):
        on_closing_main()

#draw icon
image= "icon.ico"
n=1
while (n!=0):
    #check weather
    true_temp = checkWeather()
    temp = true_temp
    if (color_mode == 1):
        temp = round(abs(temp))

    operator = ("C" if units == "metric" else "F")
    convOper = ("F" if units == "metric" else "C")
    
    #text position
    x = 1
    #adjust size of font
    if len(str(temp)) > 3:
        fontSize = 20
        y = 12 #height
    elif len(str(temp)) > 2:
        fontSize = 33
        y = 3 #height
        x = -5
    elif len(str(temp)) > 1:
        fontSize = 40
        y = -2 #height
        x = 1 #center
    else:
        fontSize = 45
        y = -6 #height
        x = 14

    # create image
    img = Image.new('RGBA', (48, 48), color = (255, 255, 255, 0))  # color background =  white  with transparency
    d = ImageDraw.Draw(img)

    #add text to the image
    font_type  = ImageFont.truetype("comic.ttf", fontSize)

    color = (255,255,255)
    if (color_mode == 1):
        if (true_temp < 0):
            color = (0,150,255)
        if (true_temp > 0):
            color = (255,80,0)
    
    d.text((x,y), str(temp), fill=color, font = font_type)

    img.save(image)

    updateTime = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

    #generate text for overlay
    hover_text = (
        "Temperature: " + str(temperature) + "\n" +
        "Apparent temperature: "  + str(apparent_temperature) + "\n" +
        "Weathercode: " + str(weathercode) + "\n" +
        "Precipitation: " + str(precipitation) + "\n" +
        "Windspeed: " + str(windspeed)
        )
    
    # display image in systray
    menu_options = (
        ("Full Info", None, launch_MainWindow),
    )
    if n==1:
        systray = SysTrayIcon(image, hover_text, menu_options, shutdown)
        systray.start()
        n+=1
    else:
        systray.update(icon=image, hover_text=hover_text)
    time.sleep(5)
