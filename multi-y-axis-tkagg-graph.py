# 'multi-y-axis-tkagg-graph.py'
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


class GraphDataObj:
    def __init__(self):
        self.number_counts = []
        self.chi_square_values = []
        self.p_values = []
        self.number_of_results = 0
        self.min_count = 1
        self.max_count = 10
        self.min_chi_square = 0
        self.max_chi_square = 10
        self.min_p_value = 0
        self.max_p_value = 1


class MultiYAxisTkaggGraph(tk.Frame):    

    def __init__(self, parent, controller, arg_graph_data_obj=None):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.graph_header_label = tk.Label(self, text="Multi Y-Axis Graph", font=controller.child_font)
        self.graph_header_label.pack(padx=2,pady=2)

        # instantiate and expose the figure and subplot as class instance attributes
        self.fig = Figure(figsize=(5, 5), dpi=100)
        # 111 indicates the grid position of the subplot
        self.subplot = self.fig.add_subplot(111)

        # graph display setup with additional figure plot axes
        self.fig.subplots_adjust(right=0.8)
        axis_1 = self.fig.axes[0]
        axis_twin_1 = axis_1.twinx()
        axis_twin_2 = axis_1.twinx()
        axis_twin_2.spines['right'].set_position(('axes', 1.1))
        axis_1.set_ylim(arg_graph_data_obj.min_count, arg_graph_data_obj.max_count)
        axis_twin_1.set_ylim(arg_graph_data_obj.min_chi_square, arg_graph_data_obj.max_chi_square)
        axis_twin_2.set_ylim(arg_graph_data_obj.min_p_value, arg_graph_data_obj.max_p_value)
        x_axis_values = list(range(1, arg_graph_data_obj.number_of_results + 1))
        p1 = axis_1.plot(x_axis_values, arg_graph_data_obj.number_counts, "C0", label="Number Counts")
        p2 = axis_twin_1.plot(x_axis_values, arg_graph_data_obj.chi_square_values, "C1", label="Chi-Square Values")
        p3 = axis_twin_2.plot(x_axis_values, arg_graph_data_obj.p_values, "C2", label="p Values")
        self.fig.axes[0].set_xlim(1, arg_graph_data_obj.number_of_results)

        # set the colors for the axes and labels
        axis_1.yaxis.label.set_color(p1[0].get_color())
        axis_twin_1.yaxis.label.set_color(p2[0].get_color())
        axis_twin_2.yaxis.label.set_color(p3[0].get_color())
        axis_1.tick_params(axis='y', colors=p1[0].get_color())
        axis_twin_1.tick_params(axis='y', colors=p2[0].get_color())
        axis_twin_2.tick_params(axis='y', colors=p3[0].get_color())

        # turn on the legend
        axis_1.legend(handles=[p1[0], p2[0], p3[0]], loc='upper left')

        # instantiate and show the canvas
        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.canvas.draw()

        