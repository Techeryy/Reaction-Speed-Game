# A simple reaction speed game programmed in python
# using the tkinter graphics library.
# Requirements: time, random, threading, ctypes, tkinter
# Programmed By: Stephen Adams

# Imports
import ctypes as ct
from tkinter import *
import time, random, threading

# Colour Definitions
font, grey, light_grey = '#FFFFFF', '#424549', '#676a6d'

# Global Variable Setup
start_time = None
high_score = 9999

# Fetch Text From Tkinter Element
def getContains(element):
    return str(element.cget('text'))

# Amend Start Time Value
def updateTime(value):
    global start_time
    start_time = value

# Initialise Button & Record Time
def readyButton():
    updateTime(time.time()) 
    button.config(text='Press', bg='green', fg=font)
    display.config(text='Press')

# Start Game Countdown
def startGame():
    updateTime(None)
    for i in range(5, 0, -1):
        display.config(text=f'Starting In: {i}')
        time.sleep(1)
        if getContains(display) == 'Game Failed': return False
    display.config(text='Get Ready...')
    time.sleep(random.uniform(2.0, 5.0))
    readyButton()

# Button Handling
def buttonPress():
    global high_score
    if getContains(button) == 'Play Again':
        if threading.active_count() == 1:
            button.config(text='Wait...', bg=light_grey, fg=font)
            high_score_display.config(text='')
            threading.Thread(target=startGame).start()
    elif start_time is not None:
        elapsed_time = round((time.time() - start_time) * 1000)
        if high_score > elapsed_time:
            high_score_display.config(text='New High Score!')
            high_score = elapsed_time
        display.config(text=f'Pressed In {elapsed_time}ms')
        button.config(text='Play Again', bg='green', fg=font)
    else:
        display.config(text='Game Failed')
        button.config(text='Play Again', bg='red', fg=font)

# Tkinter Window Configuration
window = Tk()
window.geometry('425x425')
window.title('Reaction Speed Game')
window.resizable(False,False)
window.configure(bg=grey)
window.iconphoto(True,PhotoImage(file='assets/favicon.png'))
window.update()
ct.windll.dwmapi.DwmSetWindowAttribute(ct.windll.user32.GetParent(window.winfo_id()), 35, ct.byref(ct.c_int(0x00221F1E)),ct.sizeof(ct.c_int))

# User Interface Element Setup
display = Label(window,font=('terminal',23),bg=grey,fg=font)
display.pack(pady=15)
button = Button(window,text='Wait...',font=('Helvatical bold',20),command=buttonPress,width=14,height=7,bg=light_grey,fg=font,bd=0)
button.pack(expand=True)
high_score_display = Label(window,font=('terminal',23),bg=grey,fg=font)
high_score_display.pack(pady=15)

# Starting Processes
threading.Thread(target=startGame).start()
window.mainloop()