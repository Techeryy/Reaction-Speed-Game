# A simple reaction speed game programmed in python
# using the tkinter graphics library.
# Requirements: time, random, threading, ctypes, tkinter
# Programmed By: Stephen Adams

# Imports
import ctypes as ct
from tkinter import *
import time, random, threading

# Global Variable Setup
font_colour, grey, light_grey = '#FFFFFF', '#424549', '#676a6d'
high_score = 9999

# Tkinter Element Helpers
def getContains(element):
    return str(element.cget('text'))

def updateDisplay(text, bg_color=grey):
	display.config(text=text, bg=bg_color)

def updateSubDisplay(text, bg_color=grey):
	sub_display.config(text=text, bg=bg_color)

def updateButton(text, bg_color=light_grey, command=None):
	button.config(text=text, bg=bg_color, command=command)

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
	global high_score
	elapsed_time = round((time.time() - start_time) * 1000)
	if high_score > elapsed_time:
		high_score = elapsed_time
		updateSubDisplay('New High Score!')
	updateDisplay(f'Pressed In {elapsed_time}ms'), updateButton('Play Again', 'green', startGameThread)

def gameFailed():
	updateDisplay('Game Failed'), updateButton('Play Again', 'red', startGameThread)

# Tkinter Setup
window = Tk()
window.geometry('425x425')
window.title('Reaction Speed Game')
window.resizable(False, False)
window.configure(bg=grey)
window.iconphoto(True,PhotoImage(file='assets/favicon.png'))
window.update()
ct.windll.dwmapi.DwmSetWindowAttribute(ct.windll.user32.GetParent(window.winfo_id()), 35, ct.byref(ct.c_int(0x00221F1E)),ct.sizeof(ct.c_int))

# UI Elements
display = Label(window, font=('terminal', 23), fg=font_colour, bg=grey)
display.pack(pady=15)
button = Button(window, font=('Helvatical bold', 20), fg=font_colour, bg=light_grey, width=14, height=7, bd=0)
button.pack(expand=True)
sub_display = Label(window, font=('terminal', 23), fg=font_colour, bg=grey)
sub_display.pack(pady=15)

# Starting Processes
startGameThread()
window.mainloop()