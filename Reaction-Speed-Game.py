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
times = {}

# Fetch Text From Tkinter Element
def getContains(element):
    return str(element.cget('text'))

# Subroutines
def countdown(display, times):
    for i in reversed(range(5)):
        if getContains(display) == 'Game Failed':
            return
        display.config(text=f'Starting In: {i+1}')
        time.sleep(1)
    if not getContains(display) == 'Game Failed':
        display.config(text='Get Ready...')
        time.sleep(random.randint(200, 500)/100)
    if not getContains(display) == 'Game Failed':
        times['start_time'] = time.time()
        button.config(text='Press', bg='green', fg=font)
        display.config(text='Press')

def buttonPress(display, times):
    if getContains(button) == 'Play Again':
        times.clear()
        display.config(text='')
        button.config(text='Wait...', bg=light_grey, fg=font)
        threading.Thread(target=countdown, args=(display, times)).start()
    elif 'start_time' in times:
        times['end_time'] = time.time()
        elapsed_time = times['end_time'] - times['start_time']
        display.config(text=f'Pressed In {elapsed_time:.2f}s')
        button.config(text='Play Again', bg='green', fg=font)
    else:
        display.config(text='Game Failed')
        button.config(text='Play Again', bg='red', fg=font)

# Tkinter Window Configuration
window = Tk()
window.geometry('400x400')
window.title('Reaction Speed Game')
window.resizable(False,False)
window.configure(bg=grey)
window.iconphoto(True,PhotoImage(file='assets/favicon.png'))
window.update()
ct.windll.dwmapi.DwmSetWindowAttribute(ct.windll.user32.GetParent(window.winfo_id()), 35, ct.byref(ct.c_int(0x00221F1E)),ct.sizeof(ct.c_int))

# User Interface Element Setup
display = Label(window,font=('terminal',23),bg=grey,fg=font)
display.pack(pady=15)
button = Button(window,text='Wait...',font=('Helvatical bold',20),command=lambda:buttonPress(display, times),width=14,height=7,bg=light_grey,fg=font,bd=0)
button.pack(expand=True)

# Starting Processes
threading.Thread(target=countdown, args=(display, times)).start()
window.mainloop()