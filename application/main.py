"""
Тестовая программа для запуска приложения
по комплектации лопаток компрессора
"""

from handlers.mainHandler import MainHandler

from forms.mainForm import MainForm

app = MainForm()
app.show()