# A simple reaction speed game programmed in python
# using the tkinter graphics library.
# Requirements: time, json, random, threading, ctypes, tkinter, datetime
# Programmed By: Stephen Adams

# Imports
import ctypes as ct
from tkinter import *
from datetime import datetime
import time, json, random, threading

# Global Variable Setup
font_colour, grey, light_grey, dark_grey = '#FFFFFF', '#424549', '#676a6d', '#3B3D3E'

# Tkinter Element Helpers
def getContains(element):
    return str(element.cget('text'))

def updateDisplay(text, bg_color=grey):
    display.config(text=text, bg=bg_color)

def updateSubDisplay(text, bg_color=grey):
    sub_display.config(text=text, bg=bg_color)

def updateButton(text, bg_color=light_grey, command=None):
    button.config(text=text, bg=bg_color, command=command)

# Score Storage
def storeTime(time):
    scores_list = getTimes()
    scores_list.append({'date_time': datetime.now().strftime('%d/%m/%Y %H:%M:%S'), 'time': time})
    with open('scores.json', 'w') as file:
        json.dump(scores_list, file, indent=4)

def getTimes():
    try:
        with open('scores.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError: return []

def getHighScore(lowest=9999):
    for item in getTimes():
        if item['time'] < lowest: lowest = item['time']
    return lowest

# Historic Scores Widget
def createWidget():
    history_canvas = Canvas(window, bg=dark_grey, highlightthickness=0)
    history_canvas.place(relx=0.5, rely=0.5, anchor='center')
    navbar = Frame(history_canvas, bg=dark_grey)
    navbar.pack(side='top', fill='x')
    Label(navbar, text="Historic Scores", fg=font_colour, bg=dark_grey).pack(side='left')
    Button(navbar, text="X", command=lambda: history_canvas.destroy(), fg=font_colour, bg=dark_grey, bd=0).pack(side='right')
    if getTimes() == []:
        Label(history_canvas, text='No Data Available', fg=font_colour, bg=dark_grey).pack()
    for entry in getTimes():
        Label(history_canvas, text=f"{entry['date_time']}, Time: {entry['time']} ms", fg=font_colour, bg=dark_grey).pack()

# Core Functions
def startGame():
    global start_time
    start_time = None
    updateSubDisplay(''), updateButton(text='Wait...', command=gameFailed)
    for i in range(5, 0, -1):
        updateDisplay(f'Starting In: {i}')
        time.sleep(1)
        if getContains(display) == 'Game Failed': return False
    updateDisplay('Get Ready...')
    time.sleep(random.uniform(2.0, 5.0))
    start_time = time.time()
    updateDisplay('Press'), updateButton('Press', 'green', gameSuccess)

def startGameThread():
    if threading.active_count() == 1:
        threading.Thread(target=startGame).start()

def gameSuccess():
    elapsed_time = round((time.time() - start_time) * 1000)
    if getHighScore() > elapsed_time:
        updateSubDisplay('New High Score!')
    storeTime(elapsed_time)
    updateDisplay(f'Pressed In {elapsed_time}ms'), updateButton('Play Again', 'green', startGameThread)

def gameFailed():
    updateDisplay('Game Failed'), updateButton('Play Again', 'red', startGameThread)

# Tkinter Window Configuration
window = Tk()
window.geometry('425x410')
window.title('Reaction Speed Game')
window.resizable(False, False)
window.configure(bg=grey)
window.iconphoto(True,PhotoImage(file='assets/favicon.png'))
window.update()
ct.windll.dwmapi.DwmSetWindowAttribute(ct.windll.user32.GetParent(window.winfo_id()), 35, ct.byref(ct.c_int(0x00221F1E)),ct.sizeof(ct.c_int))

# User Interface Element Setup
display = Label(window, font=('terminal', 23), fg=font_colour, bg=grey)
display.pack(pady=(15,0))
sub_display = Label(window,font=('Helvatical bold', 16), fg=font_colour, bg=grey)
sub_display.pack(pady=4)
button = Button(window, font=('Helvatical bold', 20), fg=font_colour, bg=light_grey, width=14, height=7, bd=0)
button.pack(pady=5)
Button(window, text='★ Scores', command=createWidget, font=('Helvatical bold', 15), fg=font_colour, bg=grey, bd=0).pack(pady=10)

# Starting Processes
startGameThread()
window.mainloop()