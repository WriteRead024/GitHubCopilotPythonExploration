# 'evaluate-random-data-graph-window.py' adapted 4/10/2024 from
# 'evaluate-random-data-window.py' started 2/8/2024
#
# Rich W.
# using
# GitHub Copilot
# and tutorial from
# https://pythonprogramming.net/how-to-embed-matplotlib-graph-tkinter-gui/
#

import tkinter as tk
import importlib
import sys
sys.path.append('..')
erd = importlib.import_module("evaluate-random-data")
MultiYAxisTkaggGraph = importlib.import_module("multi-y-axis-tkagg-graph").MultiYAxisTkaggGraph
GraphDataObj = importlib.import_module("multi-y-axis-tkagg-graph").GraphDataObj


ARIAL_FONT = ("Arial", 12)

graph_data_obj = GraphDataObj()
graph_frame = None


def generate_evaluate_tabulate_new_numbers():
    global graph_data_obj

    # Call evaluate_randomness method and record the results
    random_number_list, observed_frequencies, expected_frequencies, chi_square_stat, p_value = erd.evaluate_randomness(return_data=True)
    number_list_length = len(random_number_list)
        
    # Set the text of the labels to descriptions and values
    label_random_numbers.config(text=f"Random Numbers: {random_number_list}")
    label_random_numbers_length.config(text=f"Random Numbers Length: {number_list_length}")
    label_observed_frequencies.config(text=f"Observed Frequencies: {observed_frequencies}")
    label_expected_frequencies.config(text=f"Expected Frequencies: {expected_frequencies}")
    label_chi_square_stat.config(text=f"Chi-Square Statistic: {chi_square_stat}")
    label_p_value.config(text=f"P-Value: {p_value}")

    # Append the results to respective lists and check for min or max changes
    graph_data_obj.number_counts.append(number_list_length)
    graph_data_obj.chi_square_values.append(chi_square_stat)
    graph_data_obj.p_values.append(p_value)
    if chi_square_stat < graph_data_obj.min_chi_square:
        graph_data_obj.min_chi_square = chi_square_stat
    if chi_square_stat > graph_data_obj.max_chi_square:
        graph_data_obj.max_chi_square = chi_square_stat
    if p_value < graph_data_obj.min_p_value:
        graph_data_obj.min_p_value = p_value
    if p_value > graph_data_obj.max_p_value:
        graph_data_obj.max_p_value = p_value
    
    # Update the number of results
    graph_data_obj.number_of_results += 1

    # Generate and draw the graph
    generate_and_draw_graph()


def generate_and_draw_graph():
    global graph_frame
    
    if graph_frame is not None:
        graph_frame.destroy()
    
    # Create a frame for the graph
    graph_frame = tk.Frame(window)
    graph_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    # Create an instance of TkaggGraph in the frame
    data_graph = MultiYAxisTkaggGraph(graph_frame, window, graph_data_obj)

    # Pack the graph to the right side of the frame
    data_graph.pack(fill=tk.BOTH, expand=True)

    # Set the width of the graph frame to occupy only the right half of the window
    graph_frame.config(width=window_x // 2)

    # Update the graph
    data_graph.canvas.draw()
    

# Create a new window
window = tk.Tk()

# Set the window title
window.title("Random Number Graph Display")

# Get the screen width and height
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# initial window geometry dimensions
window_x = 1200
window_y = 530

# Calculate the x and y coordinates for the window to be centered
x = int((screen_width / 2) - (window_x / 2))
y = int((screen_height / 2) - (window_y / 2))

# Set intial the window position and minimum size
# not sure yet how to center on a single screen instead of the whole desktop
window.geometry(f"{window_x}x{window_y}+{x}+{y}")
window.minsize(500, 330)

# Special font for the window's children
window.child_font = ARIAL_FONT

# Create a frame for the controls
controls_frame = tk.Frame(window)
controls_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Create labels to display the numbers
label_random_numbers = tk.Label(controls_frame, text="Random Numbers: (uninitialized value)", font=ARIAL_FONT)
label_random_numbers_length = tk.Label(controls_frame, text="Random Numbers Length: (uninitialized value)", font=ARIAL_FONT)
label_observed_frequencies = tk.Label(controls_frame, text="Observed Frequencies: (uninitialized value)", font=ARIAL_FONT)
label_expected_frequencies = tk.Label(controls_frame, text="Expected Frequencies: (uninitialized value)", font=ARIAL_FONT)
label_chi_square_stat = tk.Label(controls_frame, text="Chi-Square Statistic: (uninitialized value)", font=ARIAL_FONT)
label_p_value = tk.Label(controls_frame, text="P-Value: (uninitialized value)", font=ARIAL_FONT)

# Center the labels in the controls frame
label_random_numbers.pack(anchor=tk.W, padx=10, pady=(50, 5))
label_random_numbers_length.pack(anchor=tk.W, padx=10, pady=5)
label_observed_frequencies.pack(anchor=tk.W, padx=10, pady=5)
label_expected_frequencies.pack(anchor=tk.W, padx=10, pady=5)
label_chi_square_stat.pack(anchor=tk.W, padx=10, pady=5)
label_p_value.pack(anchor=tk.W, padx=10, pady=5)

# Create a button to generate new numbers
button_generate = tk.Button(controls_frame, text="Evaluate New Number List", command=generate_evaluate_tabulate_new_numbers)

# Place the button below the labels
button_generate.pack(pady=10)

# Create a button to close the window
button_close = tk.Button(controls_frame, text="Close", command=window.destroy)

# Place the button below the generate button
button_close.pack(pady=10)

# Set the initial text of the labels to generated random numbers
generate_evaluate_tabulate_new_numbers()

# Function to close the window when Escape key is pressed
def close_window(event):
    if event.keysym == "Escape":
        window.destroy()

# Bind the Escape key press event to the close_window function
window.bind("<Key>", close_window)

# Run the window's event loop
window.mainloop()
