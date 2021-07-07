"""
Класс для работы с базой данных
"""
import math
import numpy as np
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker

from db.supportFunctions import resultproxy_to_dict

from .base import Session, current_session, Base
from .measuredParameters import MeasuredParameters
from .nominalParameters import NominalParameters

class SQLDataBase():

    def __init__(self,name_of_database):
        #name_of_database = 'set_of_blades'
        self.engine = create_engine('sqlite:///' + name_of_database, echo = True)

    def table_create(self):
        #Метод для создания таблиц и базы данных
       Base.metadata.create_all(self.engine)

    def create_session(self):
        #Создание сессии, через которую мапяться объекты
        self.session = sessionmaker(bind=self.engine)()

    def init_repletion_data_base(self):
        # Создание объектов в таблице NominalParameters
        thickness_T_nom =11.1*24.73/25.13
        thickness_B_nom = 24.73 - thickness_T_nom
        type_object = NominalParameters(thickness_nom = 24.73, thickness = 25.13, T_thickness_lower = -0.1,
                                        T_thickness_upper = 0.15, thickness_T = 11.1, thickness_B = 25.13-11.1,
                                        thickness_T_nom = thickness_T_nom, thickness_B_nom = thickness_B_nom,
                                        angle = 30/180*math.pi, T_angle_lower = -1/6/180*math.pi,
                                        T_angle_upper = 1/6/180*math.pi, shelf_width_T = 11.75, shelf_width_half_T = 6,
                                        T_shelf_width_half_T_lower = -0.1, T_shelf_width_half_T_upper = 0.1,
                                        shelf_width_B = 11.5, shelf_width_half_B = 6.8, T_shelf_width_half_B_lower = -0.1,
                                        T_shelf_width_half_B_upper =  0.1, angle_slice = 50/180*math.pi, slice_B = 16.05,
                                        slice_T = 12.7)
        self.session.add(type_object)
        self.session.commit()
    def generated_data_save_data_base(self,delta_thickness,delta_angle):
        # Создание объектов в таблице MeasuredParameters
        #Генерация значений, временно здесь, нужно переносить в отдельную функцию mainHandler-а
        # Добавать в сессию
        for thickness, angle in zip(delta_thickness,delta_angle):
            measured_object = MeasuredParameters(type_id=1, delta_thickness=thickness, delta_angle=angle)
            self.session.add(measured_object)
        self.session.commit()

    def select_all_nominal_params(self):
        # Функция для подачи запроса
        request_str = "SELECT * \
                           FROM \
                           nominal"
        s = self.session.execute(request_str)
        result_of_query = resultproxy_to_dict(s)
        return result_of_query

    def request_delete_of_measured(self):
        #Запрос на удаление всего из таблицы measure
        request_str = "DELETE FROM measure \
                           WHERE type_id = 1"
        s = self.session.execute(request_str)

    def request_of_imbalance(self):
        # Функция для подачи запроса
        request_str = "SELECT passport.passport_id, imbalance, diameter \
                           FROM \
                           passport INNER JOIN characteristic \
                           ON passport.passport_id=characteristic.passport_id \
                           WHERE imbalance<" + str(self.imbalance_tolerance) +" \
                           ORDER BY diameter DESC"
        s2 = self.session.execute(request_str)
        result_of_query = resultproxy_to_dict(s2)
        return result_of_query



    def search_for_id(self, id):
        # Функция для подачи запроса на поиск
        request_str = "SELECT type_name \
                              FROM \
                              type INNER JOIN passport \
                              ON type.type_id=passport.type_id \
                              WHERE passport.passport_id=" + str(id)
        s2 = self.session.execute(request_str)
        result_of_query = resultproxy_to_dict(s2)
        return result_of_query

    def updata_for_id(self, id):
        # Функция для подачи запроса на поиск
        request_str = "SELECT passport.passport_id, type_name, workshop_number, receipt_date, lot_number \
                              FROM \
                              type INNER JOIN passport \
                              ON type.type_id=passport.type_id \
                              INNER JOIN location \
                              ON passport.location_id=location.location_id \
                              WHERE passport.passport_id=" + str(id)
        s2 = self.session.execute(request_str)
        result_of_query = resultproxy_to_dict(s2)
        return result_of_query

    def list_of_parts(self):
        # Вызов списка видов деталей из базы данных
        request_str = "SELECT type_name \
                                      FROM \
                                      type "
        s4 = self.session.execute(request_str)
        result_of_query = resultproxy_to_dict(s4)
        ciphers = []
        for a1 in result_of_query:
            #print(a1)
            ciphers.append(a1['type_name'])
        return ciphers