import tkinter as tk
from tkinter import *
from tkinter.ttk import Combobox
from PIL import Image, ImageTk
import pyttsx3
import os

# ------------------- GLOBAL IMAGE HANDLERS -------------------
# Needs to be global or attached to a persistent object (like root) 
# to prevent garbage collection if used outside a function.
play_icon = None 
title_logo_img = None
# ------------------- MAIN WINDOW -------------------
root = Tk()
root.title("Text To Speech Converter")

try:
    # Use PIL to load the image first (handles more formats)
    # This is for the window icon
    pil_image = Image.open("C:/Users/user/Desktop/TextToSpeech/play.png")
    logo_image = ImageTk.PhotoImage(pil_image)
    root.iconphoto(False, logo_image)
except Exception as e:
    print(f"Error loading window icon image: {e}")
    # Continue without setting an icon if image can't be loaded

root.geometry("1000x580+200+80")
root.resizable(True, True)
root.configure(bg="#588157")

# ------------------- TTS ENGINE -------------------
tts = pyttsx3.init()

def speaknow():
    text = text_box.get(1.0, END).strip()
    gender = gender_box.get()
    speed = speed_box.get()
    voices = tts.getProperty('voices')

    if not text:
        return  # do nothing if empty

    # Set gender voice
    if gender == 'Male':
        # Safely set to the first voice as a default male
        tts.setProperty('voice', voices[0].id if len(voices) > 0 else '')
    else:
        # Safely set to the second voice (assuming female) or fallback to first
        tts.setProperty('voice', voices[1].id if len(voices) > 1 else voices[0].id if len(voices) > 0 else '')

    # Set speed
    if speed == 'Fast':
        tts.setProperty('rate', 250)
    elif speed == 'Medium':
        tts.setProperty('rate', 150)
    else:
        tts.setProperty('rate', 60)

    # Speak
    tts.say(text)
    tts.runAndWait()

# ------------------- UI -------------------
upper_frame = Frame(root, bg="#C3EA4F", width=1200, height=130)
upper_frame.place(x=0, y=0)

# 1. Add Image in front of "Text To Speech Converter"
try:
    # Load and resize image for the title logo
    pil_title_logo = Image.open("C:/Users/user/Desktop/TextToSpeech/text.png").resize((70, 70))
    # Assigning to the global variable initialized at the top. No 'global' keyword needed.
    title_logo_img = ImageTk.PhotoImage(pil_title_logo)
    
    # Place the image as a Label
    logo_label = Label(upper_frame, image=title_logo_img, bg="#C3EA4F")
    logo_label.place(x=160, y=30) # Adjusted position to be left of the text
except Exception as e:
    print(f"Error loading title logo image: {e}")
    # Image will not be displayed, continue with text only

# Update position for the text to accommodate the logo
upper_text = Label(
    upper_frame,
    text="Text To Speech Converter",
    font="TimesNewRoman 40 bold",
    bg="#C3EA4F",
    fg="black"
)
# Place the text next to the logo (if loaded, x=250 was the original)
upper_text.place(x=250, y=35) 

# Text box
text_box = Text(root, font="calibri 20", bg="white", relief=GROOVE, wrap=WORD, bd=0)
text_box.place(x=30, y=150, width=940, height=180)

# Gender selection
gender_box = Combobox(root, values=['Male', 'Female'], font="Robote 12", state='readonly', width=12)
gender_box.place(x=340, y=400)
gender_box.set('Male')

# Speed selection
speed_box = Combobox(root, values=['Fast', 'Medium', 'Slow'], font="Robote 12", state='readonly', width=12)
speed_box.place(x=540, y=400)
speed_box.set('Medium')

# Labels
Label(root, text="Select Voice", font="TimesNewRoman 15 bold", bg="#588157", fg="white").place(x=340, y=370)
Label(root, text="Select Speed", font="TimesNewRoman 15 bold", bg="#588157", fg="white").place(x=540, y=370)

# 2. Play Button Fix
try:
    # Load and resize the play button icon (using 'play.png' as a placeholder)
    pil_play_icon = Image.open("C:/Users/user/Desktop/TextToSpeech/play.png").resize((30, 30))
    # Fix: Removed 'global play_icon' here. The variable is already global via module-level initialization.
    play_icon = ImageTk.PhotoImage(pil_play_icon) 
    
    # Create the button with the image and text
    play_btn = Button(
        root, 
        text="Play", 
        compound=LEFT, # Places the image to the left of the text
        image=play_icon,
        bg="#C3EA4F", # Changed background color for better visibility
        fg="black",
        width=120, 
        height=40, # Explicitly set height for better control
        font="arial 15 bold", # Increased font size
        borderwidth=0, 
        relief=RIDGE, # Added a subtle border style
        command=speaknow
    )
except Exception as e:
    print(f"Error loading play button image: {e}")
    # Fallback if image not found (uses text only, no image)
    play_btn = Button(
        root, 
        text=" Play", 
        bg="#C3EA4F", 
        fg="black",
        width=12,
        height=2,
        font="arial 15 bold", 
        borderwidth=0, 
        relief=RIDGE,
        command=speaknow
    )

play_btn.place(x=435, y=450) # The button should now be visible and clickable

# ------------------- START APP -------------------
root.mainloop()
