import sqlite3
import json
from datetime import datetime

class WeatherDB:
    def __init__(self, db_file):
        self.db_file = db_file
        self.init_db()
    
    def init_db(self):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        
        # Create tables
        c.execute('''
            CREATE TABLE IF NOT EXISTS weather_readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                city TEXT,
                main TEXT,
                temp REAL,
                feels_like REAL,
                humidity REAL,
                wind_speed REAL,
                dt INTEGER,
                timestamp TEXT
            )
        ''')
        
        c.execute('''
            CREATE TABLE IF NOT EXISTS daily_summaries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                city TEXT,
                avg_temp REAL,
                max_temp REAL,
                min_temp REAL,
                dominant_weather TEXT,
                readings INTEGER,
                UNIQUE(date, city)
            )
        ''')
        
        c.execute('''
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                city TEXT,
                message TEXT,
                type TEXT,
                timestamp TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_weather_data(self, data):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        
        for reading in data:
            c.execute('''
                INSERT INTO weather_readings 
                (city, main, temp, feels_like, humidity, wind_speed, dt, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                reading['city'], reading['main'], reading['temp'],
                reading['feels_like'], reading['humidity'], reading['wind_speed'],
                reading['dt'], reading['timestamp']
            ))
        
        conn.commit()
        conn.close()