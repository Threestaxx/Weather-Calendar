# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 13:54:17 2025

@author: Threestaxx
"""
import tkinter as tk
from tkinter import messagebox
import requests
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

# Visual Crossing API key and endpoint
API_KEY = "ZKSLPFNAPZAY9CNUU4MPCNJEN"  # Replace with your actual API key
BASE_URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"

# Function to get latitude and longitude from location input
def get_lat_lon(location):
    geolocator = Nominatim(user_agent="weather_app")
    try:
        location = geolocator.geocode(location, timeout=10)
        if location:
            return location.latitude, location.longitude
        else:
            messagebox.showerror("Error", "Could not find the location. Please try again.")
            return None
    except GeocoderTimedOut:
        messagebox.showerror("Error", "Geocoding service timed out. Please try again.")
        return None

# Function to fetch historical weather data
def get_weather_data(lat, lon, date):
    url = f"{BASE_URL}/{lat},{lon}/{date}?key={API_KEY}&include=days"
    print(f"API URL: {url}")  # Debugging: Print the API URL
    response = requests.get(url)
    print(f"API Response Status Code: {response.status_code}")  # Debugging: Print the status code
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching weather data: {response.status_code}")
        print(f"Response Text: {response.text}")  # Debugging: Print the response text
        messagebox.showerror("Error", f"Failed to fetch weather data: {response.status_code}")
        return None

# Function to display weather data in the UI
def display_weather(data):
    if data and "days" in data and len(data["days"]) > 0:
        weather = data["days"][0]
        result_text.delete(1.0, tk.END)  # Clear previous results
        result_text.insert(tk.END, f"Weather on {weather['datetime']}:\n")
        result_text.insert(tk.END, f"  Temperature: {weather['temp']}°F\n")
        result_text.insert(tk.END, f"  Feels Like: {weather['feelslike']}°F\n")
        result_text.insert(tk.END, f"  Precipitation: {weather['precip']} inches\n")
        result_text.insert(tk.END, f"  Wind Speed: {weather['windspeed']} mph\n")
        result_text.insert(tk.END, f"  Conditions: {weather['conditions']}\n")
    else:
        messagebox.showinfo("No Data", "No weather data found for the specified date and location.")

# Function to handle the "Get Weather" button click
def on_get_weather():
    location = location_entry.get().strip()
    date = date_entry.get().strip()

    if not location or not date:
        messagebox.showwarning("Input Error", "Please enter both location and date.")
        return

    lat_lon = get_lat_lon(location)
    if not lat_lon:
        return

    lat, lon = lat_lon
    weather_data = get_weather_data(lat, lon, date)
    if weather_data:
        display_weather(weather_data)

# Create the main application window
app = tk.Tk()
app.title("Historical Weather Lookup")
app.geometry("600x400")

# Location input
location_label = tk.Label(app, text="Enter a city, state, or ZIP code:")
location_label.pack(pady=5)
location_entry = tk.Entry(app, width=50)
location_entry.pack(pady=5)

# Date input
date_label = tk.Label(app, text="Enter a date (YYYY-MM-DD) within the last 12 months:")
date_label.pack(pady=5)
date_entry = tk.Entry(app, width=50)
date_entry.pack(pady=5)

# Get Weather button
get_weather_button = tk.Button(app, text="Get Weather", command=on_get_weather)
get_weather_button.pack(pady=10)

# Text widget to display results
result_text = tk.Text(app, wrap=tk.WORD, width=70, height=15)
result_text.pack(pady=10)

# Run the application
app.mainloop()