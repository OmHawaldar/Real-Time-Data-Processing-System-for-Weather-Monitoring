import pandas as pd
from datetime import datetime, timedelta
import sqlite3
from config import ALERT_CONFIG

class WeatherAnalyzer:
    def __init__(self, db_file):
        self.db_file = db_file
    
    def calculate_daily_summary(self):
        conn = sqlite3.connect(self.db_file)
        
        # Get today's date
        today = datetime.now().strftime('%Y-%m-%d')
        
        # Calculate daily aggregates
        query = f"""
            SELECT 
                city,
                AVG(temp) as avg_temp,
                MAX(temp) as max_temp,
                MIN(temp) as min_temp,
                COUNT(*) as readings,
                GROUP_CONCAT(main) as weather_conditions
            FROM weather_readings
            WHERE date(timestamp) = '{today}'
            GROUP BY city
        """
        
        df = pd.read_sql_query(query, conn)
        
        # Calculate dominant weather
        for index, row in df.iterrows():
            weather_list = row['weather_conditions'].split(',')
            dominant = max(set(weather_list), key=weather_list.count)
            
            # Save summary to database
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO daily_summaries 
                (date, city, avg_temp, max_temp, min_temp, dominant_weather, readings)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                today, row['city'], row['avg_temp'], row['max_temp'],
                row['min_temp'], dominant, row['readings']
            ))
        
        conn.commit()
        conn.close()
    
    def check_alerts(self, current_data):
        alerts = []
        conn = sqlite3.connect(self.db_file)
        
        for reading in current_data:
            # Check for temperature thresholds
            if reading['temp'] > ALERT_CONFIG['max_temp']:
                # Check if this is the second consecutive reading
                query = f"""
                    SELECT COUNT(*) FROM weather_readings
                    WHERE city = '{reading['city']}'
                    AND temp > {ALERT_CONFIG['max_temp']}
                    AND dt > {reading['dt'] - (ALERT_CONFIG['consecutive_readings'] * 300)}
                """
                cursor = conn.cursor()
                cursor.execute(query)
                count = cursor.fetchone()[0]
                
                if count >= ALERT_CONFIG['consecutive_readings']:
                    alert = {
                        'city': reading['city'],
                        'message': f"High temperature alert: {reading['temp']}°C",
                        'type': 'danger',
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    alerts.append(alert)
                    
                    # Save alert to database
                    cursor.execute('''
                        INSERT INTO alerts (city, message, type, timestamp)
                        VALUES (?, ?, ?, ?)
                    ''', (alert['city'], alert['message'], alert['type'], alert['timestamp']))
        
        conn.commit()
        conn.close()
        return alerts