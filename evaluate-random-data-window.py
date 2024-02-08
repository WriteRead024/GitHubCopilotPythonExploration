# started 2/8/2024
# Rich W.
# using
# GitHub Copilot


import tkinter as tk
import importlib
erd = importlib.import_module("evaluate-random-data")

def evaluate_new_numbers():
    random_number_list, observed_frequencies, expected_frequencies, chi_square_stat, p_value = erd.evaluate_randomness(return_data=True)
    
    # Set the text of the labels to descriptions and values
    label_random_numbers.config(text=f"Random Numbers: {random_number_list}")
    label_random_numbers_length.config(text=f"Random Numbers Length: {len(random_number_list)}")
    label_observed_frequencies.config(text=f"Observed Frequencies: {observed_frequencies}")
    label_expected_frequencies.config(text=f"Expected Frequencies: {expected_frequencies}")
    label_chi_square_stat.config(text=f"Chi-Square Statistic: {chi_square_stat}")
    label_p_value.config(text=f"P-Value: {p_value}")

# Create a new window
window = tk.Tk()

# Set the window title
window.title("Number Display")

# Get the screen width and height
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Calculate the x and y coordinates for the window to be centered
x = int((screen_width / 2) - (600 / 2))
y = int((screen_height / 2) - (400 / 2))

# Set the window position
window.geometry(f"600x400+{x}+{y}")

# Create labels to display the numbers
label_random_numbers = tk.Label(window, text="Random Numbers: (uninitialized value)", font=("Arial", 12))
label_random_numbers_length = tk.Label(window, text="Random Numbers Length: (uninitialized value)", font=("Arial", 12))
label_observed_frequencies = tk.Label(window, text="Observed Frequencies: (uninitialized value)", font=("Arial", 12))
label_expected_frequencies = tk.Label(window, text="Expected Frequencies: (uninitialized value)", font=("Arial", 12))
label_chi_square_stat = tk.Label(window, text="Chi-Square Statistic: (uninitialized value)", font=("Arial", 12))
label_p_value = tk.Label(window, text="P-Value: (uninitialized value)", font=("Arial", 12))

# Set the initial text of the labels to generated random numbers
evaluate_new_numbers()

# Center the labels in the window
label_random_numbers.place(relx=0.5, rely=0.25, anchor=tk.CENTER)
label_random_numbers_length.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
label_observed_frequencies.place(relx=0.5, rely=0.35, anchor=tk.CENTER)
label_expected_frequencies.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
label_chi_square_stat.place(relx=0.5, rely=0.45, anchor=tk.CENTER)
label_p_value.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Create a button to generate new numbers
button_generate = tk.Button(window, text="Evaluate New Number List", command=evaluate_new_numbers)

# Place the button below the labels
button_generate.place(relx=0.5, rely=0.65, anchor=tk.CENTER)

# Create a button to close the window
button_close = tk.Button(window, text="Close", command=window.destroy)

# Place the button below the generate button
button_close.place(relx=0.5, rely=0.75, anchor=tk.CENTER)

# Function to close the window when Escape key is pressed
def close_window(event):
    if event.keysym == "Escape":
        window.destroy()

# Bind the Escape key press event to the close_window function
window.bind("<Key>", close_window)

# Run the window's event loop
window.mainloop()
