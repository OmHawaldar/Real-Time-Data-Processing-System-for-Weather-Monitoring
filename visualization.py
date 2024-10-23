import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import sqlite3
from datetime import datetime, timedelta

class WeatherVisualizer:
    def __init__(self, db_file):
        self.db_file = db_file
    
    def create_temperature_chart(self):
        conn = sqlite3.connect(self.db_file)
        
        # Get last 24 hours of data
        query = """
            SELECT city, timestamp, temp
            FROM weather_readings
            WHERE timestamp >= datetime('now', '-1 day')
            ORDER BY timestamp
        """
        
        df = pd.read_sql_query(query, conn)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        fig = px.line(df, x='timestamp', y='temp', color='city',
                     title='Temperature Variation (Last 24 Hours)')
        fig.write_html('temperature_chart.html')
        
    def create_daily_summary_chart(self):
        conn = sqlite3.connect(self.db_file)
        
        query = """
            SELECT *
            FROM daily_summaries
            ORDER BY date DESC
            LIMIT 7
        """
        
        df = pd.read_sql_query(query, conn)
        
        fig = go.Figure()
        
        for city in df['city'].unique():
            city_data = df[df['city'] == city]
            fig.add_trace(go.Bar(
                name=city,
                x=city_data['date'],
                y=city_data['avg_temp'],
                error_y=dict(
                    type='data',
                    symmetric=False,
                    array=city_data['max_temp'] - city_data['avg_temp'],
                    arrayminus=city_data['avg_temp'] - city_data['min_temp']
                )
            ))
        
        fig.update_layout(
            title='Daily Temperature Summary (Last 7 Days)',
            barmode='group'
        )
        fig.write_html('daily_summary.html')
        
    def create_alert_dashboard(self):
        conn = sqlite3.connect(self.db_file)
        
        query = """
            SELECT *
            FROM alerts
            WHERE timestamp >= datetime('now', '-24 hours')
            ORDER BY timestamp DESC
        """
        
        df = pd.read_sql_query(query, conn)
        
        fig = go.Figure(data=[go.Table(
            header=dict(values=['City', 'Message', 'Type', 'Timestamp'],
                       fill_color='paleturquoise',
                       align='left'),
            cells=dict(values=[df['city'], df['message'], df['type'], df['timestamp']],
                      fill_color='lavender',
                      align='left'))
        ])
        
        fig.update_layout(title='Recent Alerts (Last 24 Hours)')
        fig.write_html('alerts_dashboard.html')