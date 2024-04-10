#'multi-y-axis-graph-window.py'
# written 4/10/2024
# for testing the multi-y-axis-tkagg-graph.py class
# Rich W.
# using
# GitHub Copilot

import tkinter as tk

import importlib
MultiYAxisTkaggGraph = importlib.import_module("multi-y-axis-tkagg-graph").MultiYAxisTkaggGraph
GraphDataObj = importlib.import_module("multi-y-axis-tkagg-graph").GraphDataObj

ARIAL_FONT = ("Arial", 12)

graph_window = tk.Tk()
graph_window.title("Graph Window")
graph_window.child_font = ARIAL_FONT

# create a GraphDataObj instance with example data
graph_data_obj = GraphDataObj()
graph_data_obj.number_counts = [2, 2, 3, 4, 4]
graph_data_obj.chi_square_values = [10, 20, 5, 14, 15]
graph_data_obj.p_values = [.35, .45, .55, .65, .75]
graph_data_obj.number_of_results = 5
graph_data_obj.min_count = 1
graph_data_obj.max_count = 5
graph_data_obj.min_chi_square = 5
graph_data_obj.max_chi_square = 20
graph_data_obj.min_p_value = .35
graph_data_obj.max_p_value = .75

# Create an instance of the class
graph = MultiYAxisTkaggGraph(graph_window, graph_window, graph_data_obj)

# Pack the graph to make it visible
graph.pack()

# Start the Tkinter event loop
graph_window.mainloop()