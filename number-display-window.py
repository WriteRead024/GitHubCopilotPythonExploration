# started 2/8/2024
# Rich W.
# with
# GitHub Copilot


import tkinter as tk

# Create a new window
window = tk.Tk()

# Set the window title
window.title("Number Display")

# Set the window size
window.geometry("400x200")

# Get the screen width and height
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Calculate the x and y coordinates for the window to be centered
x = int((screen_width / 2) - (400 / 2))
y = int((screen_height / 2) - (200 / 2))

# Set the window position
window.geometry(f"400x200+{x}+{y}")

# Create a label to display the numbers
label = tk.Label(window, text="1, 2, 3, 4, 5")

# Center the label in the window
label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Create a button to close the window
button = tk.Button(window, text="Close", command=window.destroy)

# Place the button below the label
button.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

# Function to close the window when Escape key is pressed
def close_window(event):
    if event.keysym == "Escape":
        window.destroy()

# Bind the Escape key press event to the close_window function
window.bind("<Key>", close_window)

# Run the window's event loop
window.mainloop()
