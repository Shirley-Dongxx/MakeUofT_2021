#
#  oscilloscope.py
#  MakeUofT_2021
#
#  Created by Xuening on 2021-02-16.
#  Copyright © 2021 Xuening. All rights reserved.
#

import matplotlib

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style

import tkinter as tk
from tkinter import ttk

import tkinter as tk
from tkinter import *
from tkinter import ttk
import serial
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style

LARGE_FONT = ("Verdana", 12)
style.use("ggplot")

f = Figure(figsize=(5, 5), dpi=100)
a = f.add_subplot(111)
a.grid()

global x,y
x = 1
y = 1

global xList, yList
xList = []
yList = []

global connected, ser, data
connected = 0
data = []

def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False


def connect():
    global connected, ser
    ser = serial.Serial('/dev/cu.usbmodem141101', 9800, timeout=1)
    connected = 1
    print("hi")

def close():
    global connected, ser
    ser.close()
    connected = 0
    print("bye")

def show():
  print("Connected: ", connected)

def animate(i):

    global data
    if (connected == 0):
        return

    b = ser.readline()  # read a byte string
    string_n = b.decode()  # decode byte string into Unicode
    string = string_n.rstrip()  # remove \n and \r
    print("curr: ", string)
    if (isfloat(string)):
        flt = float(string)
    elif (string == "" and len(data)>=1):
        flt = data[-1]
    else:
        flt = 0
    data.append(flt)
    a.clear()
    a.plot(range(len(data)), data, marker='o', color='blue')
    a.set_ylabel("Voltage")
    a.set_xlabel("Time")
    a.grid(True)
    time.sleep(0.2)

class oscilloscope(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self)
        tk.Tk.wm_title(self, "Oscilloscope")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageOne, PageTwo, PageThree):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.grid(row=0, column=1, padx=10, pady=5)

        button = ttk.Button(self, text="Visit Page 1",
                            command=lambda: controller.show_frame(PageOne))
        button.grid(row=1, column=1, padx=10, pady=5)

        button2 = ttk.Button(self, text="Visit Page 2",
                             command=lambda: controller.show_frame(PageTwo))
        button2.grid(row=1, column=2, padx=10, pady=5)

        button3 = ttk.Button(self, text="Start Plotting",
                             command=lambda: controller.show_frame(PageThree))
        button3.grid(row=2, column=0, padx=10, pady=5)

        button_4 = tk.Button(self, text="Connect", width=10, command=connect)
        button_4.grid(row=2, column=1, padx=10, pady=5)
        button_5 = tk.Button(self, text="Close", width=10, command=close)
        button_5.grid(row=2, column=2, padx=10, pady=5)
        button_6 = tk.Button(self, text="Show Connection", width=10, command=show)
        button_6.grid(row=2, column=3, padx=10, pady=5)

class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page One!!!", font=LARGE_FONT)
        label.grid(row=0, column=1, padx=10, pady=5)

        button1 = ttk.Button(self, text="Back to Home",
                             command=lambda: controller.show_frame(StartPage))
        button1.grid(row=1, column=0, padx=10, pady=5)

        button2 = ttk.Button(self, text="Page Two",
                             command=lambda: controller.show_frame(PageTwo))
        button2.grid(row=1, column=1, padx=10, pady=5)


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page Two!!!", font=LARGE_FONT)
        label.grid(row=0, column=0, padx=10, pady=5)

        button1 = ttk.Button(self, text="Back to Home",
                             command=lambda: controller.show_frame(StartPage))
        button1.grid(row=1, column=0, padx=10, pady=5)

        button2 = ttk.Button(self, text="Page One",
                             command=lambda: controller.show_frame(PageOne))
        button2.grid(row=1, column=1, padx=10, pady=5)


class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        def clear():
            a.clear()
            a.grid(True)
            global data
            data = []

        label = tk.Label(self, text="Live Plotting!", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                             command=lambda: controller.show_frame(StartPage))
        button1.pack()

        global data
        data = []
        clear()

        button_c = tk.Button(self, text="Clear Plotting", width=10, command=clear)
        button_c.pack()

        button_s = tk.Button(self, text="Stop Plotting", width=10, command=close)
        button_s.pack()

        button_r = tk.Button(self, text="Resume Plotting", width=10, command=connect)
        button_r.pack()

        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)



app = oscilloscope()
ani = animation.FuncAnimation(f, animate, interval=200)
app.mainloop()