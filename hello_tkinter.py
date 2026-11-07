
import tkinter as tk


# Create main window
window = tk.Tk()

window.title("Hello Tkinter")
window.geometry("400x250")


# Create heading
heading = tk.Label(
    window,
    text="Hello World!",
    font=("Arial", 24)
)

heading.pack(pady=30)


# Button click function
def button_clicked():

    heading.config(
        text="Welcome to Tkinter!"
    )


# Create button
button = tk.Button(
    window,
    text="Click Me",
    font=("Arial", 14),
    command=button_clicked
)

button.pack(pady=20)


# Run application
window.mainloop()
