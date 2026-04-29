import tkinter as tk
from tkinter import scrolledtext, messagebox
import pygame
import os
import random
import datetime
import sys

#Initialize Pygame mixer (if you haven't already)
pygame.mixer.init()
#Path to your sounds folder (relative to executable)
sounds_folder = "silence_breaker_DELTA_sounds"

#Check for sounds folder:
if not os.path.exists(sounds_folder):
    os.makedirs(sounds_folder)
    tk.messagebox.showinfo(
        title="Sounds Folder Created",
        message=(
            f"THIS NOT AN ERROR!\n\n"
            "Folder \""+sounds_folder+"\" has been created!\n\n"
            "Keep this folder and the .exe file together.\n\n"
            "NEXT:\nAdd sounds to the \""+sounds_folder+"\" folder, and run the .exe again."
        )
    )
    sys.exit(0)

#Create the list and load all sounds
filenames = []
sounds = []
buttons = []
minute_fields = []
active_minute_values = []
seconds_left_values = []
sound_checkboxes = []

#Load sounds from "sounds" folder
for filename in os.listdir(sounds_folder):
    if filename.lower().endswith(('.wav', '.ogg', '.mp3')):  # Add more extensions if needed
        sounds.append(pygame.mixer.Sound(sounds_folder + "/" + filename))
        filenames.append(filename)
print(f"Total sounds loaded: {len(sounds)}")

if (len(sounds) < 1):
    tk.messagebox.showinfo(
        title="ERROR: No sounds!",
        message=(
            f"WARNING:\n\n"
            "The folder \""+sounds_folder+"\" contains no sound files.\n\n"
            "This folder is located in the same place as the .exe that you just launched.\n\n"
            "Add sounds to the \""+sounds_folder+"\" folder, then run the .exe again."
        )
    )
    sys.exit(0)

#Set up GUI
root = tk.Tk()
root.title("Silence Breaker")
root.geometry("1200x900")

top_frame = tk.Frame(root)
top_frame.pack(fill='x', padx=10, pady=6)
#Clock (Lets you see ticks, but doesn't count counting them.)
clock_states = ["|", "/", "—", "\\"]
clock_state_index = 0
#clock_frame = tk.Frame(root)
#clock_frame.pack(fill='x', padx=10, pady=6)
clock_label = tk.Label(top_frame, text="Running: " + clock_states[clock_state_index],
                       font=("Courier", 12), width=16, anchor='w')
clock_label.pack(fill='x')

def test_sound(i):
    sounds[i].stop()
    sounds[i].play()
    log_text.config(state='normal')
    log_text.insert(tk.END, "🔧 TESTED " +filenames[i]+ " " +datetime.datetime.now().strftime("%m-%d at %I:%M:%S %p.\n"))
    log_text.see(tk.END)
    log_text.config(state='disabled')

#Create one hbox per sound
for i in range(len(sounds)):
    hbox = tk.Frame(root)
    hbox.pack(fill='x', padx=10, pady=6)
    #Checkbox
    sound_checkbox = tk.IntVar(value=1)
    sound_checkboxes.append(sound_checkbox)
    check = tk.Checkbutton(hbox, variable=sound_checkbox,
                           font=("Arial", 12), width=4)
    check.pack(side='left', padx=(0, 8))
    #Test buttons
    test_button = tk.Button(hbox, text="Test", command=lambda i=i: test_sound(i),
                            font=("Arial", 12), width=8)
    test_button.pack(side='left', padx=(0, 10))
    buttons.append(test_button)
    #Sound Labels
    sound_label = tk.Label(hbox, text=filenames[i], font=("Arial", 12), width=16, anchor='w')
    sound_label.pack(side='left', padx=5)
    #Minute fields
    minutes_entry = tk.Entry(hbox, width=5, font=("Arial", 12), justify='center')
    minutes_entry.insert(0, "60")
    minutes_entry.pack(side='left', padx=5)
    minute_fields.append(minutes_entry)
    #Entry Labels
    sound_label = tk.Label(hbox, text="Max wait (minutes)", font=("Arial", 10),
                           width=21, anchor='w')
    sound_label.pack(side='left', padx=5)
    #Math
    active_minute_values.append(60)
    seconds_left_values.append(random.randint(1, 3600))
    print("Sound " +filenames[i]+ " wait time chosen: " +str(seconds_left_values[i])+ " seconds.")
    #NOTE: 3600=seconds in 1 hour, the default average wait.

log_label = tk.Label(root, text="\n\nLog:",
                       font=("Courier", 12), width=16, anchor='w')
log_label.pack(fill='x')
#Log window
log_text = scrolledtext.ScrolledText(root, height=6, width=120, font=("Courier", 11),
                                     wrap=tk.WORD, state='disabled')
log_text.pack(fill='x', padx=10, pady=10)

def tick_timers():
    global clock_state_index
    global clock_label
    global sounds
    global buttons
    global minute_fields
    global active_minute_values
    global seconds_left_values
    global active_minute_values
    global log_text
    #global filenames
    #visual tick
    clock_state_index = (clock_state_index+1) % 4
    clock_label.config(text="Running: " + clock_states[clock_state_index])
    #Do upkeep and play sounds
    for i in range(len(sounds)):
        #Check entries for valid ints.
        try:
            val = int(minute_fields[i].get().strip())
        except:
            print("WRONG")
            minute_fields[i].delete(0, tk.END)
            minute_fields[i].insert(0, "1")
        #Check for entry changes and update seconds left if needed.
        if(int(active_minute_values[i]) != int(minute_fields[i].get())):
            active_minute_values[i] = max(1, int(minute_fields[i].get()))
            minute_fields[i].delete(0, tk.END)      # Clear existing text
            minute_fields[i].insert(0, active_minute_values[i])
            new_seconds_max = active_minute_values[i]*60
            seconds_left_values[i] = random.randint(1, int(new_seconds_max))
            print("New timer for sound " +filenames[i]+ ": " +str(seconds_left_values[i])+
                  " seconds.")
        #Tick the value, and play sound if needed.
        if(not sound_checkboxes[i].get()):
            break #disarmed, so don't tick this sound.
        seconds_left_values[i] = (seconds_left_values[i] - 1)
        if (seconds_left_values[i] < 1):
            sounds[i].play()
            new_seconds_max = (active_minute_values[i]*60)
            seconds_left_values[i] = random.randint(1, int(new_seconds_max))
            print("New timer for sound " +filenames[i]+ ": " +str(seconds_left_values[i])+
                  " seconds.")
            #Log sound event
            log_text.config(state='normal')
            log_text.insert(tk.END, "✅ Played " +filenames[i]+ " " +datetime.datetime.now().strftime("%m-%d at %I:%M:%S %p.\n"))
            log_text.see(tk.END)
            log_text.config(state='disabled')
    #Run again in 1000ms (1 second)
    root.after(1000, tick_timers)

tick_timers()
root.mainloop()
