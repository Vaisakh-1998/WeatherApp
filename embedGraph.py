from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

Y = [20 for _ in range(8)]
X = ["Today", "sun", "Mon", "Tue", "Wen", "Thu", "Fri", "Str"]
Y1 = [15 for _ in range(8)]
Y2 = [30 for _ in range(8)]

class EmbedGraph:
	def __init__(self, tk_widget, x_data=X, y_data=Y, y1_data=Y1, y2_data=Y2):
		self.tk_widget = tk_widget
		self.x = x_data
		self.y = y_data
		self.y1 = y1_data
		self.y2 = y2_data	
		self.yticks = [15, 20, 25, 30]
		self.fig, self.plot = self.create_figure()
	
	
	def add_values(self, x, y, y1, y2):
		n = len(x)
		for i in range(n):
			self.plot.text(x[i], y[i]+.5, f"{y[i]}°",
			horizontalalignment='center',verticalalignment='center')
			self.plot.text(x[i], y1[i]+.5, f"{y1[i]}°",
			horizontalalignment='center',verticalalignment='center')
			self.plot.text(x[i], y2[i]+.5, f"{y2[i]}°",
			horizontalalignment='center',verticalalignment='center')
				
	def create_figure(self):
		fig = Figure(figsize=(5,5), dpi=100)
		plt = fig.add_subplot(1, 1, 1)
		plt.plot(self.x, self.y, label="avg")
		plt.plot(self.x, self.y1, label="min")
		plt.plot(self.x, self.y2, label="max")
		plt.legend()
		plt.set_yticks(self.yticks)
		return fig, plt
	
	def update_plot(self, x, y, y1, y2):
		self.plot.clear()
		self.plot.plot(x, y, label="avg")
		self.plot.plot(x, y1, label="min")
		self.plot.plot(x, y2, label="max")
		self.plot.legend()
		self.plot.set_yticks(self.yticks)
		self.plot.set_ylim(0, max(y2)+5)
		self.add_values(x, y, y1, y2)
		
	def embed(self):
		canvas = FigureCanvasTkAgg(figure=self.fig, master=self.tk_widget)
		canvas.draw()
		canvas.get_tk_widget().pack(expand=True, fill="both")

if __name__ == "__main__":
	gui = tk.Tk()
	grp = EmbedGraph(gui)
	grp.embed()
	gui.mainloop()