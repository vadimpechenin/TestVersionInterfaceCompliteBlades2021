"""
Класс для прорисовки формы
"""
from forms.mplgraph import MPLgraph

import tkinter as tk

import matplotlib as mpl
mpl.use("TkAgg")  # MUST be invoked prior to importing mpl backends!
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)  # NavigationToolbar2TkAgg was deprecated
import numpy as np
import PySimpleGUI as sg


class MainForm():
    def __init__(self):
        pass

    def show(self):
        figure_w, figure_h = 300, 300
        layout = [
            [sg.Text('base'), sg.InputText('1'), sg.Text('exponent'), sg.InputText('1')],
            [sg.Canvas(size=(figure_w, figure_h), key='-CANVAS-'),
             sg.Canvas(size=(figure_w, figure_h), key='-CANVAS2-')],
            [sg.Submit(), sg.Exit(), sg.Button('Ok')],#, sg.Output
            [sg.Input(), sg.FileBrowse()]
        ]
        window = sg.Window('MVC Test', layout, grab_anywhere=True, finalize=True)
        figure = mpl.figure.Figure(figsize=(5, 4), dpi=100)  # 5, 4
        # Первое окно
        canvas = MPLgraph(figure, window['-CANVAS-'].TKCanvas)
        canvas._tkcanvas.pack(side=tk.BOTTOM, fill=tk.BOTH)  # expand=tk.YES,
        canvas.plot(*self.powerplot(1, 1))
        # Второе окно

        canvas2 = MPLgraph(figure, window['-CANVAS2-'].TKCanvas)
        canvas2._tkcanvas.pack(side=tk.BOTTOM, expand=tk.YES, fill=tk.BOTH)
        canvas2.plot(*self.powerplot(1, 1))

        while True:
            event, values = window.Read()  # event = name of event; values = {0: str, 0: str} of entry values
            if event in (None, 'Exit'):  # If user closed window with X or if user clicked "Exit" event then exit
                break
            if event == 'Submit':
                x, y = self.powerplot(float(values[0]), float(values[1]))
                canvas.clear()
                canvas.plot(x, y)
            if event == 'Ok':
                sg.Print('You entered ', values[0])
        window.close()

    def powerplot(self,base, exponent):
        """
        Calculates data for plotting the function: y = (base * x) ** exponent,
        for x = 0...10.
        Arguments: base and exponent as floats
        Returns: two numpy arrays of x and y coordinates (length 800).
        """

        x = np.linspace(0, 10, 800)
        y = (x * base) ** exponent
        return x, y

    def powerplot2(self,base, exponent):
        """
        Calculates data for plotting the function: y = (base * x) ** exponent,
        for x = 0...10.
        Arguments: base and exponent as floats
        Returns: two numpy arrays of x and y coordinates (length 800).
        """

        x = np.linspace(0, 10, 800)
        y = (x * base) ** exponent
        return x, y