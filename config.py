import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
API_KEY = os.getenv('OPENWEATHER_API_KEY')
CITIES = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']
UPDATE_INTERVAL = 300  # 5 minutes in seconds

# Alert Thresholds
ALERT_CONFIG = {
    'max_temp': 35,
    'min_temp': 10,
    'consecutive_readings': 2
}

# Database Configuration
DB_FILE = 'weather_data.db'