# started 2/8/2024
# Rich W.
# with
# GitHub Copilot


import tkinter as tk
import importlib
grtd = importlib.import_module("generate-random-test-data")

def generate_new_numbers():
    number = grtd.generate_random_number()
    numberlist = grtd.generate_random_number_list(number)
    label.config(text=", ".join(str(num) for num in numberlist))

# Create a new window
window = tk.Tk()

# Set the window title
window.title("Random Numbers Window")

# Get the screen width and height
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Calculate the x and y coordinates for the window to be centered
x = int((screen_width / 2) - (400 / 2))
y = int((screen_height / 2) - (200 / 2))

# Set the window position
window.geometry(f"400x200+{x}+{y}")

# Create a label to display the numbers
label = tk.Label(window, text="init value", font=("Arial", 24))

# Set the initial text of the label to generated random numbers
generate_new_numbers()

# Center the label in the window
label.place(relx=0.5, rely=0.35, anchor=tk.CENTER)

# Create a button to generate new numbers
button_generate = tk.Button(window, text="Generate", command=generate_new_numbers)

# Place the button below the label
button_generate.place(relx=0.5, rely=0.55, anchor=tk.CENTER)

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
