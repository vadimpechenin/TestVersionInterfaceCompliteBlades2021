"""
Класс для прорисовки формы
"""
from handlers.loadNominals.loadNominalsCommandHandlerParameter import LoadNominalsCommandHandlerParameter
from handlers.generateMeasure.generateMeasureCommandHandlerParameter import GenerateMeasureCommandHandlerParameter
from handlers.loadMeasure.loadMeasureCommandHandlerParameter import LoadMeasureCommandHandlerParameter

from forms.mplgraph import MPLgraph
import os
import tkinter as tk

import matplotlib as mpl
mpl.use("TkAgg")  # MUST be invoked prior to importing mpl backends!
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)  # NavigationToolbar2TkAgg was deprecated
import numpy as np
import PySimpleGUI as sg


class MainForm():
    def __init__(self,handler):
        self.handler = handler

    def show(self):
        figure_w, figure_h = 300, 300
        layout = [
            [sg.Text('base'), sg.InputText('84'), sg.Text('exponent'), sg.InputText('1')],
            [sg.Canvas(size=(figure_w, figure_h), key='-CANVAS-'),
             sg.Canvas(size=(figure_w, figure_h), key='-CANVAS2-')],
            [sg.Multiline(size=(50, 10), key = '_output_'), sg.Multiline(size=(50, 10), key = '_output2_')],
            [sg.Submit(), sg.Exit(), sg.Button('Загрузить номинальные значения'), sg.Button('Загрузить измерения'), sg.Button('Генерация измерений')],#, sg.Output
            [sg.Input(), sg.FileBrowse()]
        ]
        window = sg.Window('MVC Test', layout, grab_anywhere=True, finalize=True)
        figure = mpl.figure.Figure(figsize=(5, 5), dpi=100)  # 5, 4
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

            if event == 'Загрузить номинальные значения':
                window.FindElement('_output_').Update('')
                # window['_output_'].TKOut.output.config(wrap='word')  # set Output element word wrapping
                file1 = os.path.basename(values[2])
                parameters = LoadNominalsCommandHandlerParameter(file1, 'nominal')
                window['_output_'].print('Load from database: ' + file1)
                result_request = self.handler.initFunction(0, parameters)
                window['_output_'].print('Parameters: ' + str(result_request))

            if event == 'Генерация измерений':
                #sg.Print('You entered ', values[0])
                file1 = os.path.basename(values[2])
                number_of_blades = int(values[0])
                T_thickness_lower = -0.1  # Допуск на толщину, нижняя граница
                T_thickness_upper = 0.15  # Допуск на толщину, верхняя граница
                T_angle_lower = -1/6/180*np.pi  # Допуск на угол, нижняя граница
                T_angle_upper = 1/6/180*np.pi  # Допуск на угол, верхняя граница
                delta_thickness = np.random.normal((T_thickness_upper+T_thickness_lower)/2,
                                                   (T_thickness_upper-T_thickness_lower)/6, size = number_of_blades)
                delta_angle = np.random.normal((T_angle_upper + T_angle_lower)/2,
                                                   (T_angle_upper - T_angle_lower)/6, size = number_of_blades)
                parameters = GenerateMeasureCommandHandlerParameter(file1,'measure',delta_thickness,delta_angle)
                result_request = self.handler.initFunction(1, parameters)
                window.FindElement('_output2_').Update('')
                window['_output2_']. print('You entered ', result_request)

            if event == 'Загрузить измерения':
                window.FindElement('_output_').Update('')
                #window['_output_'].TKOut.output.config(wrap='word')  # set Output element word wrapping
                file1 = os.path.basename(values[2])
                parameters = LoadNominalsCommandHandlerParameter(file1,'measure')
                window['_output2_'].print('Load from database: ' + file1)
                result_request = self.handler.initFunction(2, parameters)
                window['_output2_'].print('Parameters: ' + str(result_request))
                number_of_blades =result_request.pop()

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