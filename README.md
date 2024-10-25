# Real-Time Data Processing System for Weather Monitoring

This project is a real-time weather monitoring and alerting system, analyzing data from various cities. It visualizes temperature trends, summarizes daily data, and provides visualizations for weather data.
Check out the Deployed application here https://real-time-data-processing-system-for-weather-monitoring-navy.vercel.app/

## Features
- **Real-Time Data Fetching**: Retrieves weather data using OpenWeather API.
- **Temperature Analysis**: Summarizes daily temperature averages, maximums, and minimums.
- **Data Visualization**: Plots daily temperature trends using Victory charts.

## Installation
1. Clone the repository:
```bash
 git clone https://github.com/OmHawaldar/Real-Time-Data-Processing-System-for-Weather-Monitoring.git
```
2.Install Dependencies:
```bash
npm install
```
3.Replace your OpenWeather API key in .env file
```
OPENWEATHER_API_KEY= "replace here"
```
4. Run the Project
```
npm run dev
```
## Project Structure

- **src/components**: React components for weather cards, chart, preferences form, and visualizations.
- **src/services**: Contains `weatherApi.js` for API interactions.
- **src/hooks**: Custom hook for theme management.
- **src/types**: TypeScript interfaces for data structures.

## Usage

1. Update `CITIES` in `App.js` to include cities of interest.
2. Set user preferences for temperature unit, alert threshold, and theme.
3. View real-time updates and receive alerts for high temperatures.

## Contributing

Feel free to open issues and submit pull requests.
Contact hawaldarom39@gmail.com
