export interface WeatherData {
  city: string;
  main: string;
  temp: number;
  feels_like: number;
  dt: number;
  humidity?: number;
  wind_speed?: number;
}

export interface DailySummary {
  date: string;
  city: string;
  avgTemp: number;
  maxTemp: number;
  minTemp: number;
  dominantWeather: string;
  readings: number;
}

export interface AlertConfig {
  maxTemp: number;
  minTemp: number;
  consecutive: number;
}

export interface Alert {
  city: string;
  message: string;
  timestamp: number;
  type: 'warning' | 'danger';
}