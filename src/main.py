from customtkinter import *
from tkinter import *
import os
import geopy
import requests
import bs4
import re
from PIL import ImageTk, Image
import json
from datetime import datetime as dt

def show_location():
    """
    Reads the coordinates saved in a file and
    displays the coordinates of the current location.
    """

    # reads the file that contains the location of the user
    with open("../coordinates.txt") as file:
        coord = file.read()

    # reverse geocoding using GeoPy
    locator = geopy.Nominatim(user_agent="ctk_weather_app")
    location = locator.reverse(coord).address.split(",")

    # returns the city and the country name
    return f"{location[-4]},{location[-1]}"

def current_weather(city):
    # generates the url
    url = "https://api.openweathermap.org/data/2.5/weather?q=" + city + "%20&units=metric&appid=4c252364e3f8712e6d14a4a586bfa2b4"

    # grabs the content from the URL
    html = requests.get(url)

    # creates a soup object that contains parsed content
    soup = bs4.BeautifulSoup(html.text, "html.parser")

    # parses the json object and deserializes it into a python object (i.e. dict)
    weather = json.loads(soup.text)

    # gets the temperature in Celsius
    temp = weather["main"]["feels_like"]

    # humidity
    humid = weather["main"]["humidity"]

    # wind speed (converted to Km/h)
    wind = round(weather["wind"]["speed"] * 3.6, 2)

    # visibility
    visibility = weather["visibility"]

    # rainfall (in %)
    if "rain" not in weather.keys():
        rain = 0
    else:
        rain = weather["rain"]["1h"] * 100

    # weather type
    weather_type = weather["weather"][0]["description"]

    app.text3.set(str(humid))
    app.text4.set(str(wind))
    app.text5.set(str(visibility))


class CTkApp(CTk):

    def __init__(self, time, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # setting the dimensions of the window
        self.geometry("800x500")

        # disabling the resize button
        self.resizable(False, False)

        # choosing an image for the icon
        self.iconbitmap("../data/img/weather-news.ico")

        # grid properties
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # making the mainframe
        self.mainframe = CTkFrame(master=self, width=250, height=240, corner_radius=15)
        self.mainframe.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        # customizing the mainframe
        self.mainframe.grid_columnconfigure(0, weight=1)
        self.mainframe.grid_columnconfigure(1, weight=1)

        # left frame
        self.left_frame = CTkFrame(master=self.mainframe, width=50, height=450, corner_radius=15)
        self.left_frame.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")

        # right frame
        self.right_frame = CTkFrame(master=self.mainframe, width=50, height=150, corner_radius=15)
        self.right_frame.grid(row=0, column=1, padx=15, pady=15, sticky="ew")

        # bottom frame
        self.bottom_frame = CTkFrame(master=self.mainframe, width=50, height=250, corner_radius=15)
        self.bottom_frame.grid(row=1, column=0, columnspan=2, padx=15, pady=15, sticky="nsew")

        # search box
        self.search_box = CTkEntry(master=self.left_frame, bg="#ccc", text_font=("Arial", 18), width=200, border=0, fg="#000")
        self.search_box.focus_set()
        self.search_box.grid(row=1, column=0, padx=10, pady=15)

        # search button
        img = Image.open("../data/img/search.png")
        resized_img = img.resize((20, 20))
        icon = ImageTk.PhotoImage(resized_img)
        self.button = CTkButton(master=self.left_frame,
                                text="Go",
                                width=80,
                                height=35,
                                compound="right",
                                image=icon,
                                command="get_weather")
        self.button.grid(row=1, column=1, padx=5, pady=15)

        # current location
        self.text1 = StringVar()
        user_location = show_location()
        self.text1.set(user_location)

        self.location = CTkLabel(master=self.left_frame, textvariable=self.text1, text_font=("Segoe", 25))
        self.location.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

        # current time
        self.timenow = CTkLabel(master=self.left_frame, text=time, text_font=("Segoe", 10))
        self.timenow.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        # # temperature
        # self.text2 = StringVar()
        # self.text2.set("")
        #
        # # humidity
        # self.text3 = StringVar()
        # self.text3.set("")
        #
        # # windspeed
        # self.text4 = StringVar()
        # self.text4.set("")
        #
        # # visibility
        # self.text5 = StringVar()
        # self.text5.set("")
        #
        # # air quality
        # self.text6 = StringVar()
        # self.text6.set("")

        # humidity = CTkLabel(master=self, textvariable=self.text3, text_font=("Segoe", 15))
        # humidity.place(relx=0.2, rely=.8)
        # windspeed = CTkLabel(master=self, textvariable=self.text4, text_font=("Segoe", 15))
        # windspeed.place(relx=0.4, rely=.8)
        # visibility = CTkLabel(master=self, textvariable=self.text5, text_font=("Segoe", 15))
        # visibility.place(relx=0.6, rely=.8)
        # # description = Label(app, textvariable=self.text4, font=("Segoe", 20))
        # # description.place(relx, rely)
        #
        # city = user_location.split(",")[0]
        # self.current_weather(city)

    # def current_weather(self, city):
    #     # generates the url
    #     url = "https://api.openweathermap.org/data/2.5/weather?q=" + city + "%20&units=metric&appid=4c252364e3f8712e6d14a4a586bfa2b4"
    #
    #     # grabs the content from the URL
    #     html = requests.get(url)
    #
    #     # creates a soup object that contains parsed content
    #     soup = bs4.BeautifulSoup(html.text, "html.parser")
    #
    #     # parses the json object and deserializes it into a python object (i.e. dict)
    #     weather = json.loads(soup.text)
    #
    #     # gets the temperature in Celsius
    #     temp = weather["main"]["feels_like"]
    #
    #     # humidity
    #     humid = weather["main"]["humidity"]
    #
    #     # wind speed (converted to Km/h)
    #     wind = round(weather["wind"]["speed"] * 3.6, 2)
    #
    #     # visibility
    #     visibility = weather["visibility"]
    #
    #     # rainfall (in %)
    #     if "rain" not in weather.keys():
    #         rain = 0
    #     else:
    #         rain = weather["rain"]["1h"] * 100
    #
    #     # weather type
    #     weather_type = weather["weather"][0]["description"]
    #
    #     self.text3.set(str(humid))
    #     self.text4.set(str(wind))
    #     self.text5.set(str(visibility))

if __name__ == "__main__":
    time = dt.now().strftime("%H:%M %p")
    set_appearance_mode("dark")
    set_default_color_theme("blue")
    app = CTkApp(time)
    app.mainloop()
