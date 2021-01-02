#A simple Tkinter app for Stock Price Visualization

from tkinter import *
from tkinter import font  as tkfont
import tkinter.messagebox
import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from datetime import date
import numpy as np
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

class MainPage(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.minsize(800, 600)
        self.resizable(0, 0)

        menu = Menu(self)
        self.config(menu = menu)

        newMenu = Menu(menu, tearoff = False)
        menu.add_cascade(label = "New", menu = newMenu)
        newMenu.add_command(label="Stock Visualization", command = self.show_visual_frame)
        newMenu.add_separator()
        newMenu.add_command(label="Exit", command = self.show_start_frame)

        aboutMenu = Menu(menu, tearoff = False)
        menu.add_cascade(label = "About", menu = aboutMenu)
        aboutMenu.add_command(label="Help", command = self.help)
        aboutMenu.add_command(label = "About Developer", command = self.about)

        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.frames["StartPage"] = StartPage(parent=container, controller=self)
        self.frames["VisualPage"] = VisualPage(parent=container, controller=self)

        self.frames["StartPage"].grid(row=0, column=0, sticky="nsew")
        self.frames["VisualPage"].grid(row=0, column=0, sticky="nsew")

        self.show_start_frame()

    def about(self):
        message = "This software is developed by Pulkit Gupta.\nContact me at guptapulkit48@gmail.com."
        tkinter.messagebox.showinfo('About Developer', message)

    def help(self):
        message = "To visualize stocks, select: New ==> Stock Visualization."
        tkinter.messagebox.showinfo('Help', message)

    def show_start_frame(self):
        '''Show a frame for the given page name'''
        frame = self.frames["StartPage"]
        frame.tkraise()

    def show_visual_frame(self):
        '''Show a frame for the given page name'''
        frame = self.frames["VisualPage"]
        frame.tkraise()

class StartPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="Welcome to the Home Page\n", font = 40)
        label.pack(side="top", fill="x", pady=10)

        self.infoFrame = Frame(self)
        self.infoFrame.pack(side = TOP)

        leftLabel = Label(self.infoFrame, text="To visualize stocks, select:\nNew ==> Stock Visualization", font = 25)
        leftLabel.pack()

class VisualPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="Stock Price Visualization", font = 40)
        label.pack(side="top", fill="x", pady=10)

        self.tickerSymbol = ''
        self.start = ''
        self.end = ''
        self.interval = ''
        self.type = ''

        #Frame: Invisible Rectangle(Container)
        self.leftFrame = Frame(self)
        self.leftFrame.pack(side = LEFT)
        self.rightFrame = Frame(self)
        self.rightFrame.pack(side = RIGHT)

        self.figure = plt.Figure(figsize=(5,4), dpi=100)
        self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, self.rightFrame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=RIGHT, fill=BOTH)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.rightFrame)
        self.figure.autofmt_xdate()
        self.toolbar.update()
        self.figure.suptitle("Stock Price Visualization")
        self.canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

        #Input Fields
        label_ticker = Label(self.leftFrame, text = "Ticker Symbol")
        label_start = Label(self.leftFrame, text = "Start Date")
        label_end = Label(self.leftFrame, text = "End Date")
        label_interval = Label(self.leftFrame, text = "Interval")
        label_type = Label(self.leftFrame, text = "Type")
        label_instruction = Label(self.leftFrame, text = "*Use YYYY-MM-DD format for date")

        self.entry_ticker = Entry(self.leftFrame)
        self.entry_start = Entry(self.leftFrame)
        self.entry_end = Entry(self.leftFrame)
        self.entry_interval = Entry(self.leftFrame)
        submit = Button(self.leftFrame, text="Visualize Graph", command = self.validate_and_plot)

        self.intervalVar = StringVar(self.leftFrame)
        intervalchoices = ['1d', '5d', '1wk', '1mo']
        self.intervalVar.set('1d') # set the default option
        self.intervalPopupMenu = OptionMenu(self.leftFrame, self.intervalVar, *intervalchoices)

        self.typeVar = StringVar(self.leftFrame)
        typechoices = ['Open', 'Close']
        self.typeVar.set('Open') # set the default option
        self.typePopupMenu = OptionMenu(self.leftFrame, self.typeVar, *typechoices)

        label_ticker.grid(row = 0, sticky = E)
        label_start.grid(row = 1, sticky = E)
        label_end.grid(row = 2, sticky = E)
        label_interval.grid(row = 3, sticky = E)
        label_type.grid(row = 4, sticky = E)

        self.entry_ticker.grid(row = 0, column = 1)
        self.entry_start.grid(row = 1, column = 1)
        self.entry_end.grid(row = 2, column = 1)
        self.intervalPopupMenu.grid(row = 3, column = 1)
        self.typePopupMenu.grid(row = 4, column = 1)
        submit.grid(row = 5, columnspan = 2)
        label_instruction.grid(row = 6, columnspan = 2)

    def validate_and_plot(self):
        self.tickerSymbol = self.entry_ticker.get()
        self.start = self.entry_start.get()
        self.end = self.entry_end.get()
        self.interval = self.intervalVar.get()
        self.type = self.typeVar.get()

        if self.tickerSymbol=='' or self.interval=='' or self.start=='' or self.end=='':
            tkinter.messagebox.showinfo('Error', 'Enter Complete Data')
            return

        self.plot_visualization()

    def plot_visualization(self):
        tickerData = yf.Ticker(self.tickerSymbol)
        tickerDf = tickerData.history(interval = self.interval,  start = self.start, end = self.end)

        self.figure.gca().clear()
        self.figure.gca().plot(tickerDf[self.type])
        self.figure.autofmt_xdate()
        self.figure.canvas.draw()
        return

def main():
    mainpage = MainPage()
    mainpage.mainloop()

if __name__=="__main__":
    main()
