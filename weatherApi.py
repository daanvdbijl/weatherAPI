import pandas as pd
import requests

import tkinter as tk
import customtkinter as ck

global key
global url

# Set key:
file = pd.read_json("OpenWeatherAPIkey.json")
key = file["APIkey"]["key"]

# Set url:
url = "https://api.openweathermap.org/data/2.5/weather?lat=%s&lon=%s&appid=%s"


# Funtion to use api and get weather:
def update_weather():
    # get weather:
    lat = latentry.get()
    lng = lngentry.get()
    if lat.replace(".", "").isnumeric() and lng.replace(".", "").isnumeric():   
        lat = float(lat)
        lng = float(lng) 
        if lat == "" or lng == "":
            weatherlabel.configure(text="Please enter a Lat and Long-idude.")
        elif lat >= -90 and lat <= 90  and lng >= -180 and lng <= 180:
            data = (lat, lng, key)
            req = url % data
            resp = requests.get(req)
            weather = resp.json()
            print(weather)
            weather_str = get_weather_str(weather)
            weatherlabel.configure(text=weather_str)
        else:
            weatherlabel.configure(text="Please enter valid values")
    else:
        weatherlabel.configure(text="Please enter valid values")
        
    
# Funtion to build weather string from json:
def get_weather_str(weather):
    weather_str = "The weather in %s is:\nSky: %s\tTemp: %s C\tPressure: %s"
    name = weather["name"]
    sky = weather["weather"][0]["main"]
    temp = str(round(weather["main"]["temp"] -253, 2))
    pres = str(weather["main"]["pressure"])
    data = (name, sky, temp, pres)
    return weather_str % data
    
    
# Funtion to clear input:
def clear():
    print("Clear")
    for i in range(len(latentry.get())):
        latentry.delete(0)
    for i in range(len(lngentry.get())):
        lngentry.delete(0)
    
    
    
# Interface:
window = tk.Tk()
window.geometry("480x480")
window.title("WeatherAPI")
ck.set_appearance_mode("dark")

# Label:
latentry = ck.CTkEntry(window, height=40, width=120, fg_color=("white", "grey"), placeholder_text="Latitude")#, text_color="grey")
latentry.place(x=60, y=5)

lngentry = ck.CTkEntry(window, height=40, width=120, fg_color=("white", "grey"), placeholder_text="Longitude")#, text_color="grey")
lngentry.place(x=300, y=5)

clearBut = ck.CTkButton(window, command=clear, height=20, width=100, fg_color=("white", "grey"))
clearBut.place(x=190, y=40)
clearBut.configure(text="Clear Lat\Long")

getWbut = ck.CTkButton(window, command=update_weather, height=60, width=440, fg_color=("white", "grey"))
getWbut.place(x=20, y=65)
getWbut.configure(text="Get weather!")

weatherlabel = ck.CTkLabel(window, height=100, width=440, text_color="Black")
weatherlabel.place(x=20, y=130)
weatherlabel.configure(text="Input coordinates for weather!")

# Mainloop:
window.mainloop()


