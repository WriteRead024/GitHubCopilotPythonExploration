#'graph-window.py'
# written 4/10/2024
# for testing the tkagg-graph.py class
# Rich W.
# using one or two lines from
# GitHub Copilot

import tkinter as tk

import importlib
TkaggGraph = importlib.import_module("tkagg-graph").TkaggGraph

ARIAL_FONT = ("Arial", 12)

graph_window = tk.Tk()
graph_window.title("Graph Window")
graph_window.child_font = ARIAL_FONT

# Create an instance of the class
graph = TkaggGraph(graph_window, controller=graph_window)

# Pack the graph to make it visible
graph.pack()

# Start the Tkinter event loop
graph_window.mainloop()