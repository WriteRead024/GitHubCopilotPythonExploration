# 'tkagg-graph.py' 
# adapted from tutorial
# https://pythonprogramming.net/how-to-embed-matplotlib-graph-tkinter-gui/
# for use in 'evaluate-random-data-graph-window.py'
# devtested with 'graph-window.py'
# 4/10/2024
# Rich W.
# using
# GitHub Copilot

import tkinter as tk

#
# matplotlib import and setup
import matplotlib
#
# Use the TkAgg backend for matplotlib
# AGG probably means 'Anti-Grain Geometry'
# (https://github.com/matplotlib/matplotlib/blob/v3.8.4/lib/matplotlib/backends/backend_agg.py#L2)
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class TkaggGraph(tk.Frame):    

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.graph_header_label = tk.Label(self, text="Graph Page", font=controller.child_font)
        self.graph_header_label.pack(padx=2,pady=2)

        # instantiate and expose the figure and subplot as class instance attributes
        self.fig = Figure(figsize=(5, 5), dpi=100)
        # 111 indicates the grid position of the subplot
        self.subplot = self.fig.add_subplot(111)
        
        # plot some default data
        self.subplot.plot([1, 2, 3, 4, 5], [4, 4, 4, 4, 3])

        # instantiate and show the canvas
        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.canvas.draw()

        