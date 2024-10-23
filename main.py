import schedule
import time
from weather_api import WeatherAPI
from database import WeatherDB
from analysis import WeatherAnalyzer
from visualization import WeatherVisualizer
from config import DB_FILE, UPDATE_INTERVAL

def run_weather_monitoring():
    # Initialize components
    weather_api = WeatherAPI()
    db = WeatherDB(DB_FILE)
    analyzer = WeatherAnalyzer(DB_FILE)
    visualizer = WeatherVisualizer(DB_FILE)
    
    try:
        # Fetch current weather data
        weather_data = weather_api.fetch_weather_data()
        
        # Save to database
        db.save_weather_data(weather_data)
        
        # Calculate daily summary
        analyzer.calculate_daily_summary()
        
        # Check for alerts
        alerts = analyzer.check_alerts(weather_data)
        if alerts:
            print("⚠️ New Alerts:")
            for alert in alerts:
                print(f"{alert['city']}: {alert['message']} ({alert['timestamp']})")
        
        # Update visualizations
        visualizer.create_temperature_chart()
        visualizer.create_daily_summary_chart()
        visualizer.create_alert_dashboard()
        
        print(f"✅ Weather monitoring update completed at {time.strftime('%Y-%m-%d %H:%M:%S')}")
        
    except Exception as e:
        print(f"❌ Error in weather monitoring: {str(e)}")

def main():
    print("🌤️ Starting Weather Monitoring System...")
    
    # Run immediately on start
    run_weather_monitoring()
    
    # Schedule regular updates
    schedule.every(UPDATE_INTERVAL).seconds.do(run_weather_monitoring)
    
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()