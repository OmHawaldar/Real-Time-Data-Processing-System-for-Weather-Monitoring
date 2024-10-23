import { WeatherData, DailySummary, Alert, AlertConfig } from '../types/weather';

const API_KEY = '588725fefd531d52239a9c00ba7dbab1';
const CITIES = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad'];

export const fetchWeatherData = async (): Promise<WeatherData[]> => {
  const weatherData = await Promise.all(
    CITIES.map(async (city) => {
      const response = await fetch(
        `https://api.openweathermap.org/data/2.5/weather?q=${city},in&appid=${API_KEY}`
      );
      const data = await response.json();
      
      return {
        city,
        main: data.weather[0].main,
        temp: kelvinToCelsius(data.main.temp),
        feels_like: kelvinToCelsius(data.main.feels_like),
        humidity: data.main.humidity,
        wind_speed: data.wind.speed,
        dt: data.dt
      };
    })
  );
  
  return weatherData;
};

export const kelvinToCelsius = (kelvin: number): number => {
  return Math.round((kelvin - 273.15) * 100) / 100;
};

export const calculateDailySummary = (readings: WeatherData[]): DailySummary[] => {
  const summaryMap = new Map<string, WeatherData[]>();
  
  readings.forEach(reading => {
    const date = new Date(reading.dt * 1000).toISOString().split('T')[0];
    const key = `${date}-${reading.city}`;
    
    if (!summaryMap.has(key)) {
      summaryMap.set(key, []);
    }
    summaryMap.get(key)!.push(reading);
  });
  
  return Array.from(summaryMap.entries()).map(([key, cityReadings]) => {
    const [date, city] = key.split('-');
    const temps = cityReadings.map(r => r.temp);
    const weatherTypes = cityReadings.map(r => r.main);
    
    return {
      date,
      city,
      avgTemp: temps.reduce((a, b) => a + b, 0) / temps.length,
      maxTemp: Math.max(...temps),
      minTemp: Math.min(...temps),
      dominantWeather: getDominantWeather(weatherTypes),
      readings: cityReadings.length
    };
  });
};

export const checkAlerts = (
  readings: WeatherData[],
  config: AlertConfig
): Alert[] => {
  return readings
    .filter(reading => reading.temp > config.maxTemp || reading.temp < config.minTemp)
    .map(reading => ({
      city: reading.city,
      message: `Temperature ${reading.temp > config.maxTemp ? 'above' : 'below'} threshold: ${reading.temp}°C`,
      timestamp: reading.dt,
      type: reading.temp > config.maxTemp ? 'danger' : 'warning'
    }));
};

const getDominantWeather = (types: string[]): string => {
  const counts = types.reduce((acc, type) => {
    acc[type] = (acc[type] || 0) + 1;
    return acc;
  }, {} as Record<string, number>);
  
  return Object.entries(counts).sort((a, b) => b[1] - a[1])[0][0];
};