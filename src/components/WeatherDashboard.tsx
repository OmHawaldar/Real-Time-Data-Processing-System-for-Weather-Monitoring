import React, { useEffect, useState } from 'react';
import { format } from 'date-fns';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { CloudRain, Thermometer, Wind, Droplets } from 'lucide-react';
import { WeatherData, DailySummary, Alert, AlertConfig } from '../types/weather';
import { fetchWeatherData, calculateDailySummary, checkAlerts } from '../utils/weather';

const ALERT_CONFIG: AlertConfig = {
  maxTemp: 35,
  minTemp: 10,
  consecutive: 2
};

const UPDATE_INTERVAL = 300000; // 5 minutes

export default function WeatherDashboard() {
  const [weatherData, setWeatherData] = useState<WeatherData[]>([]);
  const [dailySummaries, setDailySummaries] = useState<DailySummary[]>([]);
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [lastUpdate, setLastUpdate] = useState<Date>();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const data = await fetchWeatherData();
        setWeatherData(prev => [...prev, ...data]);
        
        const summaries = calculateDailySummary([...weatherData, ...data]);
        setDailySummaries(summaries);
        
        const newAlerts = checkAlerts(data, ALERT_CONFIG);
        if (newAlerts.length > 0) {
          setAlerts(prev => [...newAlerts, ...prev]);
        }
        
        setLastUpdate(new Date());
      } catch (error) {
        console.error('Error fetching weather data:', error);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, UPDATE_INTERVAL);
    
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <header className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Weather Monitoring System</h1>
          {lastUpdate && (
            <p className="text-sm text-gray-500">
              Last updated: {format(lastUpdate, 'PPpp')}
            </p>
          )}
        </header>

        {/* Current Weather Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
          {weatherData
            .filter((data, index, self) => 
              index === self.findIndex(d => d.city === data.city)
            )
            .map(data => (
              <div key={data.city} className="bg-white rounded-lg shadow-sm p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">{data.city}</h3>
                <div className="space-y-3">
                  <div className="flex items-center">
                    <Thermometer className="w-5 h-5 text-red-500 mr-2" />
                    <span>{data.temp.toFixed(1)}°C</span>
                  </div>
                  <div className="flex items-center">
                    <CloudRain className="w-5 h-5 text-blue-500 mr-2" />
                    <span>{data.main}</span>
                  </div>
                  <div className="flex items-center">
                    <Wind className="w-5 h-5 text-gray-500 mr-2" />
                    <span>{data.wind_speed} m/s</span>
                  </div>
                  <div className="flex items-center">
                    <Droplets className="w-5 h-5 text-blue-400 mr-2" />
                    <span>{data.humidity}%</span>
                  </div>
                </div>
              </div>
            ))}
        </div>

        {/* Temperature Chart */}
        <div className="bg-white rounded-lg shadow-sm p-6 mb-8">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Temperature Trends</h2>
          <div className="h-[400px]">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={weatherData.slice(-48)} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis 
                  dataKey="dt" 
                  tickFormatter={(dt) => format(new Date(dt * 1000), 'HH:mm')}
                />
                <YAxis />
                <Tooltip 
                  labelFormatter={(dt) => format(new Date(dt * 1000), 'PPpp')}
                  formatter={(value: number) => [`${value.toFixed(1)}°C`]}
                />
                <Legend />
                {Array.from(new Set(weatherData.map(d => d.city))).map((city, index) => (
                  <Line
                    key={city}
                    type="monotone"
                    dataKey="temp"
                    data={weatherData.filter(d => d.city === city)}
                    name={city}
                    stroke={`hsl(${index * 60}, 70%, 50%)`}
                    dot={false}
                  />
                ))}
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Alerts */}
        {alerts.length > 0 && (
          <div className="bg-white rounded-lg shadow-sm p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Recent Alerts</h2>
            <div className="space-y-4">
              {alerts.slice(0, 5).map((alert, index) => (
                <div
                  key={index}
                  className={`p-4 rounded-lg ${
                    alert.type === 'danger' ? 'bg-red-50' : 'bg-yellow-50'
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <div>
                      <h3 className="font-medium">{alert.city}</h3>
                      <p className="text-sm">{alert.message}</p>
                    </div>
                    <span className="text-sm text-gray-500">
                      {format(new Date(alert.timestamp * 1000), 'PPp')}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}