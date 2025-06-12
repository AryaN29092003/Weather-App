🌤️ Weather App - Tkinter + OpenWeather API

This is a Python GUI Weather App built with Tkinter, ttkbootstrap, and customtkinter, which fetches current and forecast weather data using the OpenWeatherMap API. It stores searched data locally using SQLite and allows users to view, scroll through, and delete past records.

🔧 Features

Current weather by city name input.

5-day weather forecast display.

Save forecast data with username, date, and description.

SQLite DB integration for persistent search history.

Scrollable history view with selectable deletion.

Clean and styled UI using ttkbootstrap and customtkinter.

🧠 Development Steps

Studied multiple weather APIs and chose OpenWeatherMap for real-time data and forecast.

Implemented current weather UI and input handling.

Developed UI for 5-day forecast display.

Created SQLite DB (weather_search_history.db) and table (weather_data) to store forecast data.

Added logic to insert new search results only if not already present.

Built scrollable frame to read/display all DB records.

Integrated record deletion functionality using checkboxes.

🚀 Steps to Run

1.Clone the repository

2.Create and activate a virtual environment

3.Install required packages

4.Run the WeatherApp.py application
