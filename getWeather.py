import requests
from geopy.geocoders import Nominatim 
import json
from PIL import Image
from datetime import datetime
import pytz

API_KEY = "b4c4ada6a2c91b2a126721df62de169d"

class GetWeather:
	def __init__(self, city):
		self.city = city
		self.geocode = self.get_geocode()
		self.json = self.get_json()
		if self.json:
			self.time_zone = self.get_time_zone()
			self.weather = self.get_weather()
			self.icon_png = self.get_weather_icon()
			self.date_time = self.get_date_time()
			self.location = self.get_location()
			self.forcast = self.get_forcast()

				
	def get_geocode(self):
		try:
			geo = Nominatim(user_agent="weather app")
			location = geo.geocode(self.city)
		except:
			location = None		
		return location		
	
	def check_valid(self):
		if not self.geocode:
			return False
		city_name = self.geocode.address
		if self.city in city_name:
			return True
		return False
			
	def get_json(self):
		#if not self.check_valid():
			#return None
		if  not self.geocode:
			return None
		lon , lat = self.geocode.longitude, self.geocode.latitude
		url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&appid={API_KEY}&units=metric&exclude=minutely,hourly,alerts"
		api_data = requests.get(url).text		
		return json.loads(api_data)
		
	def get_weather(self):
		temp = round(self.json["current"]["temp"])
		feels_like = round(self.json["current"]["feels_like"])
		pressure = self.json["current"]["pressure"]
		wind = round(self.json["current"]["wind_speed"],1)
		humidity = self.json["current"]["humidity"]
		visibility = round((self.json["current"]["visibility"])/1000, 1)
		uv = round(self.json["current"]["uvi"], 1)
		min_temp = round(self.json["daily"][0]["temp"]["min"])
		max_temp = round(self.json["daily"][0]["temp"]["max"])
		
		ri_dt = self.json["current"]["sunrise"]
		sunrise = datetime.fromtimestamp(ri_dt, tz=self.time_zone)
		st_dt = self.json["current"]["sunset"]
		sunset = datetime.fromtimestamp(st_dt, tz=self.time_zone)
																		
		weather = {
		"temp": f"{temp}°C",
		"feels like": f"{feels_like}°C", 
		"description": self.json["current"]["weather"][0]["description"],
		 "pressure": f"{pressure}hpa", 
		 "wind speed": f"{wind}m/s", 
		 "humidity": f"{humidity}%", 
		 "visibility": f"{visibility}km",
		 "uv": f"{uv}",
		 "min": f"{min_temp}°",
		 "max": f"{max_temp}°",
		 "sunrise":sunrise.strftime("%-I:%M %p"),
		 "sunset": sunset.strftime("%-I:%M %p")
		 }
		return weather
	
	def get_weather_icon(self):
		icon = self.json["current"]["weather"][0]["icon"]
		path = f"image/{icon}@2x.png"
		return Image.open(path)
	
	def get_time_zone(self):
		time_zone = pytz.timezone(self.json["timezone"])
		return time_zone
	
	def get_date_time(self):
		dt = datetime.now(tz=self.time_zone)
		return dt.strftime("%-I:%M %p, %a, %b %-d, %Y")
	
	def get_location(self):
		adress = self.geocode.address
		country = adress.rsplit(',', 1)[1]
		return f"{self.city},{country}"
	
	def scrap_temp(self, day):
		# helper funtion
		data = []
		for i in range(8):
			temp_data = round(self.json["daily"][i]["temp"][day])
			data.append(temp_data)
		return data
	
	def get_forcast(self):
		# daily forcast for avg, min, max temperature
		forcast = {"day": [], "avg_temp": [], "min_temp": [], "max_temp": []}
		for i in range(8):
			day = self.json["daily"][i]["dt"]
			dt = datetime.fromtimestamp(day)
			forcast["day"].append(dt.strftime("%-d%a"))
		forcast["day"][0] = "Today"			
		forcast["avg_temp"] = self.scrap_temp("day")
		forcast["min_temp"] = self.scrap_temp("min")
		forcast["max_temp"] = self.scrap_temp("max")
		return forcast
		

if __name__ == "__main__":
	wea = GetWeather("trivandrum")
	#print(wea.geocode.address)
	print(json.dumps(wea.json, indent=4))
	print(wea.weather)
	#print(wea.icon_png)
	print(wea.date_time)
	print(wea.location)
	print(wea.forcast)
	
	
	
