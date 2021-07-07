"""
Описывает базовый класс для тестирования комплектации лопаток
"""

from handlers.loadNominals.loadNominalsCommandHandler import LoadNominalsCommandHandler

class MainHandler():
    def __init__(self):
        self.dict = {}
        self.dict[0] = LoadNominalsCommandHandler()


    def initFunction(self,code_request, parameter):
        result = None
        if code_request in self.dict:
            handler = self.dict[code_request]
            result = handler.execute(parameter)

        return result