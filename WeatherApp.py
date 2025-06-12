import requests
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import ttkbootstrap
import customtkinter as ctk
import sqlite3

# Connect to (or create) the database file
conn = sqlite3.connect("weather_search_history.db")

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

record_vars= []

def history_read():
    
    cursor.execute("SELECT * FROM weather_data")
    rows = cursor.fetchall()
    print("Weather Data:")
    for row in rows:
        print(row)
    return rows

def history_show(records):
    # Clear previous records in the scrollable frame
    for widget in scroll_frame.winfo_children():
        widget.destroy()

    record_vars.clear()  # Clear the list of record variables


    for i in records:
        record_frame = ctk.CTkFrame(scroll_frame, width=600)
        record_frame.pack(pady=5, fill=tk.X)
        
        var = tk.BooleanVar()
        record_selector = tk.Checkbutton(record_frame,variable=var, text="")
        record_selector.pack(side=tk.LEFT, padx=5)

        record_label = ctk.CTkLabel(record_frame, text=f"{i[0]}")
        record_label.pack(side=tk.LEFT, padx=5)

        city_name_label = ctk.CTkLabel(record_frame, text=f"City: {i[2]}")
        city_name_label.pack(side=tk.LEFT, padx=5)

        date_label = ctk.CTkLabel(record_frame, text=f"Date: {i[3]}")
        date_label.pack(side=tk.LEFT, padx=5)

        temperature_label = ctk.CTkLabel(record_frame, text=f"T: {i[4]}")
        temperature_label.pack(side=tk.LEFT, padx=5)

        description_label = ctk.CTkLabel(record_frame, text=f"D: {i[5]}")
        description_label.pack(side=tk.LEFT, padx=5)

        record_vars.append((i[0], var, record_frame))



# retrieve data from Open weather API
def get_weather(city):
    API_Key = "Your API Key Here"  # Replace with your actual API key
    if not API_Key or API_Key == "Your API Key Here":
        messagebox.showerror("Error", "Please enter a valid API key.")
        return None
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_Key}"
    res=requests.get(url)

    if res.status_code == 404:
        messagebox.showerror("Error", "City not found")
        return None
    
    weather = res.json()
    icon_id = weather['weather'][0]['icon']
    temperature = weather['main']['temp'] - 273.15  # Convert Kelvin to Celsius
    description = weather['weather'][0]['description']
    city_name = weather['name']
    country = weather['sys']['country']

    icon_url = f"https://openweathermap.org/img/wn/{icon_id}@2x.png"
    return[icon_url, temperature, description, city_name, country]

def get_weather_forecast(city):
    API_Key = "f93ae6e52a3d1641c10ed98ca2c22420"
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_Key}&units=metric&exclude=current,minutely,hourly,alerts"
   
    res=requests.get(url)

    if res.status_code == 404:
        messagebox.showerror("Error", "City not found")
        return None
    
    weather = res.json()
    
    forecast = []
    for i in range(0, len(weather['list']), 8):
        forecast.append({
            'day': i//8 + 1,
            'city': weather['city']['name'],
            'date': weather['list'][i]['dt_txt'],
            'temperature': weather['list'][i]['main']['temp'],
            'description': weather['list'][i]['weather'][0]['description']
        })
    return forecast

def show_weather_forecast(forecast):
    
    # Clear previous forecast
    for widget in forecast_frame.winfo_children():
        widget.destroy()
        
    # Get the weather forecast and display it
    
    for i in forecast:
        forecast_day = ttkbootstrap.Frame(forecast_frame)
        forecast_day.pack(side=tk.LEFT, padx=10)
        forecast_day_label = ttkbootstrap.Label(forecast_day, text=f"Day {i['day']}", font=("Helvetica", 10))
        forecast_day_label.pack()
        forecast_city_label = ttkbootstrap.Label(forecast_day, text=f"{i['city']}", font=("Helvetica", 10))
        forecast_city_label.pack()
        forecast_temperature_label = ttkbootstrap.Label(forecast_day, text=f"T: {i['temperature']}", font=("Helvetica", 10))
        forecast_temperature_label.pack()
        forecast_description_label = ttkbootstrap.Label(forecast_day, text=f"D: {i['description']}", font=("Helvetica", 10))
        forecast_description_label.pack()
        create_record(username_entry.get(), i['city'], i['date'], i['temperature'], i['description'])


def create_record(username,city,date,temperature,description):
    # check if any record exists for the user and city adn date
    cursor.execute("SELECT * FROM weather_data WHERE city=? AND date=?", (city, date))
    existing_record = cursor.fetchone()
    if existing_record is None:
        cursor.execute("INSERT INTO weather_data (username, city, date, temperature, description) VALUES (?, ?, ?, ?, ?)",
                        (username, city, date, temperature, description))
        conn.commit()
    

# Function to search weather information for a particular city
def search():
    city = city_entry.get()
    result = get_weather(city)
    if result is None:
        return
    #  when city found, display the weather information
    icon_url, temperature, description, city_name, country = result
    city_label.config(text=f"{city_name}, {country}")
    
    #get weather icon and update
    image = Image.open(requests.get(icon_url, stream=True).raw)
    icon= ImageTk.PhotoImage(image)
    image_label.config(image=icon)
    image_label.image = icon  # Keep a reference to avoid garbage collection

    # update the temperature and description labels
    temperature_label.config(text=f"{temperature:.2f} °C")
    weather_description_label.config(text=description.capitalize()) 

    forecast = get_weather_forecast(city)
    show_weather_forecast(forecast)


    records = history_read()
    history_show(records)

def delete_record():
    # Get the selected records from the scrollable frame
    for record_id, var, frame in record_vars:
        if var.get():
            cursor.execute("DELETE FROM weather_data WHERE id = ?", (record_id,))
            conn.commit()
    
    # Refresh the history display
    records = history_read()
    history_show(records)

root = ttkbootstrap.Window(title="Weather App", themename="solar")
root.geometry("800x950")

info_frame = ttkbootstrap.Frame(root)
info_frame.pack(pady=0)

creator_label = ttkbootstrap.Label(info_frame, text="Weather App by: Arya Nazare", font=("Helvetica", 10), bootstyle="info")
creator_label.pack(side=tk.LEFT, padx=10)

Cinfo_button = ttkbootstrap.Button(info_frame, text="Creator Info", command=lambda: messagebox.showinfo("Created for","Product Manager Accelerator: From entry-level to VP of Product, we support PM professionals through every stage of their careers."))
Cinfo_button.pack(side=tk.LEFT, padx=10)

userentry_label = ttkbootstrap.Label(root,text="Enter username:", font=("Helvetica", 10))
userentry_label.pack(pady=10)
username_entry = ttkbootstrap.Entry(root, font=("Helvetica", 18))
username_entry.pack(pady=0)

# input field for city name
cityentry_label = ttkbootstrap.Label(root,text="Enter city name:", font=("Helvetica", 10))
cityentry_label.pack(pady=10)
city_entry = ttkbootstrap.Entry(root, font=("Helvetica", 18))
city_entry.pack(pady=0)

# Button to search weather information
search_button = ttkbootstrap.Button(root, text="Search", command= search, bootstyle="primary")
search_button.pack(pady=10)

# city name label to display the city name
city_label = tk.Label(root, text="", font=("Helvetica", 18))  
city_label.pack(pady=10)

# Image label widget to add weather icon
image_label = tk.Label(root)
image_label.pack()

#  temperature label to display the temperature
temperature_label = tk.Label(root, text="", font=("Helvetica", 18))     
temperature_label.pack(pady=0)

# weather description label to display the weather description
weather_description_label = tk.Label(root, text="", font=("Helvetica", 18))
weather_description_label.pack(pady=3)

forecast_frame = ttkbootstrap.Frame(root)
forecast_frame.pack(pady=10)

delete_button = ttkbootstrap.Button(root, text="Delete Selected Records", command=delete_record, bootstyle="danger")
delete_button.pack(pady=10)

history_frame = ttkbootstrap.Frame(root)
history_frame.pack(pady=10)

scroll_frame = ctk.CTkScrollableFrame(root, width=680, height=300,fg_color="#0d5f6b",scrollbar_button_color="#c59701",scrollbar_button_hover_color="#886d00",label_text="Weather History",label_fg_color="#003840")
scroll_frame.pack(pady=1,  fill=tk.BOTH, expand=True)

root.mainloop()