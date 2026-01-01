import tkinter as tk
from tkinter import messagebox
import random

# Create the main window
root = tk.Tk()
root.title("Love 💖")
root.geometry("500x600")
root.config(bg="#fff0f5")  # light pink background

# Heart animation canvas
canvas = tk.Canvas(root, width=500, height=300, bg="#fff0f5", highlightthickness=0)
canvas.pack()

hearts = []

# Generate heart shapes at random x positions
def create_heart():
    x = random.randint(20, 480)
    heart = canvas.create_text(x, 0, text="❤️", font=("Arial", 20))
    hearts.append(heart)
    root.after(300, create_heart)

# Animate hearts falling
def animate_hearts():
    for heart in hearts:
        canvas.move(heart, 0, 5)
        coords = canvas.coords(heart)
        if coords and coords[1] > 300:
            canvas.delete(heart)
            hearts.remove(heart)
    root.after(50, animate_hearts)

# Love meter logic
love_level = 0

def increase_love():
    global love_level
    if love_level < 100:
        love_level += 10
        meter_label.config(text=f"Love Meter: {love_level}% 💗")
    if love_level >= 100:
        messagebox.showinfo("Overflowing Love", "My love for you is overflowing! 💘")

# Random sweet messages
sweet_messages = [
    "You're my sunshine ☀️",
    "I love you to the moon and back 🌙",
    "You complete me 💞",
    "You're my favorite notification 🥰",
    "My heart is yours 💖",
    "You're the reason I smile 😘"
]

def show_random_message():
    msg = random.choice(sweet_messages)
    messagebox.showinfo("A Little Love Note", msg)

# UI Elements
title = tk.Label(root, text="Hi Byang! 💕", bg="#fff0f5", fg="#ff4d88", font=("Comic Sans MS", 24, "bold"))
title.pack(pady=10)

meter_label = tk.Label(root, text="Love Meter: 0% 💗", bg="#fff0f5", fg="#d63384", font=("Comic Sans MS", 16))
meter_label.pack(pady=10)

love_button = tk.Button(root, text="Love Me 💘", command=increase_love, bg="#ff85a2", fg="white", font=("Comic Sans MS", 14, "bold"))
love_button.pack(pady=10)

surprise_button = tk.Button(root, text="Surprise Me 🎁", command=show_random_message, bg="#ff66b2", fg="white", font=("Comic Sans MS", 14))
surprise_button.pack(pady=10)

# Start animations
create_heart()
animate_hearts()

# Run the app
root.mainloop()
