import tkinter as tk
from getWeather import GetWeather
from embedGraph import EmbedGraph
from PIL import ImageTk

WHITE = "#FFFFFF"
BLACK = "#25265E"
SEARCH_FONT = ("Arial", 12)
DL_FONT = ("Arial", 6)
SMALL_FONT_STYLE = ("Arial Baltic", 10)
LARGE_FONT_STYLE = ("Modern", 27, "bold")

class WeatherApp:
	def __init__(self):
		self.window = tk.Tk()
		self.window.title("Weather App")
		#self.window.geometry("1000x800")
		
		self.search_frame = self.create_search_frame()
		for i in range(2):
			self.search_frame.columnconfigure(i, weight=1)
			self.search_frame.rowconfigure(i, weight=1)
			
		self.search_entry = self.create_search_widgets()
		
		self.temp_frame = self.create_temp_frame()
		for i in range(2):
			self.temp_frame.columnconfigure(i, weight=1)
			self.temp_frame.rowconfigure(i, weight=1)
		self.temp_frame.rowconfigure(2, weight=1)
			
		self.text = ["feels like", "pressure", "humidity", "wind speed", "visibility", "uv"]
		
		self.dt_label = self.create_dt_label()
		self.location_label = self.create_location_label()
		self.temp_icon_label, self.temp_label = self.create_temp_label()
		self.description_label = self.create_description_label()
		self.min_max_label, self.sunset_rise_label = self.create_min_max()
		
		self.weather_frame = self.create_weather_frame()	
		for i in range(2):
			self.weather_frame.columnconfigure(i, weight=1)
			self.weather_frame.rowconfigure(i, weight=1)
					
		self.weather_labels = self.create_weather_label()
		
		self.graph_frame = self.create_graph_frame()
		
		self.graph = self.create_graph()

	def create_search_frame(self):
		frame = tk.Frame(self.window, bg=WHITE)
		frame.pack(fill="both", expand=True)
		return frame
	
	def error_message(self):
		tk.messagebox.showerror("Error", "invalid city name")
	
	def get_weather(self):
		city = self.search_entry.get()
		weather = GetWeather(city)
		if weather.json:
			self.update_labels(weather)
			self.update_graph_data(weather)
		else:
			self.error_message()
			
	def create_search_widgets(self):
		entry = tk.Entry(self.search_frame, border=0, justify="center", font=SEARCH_FONT)
		entry.grid(row=0, column=0, padx=20, pady=50, sticky="nsew")
		
		button = tk.Button(self.search_frame, text="search", command=self.get_weather)
		button.grid(row=0, column=1)
		return entry
		
	def create_temp_frame(self):
		frame = tk.Frame(self.window, bg=WHITE)
		frame.pack(fill="both", expand=True)
		return frame
	
	def create_dt_label(self):
		label = tk.Label(self.temp_frame, width=25, anchor="w",
	    bg =WHITE, font=DL_FONT)
		label.grid(row=0, column=0)
		return label
		
	def create_location_label(self):
		label = tk.Label(self.temp_frame, text="....", width=25, anchor="w",
		bg =WHITE, font = DL_FONT)
		label.grid(row=1, column=0, padx=50)
		return label
		
	def create_temp_label(self):
		label_icon = tk.Label(self.temp_frame, bg=WHITE)
		label_icon.grid(row=2, column=0, sticky="nsew")
		label = tk.Label(self.temp_frame, text="....", 
	    font=LARGE_FONT_STYLE, bg=WHITE)
		label.grid(row=4, column=0, sticky="nsew")
		return label_icon, label
	
	def create_description_label(self):
		label = tk.Label(self.temp_frame, font=SMALL_FONT_STYLE, bg=WHITE)
		label.grid(row=5, column=0)
		return label
	
	def create_min_max(self):
		label1 = tk.Label(self.temp_frame, text="\u2193 .... \u2191....", font=DL_FONT,
		bg=WHITE, width=39, anchor="w")
		label1.grid(row=0, column=1, sticky="nsew")
		
		label2 = tk.Label(self.temp_frame, text="sunrise ...., sunset ....", font=DL_FONT,
		bg=WHITE, width=39, anchor="w")
		label2.grid(row=1, column=1, sticky="nsew")
		
		return label1, label2
	
	def create_weather_frame(self):
		frame = tk.Frame(self.temp_frame, bg=WHITE, pady=40)
		frame.grid(row=2, column=1, sticky="nsew", rowspan=3)
		return frame				
					
	def create_weather_label(self):
		j = 0
		labels = []
		for i in range(6):
			label1 = tk.Label(self.weather_frame, text=self.text[j], 
			bg=WHITE, width=13, anchor="w", font=SMALL_FONT_STYLE)
			label1.grid(row=i, column=1, sticky="nsew")
			
			label2 = tk.Label(self.weather_frame, text="....", bg=WHITE, 
			width=10, anchor="w",font=SMALL_FONT_STYLE)
			label2.grid(row=i, column=2, sticky="nsew")
			labels.append(label2)		
			j += 1
		return labels
	
	def update_min_max(self, weather):
		data = weather.weather
		min_temp = "\u2193" + data["min"]
		max_temp = "\u2191" + data["max"]
		sunrise = "sunrise:" + data["sunrise"]
		sunset = "sunset:" + data["sunset"]
		self.min_max_label.config(text=min_temp + max_temp)
		self.sunset_rise_label.config(text=sunrise+", "+sunset)
	
	def update_weather_labels(self, weather):
		data = weather.weather
		
		temp = data["temp"]
		self.temp_label.config(text=f"{temp}")
		self.description_label.config(text=data["description"])
		
		i = 0
		for key in self.text:
			self.weather_labels[i].config(text=data[key])
			i += 1
	
	def update_labels(self, weather):
		self.dt_label.config(text=weather.date_time)
		self.location_label.config(text=weather.location)
		
		img = weather.icon_png.resize((300,300))
		img = ImageTk.PhotoImage(img)
		self.temp_icon_label.config(image=img)
		self.temp_icon_label.image = img
		self.update_min_max(weather)
		self.update_weather_labels(weather)
		
	def create_graph_frame(self):
		frame = tk.Frame(self.window, bg=WHITE)
		frame.pack(fill="both", expand=True)
		return frame
		
	def update_graph_data(self, weather):
		x= weather.forcast["day"]
		y = weather.forcast["avg_temp"]
		y1 = weather.forcast["min_temp"]
		y2 = weather.forcast["max_temp"]
		self.update_graph(x, y, y1, y2)
				
	def create_graph(self):
		graph = EmbedGraph(self.graph_frame)
		graph.embed()	
		return graph
	
	def update_graph(self, x, y, y1, y2):
		self.graph.update_plot(x, y, y1, y2)
				
	def run(self):
		self.window.mainloop()

if __name__ == "__main__":
	app = WeatherApp()
	app.run()