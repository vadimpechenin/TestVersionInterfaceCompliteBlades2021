from handlers.baseCommandHandler import BaseCommandHandler

from .pointsBackParameter import PointsBackParameter
from .pointsTroughParameter import PointsThroughParameter

import numpy as np

class CalculationNominalscommandHandler(BaseCommandHandler):
    def __init__(self):
        pass

    def execute(self, parameters):
        # Вычисление необходимых номинальных значений
        # Вычисление всех (4) задающих точек и поиск площади превышения номинальной стыковки
        # Со стороны спинки
        pointsBackParams = self.function_poisk_points_back_2D(parameters)
        # Со стороны корыта
        pointsTroughParams = self.function_poisk_points_trough_2D(parameters)

        #%Наборы точек для смещения и разворота

        ciphers = None
        return ciphers

    def function_poisk_points_back_2D(self, parameters):
        # Поиск всей геометрии на спинке для решения задачи
        Point0 = np.zeros(2)
        Point0[0], Point0[1] = 0, parameters.thickness_B / np.cos(parameters.angle)
        Point0nom = np.zeros(2)
        Point0nom[0], Point0nom[1] = 0, parameters.thickness_B_nom / np.cos(parameters.angle)

        # Уравнение типа y = kx + b
        b1 = parameters.thickness_B / np.cos(parameters.angle)
        k1 = -np.tan(parameters.angle)
        b1_nom = parameters.thickness_B_nom / np.cos(parameters.angle)
        k1_nom = -np.tan(parameters.angle)
        k0B = -np.tan(parameters.angle)
        b0B = parameters.thickness_B_nom / np.cos(parameters.angle)
        Point_1_B = np.zeros(2)
        Point_1_B[0], Point_1_B[1]= parameters.shelf_width_B - parameters.shelf_width_half_B, \
                                    k1*(parameters.shelf_width_B - parameters.shelf_width_half_B) + b1

        Point_2d_B = np.zeros(2)
        Point_2d_B[0], Point_2d_B[1] = -parameters.shelf_width_half_B, k1 * (-parameters.shelf_width_half_B) + b1

        Point0slice = np.zeros(2)
        Point0slice[0], Point0slice[1]  = -parameters.slice_B / np.cos(parameters.angle_slice), 0
        b2 = parameters.slice_B / np.cos(parameters.angle_slice)
        k2 = np.tan(parameters.angle_slice)
        # Точки пересечения скоса и линий лопаток
        # С вертикальной
        Point_3_B = np.zeros(2)
        Point_3_B[0], Point_3_B[1] = -parameters.shelf_width_half_B, k2 * (-parameters.shelf_width_half_B) + b2
        Point_2_B = np.zeros(2)
        Point_2_B[0], Point_2_B[1] = (b2 - b1) / (k1 - k2), k1 * ((b2 - b1) / (k1 - k2)) + b1
        b4 = Point_3_B[1] - k1 * Point_3_B[0]
        Point_4_B = np.zeros(2)
        Point_4_B[0], Point_4_B[1] = (parameters.shelf_width_B - parameters.shelf_width_half_B),\
                                     k1 * (parameters.shelf_width_B - parameters.shelf_width_half_B) + b4

        # Точки пересечения с фигурой
        Point_01_B = np.zeros(2)
        Point_01_B[0], Point_01_B[1]= parameters.shelf_width_B - parameters.shelf_width_half_B, \
                                    k0B * (parameters.shelf_width_B - parameters.shelf_width_half_B) + b0B
        Point_02_B = np.zeros(2)
        Point_02_B[0],  Point_02_B[1] = (b2 - b0B) / (k0B - k2), \
                                         k0B * ((b2 - b0B) / (k0B - k2)) + b0B
        pointsBackParams = PointsBackParameter(k0B,b0B,Point_1_B,Point_2_B,Point_3_B,Point_4_B, Point_01_B, Point_02_B)
        return pointsBackParams

    def function_poisk_points_trough_2D(self, parameters):

        pointsTroughParams = PointsThroughParameter()
        pass