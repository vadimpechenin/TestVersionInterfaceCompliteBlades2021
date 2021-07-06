"""
Сущность из БД - номинальные значения параметров
"""

import sqlalchemy as sa

from .base import Base
from sqlalchemy.orm import relationship

class NominalParameters(Base):
    __tablename__ = 'nominal'
    type_id = sa.Column(sa.Integer(), primary_key=True)
    thickness_nom = sa.Column(sa.Float) #Номинальное значение толщины без натяга
    thickness = sa.Column(sa.Float) #Номинальное значение толщины, обеспечивающее натяг
    thickness_nom = sa.Column(sa.Float)
    thickness_nom = sa.Column(sa.Float)
    thickness_nom = sa.Column(sa.Float)
    thickness_nom = sa.Column(sa.Float)
    thickness_nom = sa.Column(sa.Float)
    thickness_nom = sa.Column(sa.Float)

    measure = relationship('measure', backref='nominal', uselist=False)  # one to one

    def __repr__(self):
        # для печати строки и отладки
        return '<Characteristics[type_id="{}", location_id="{}", receipt_date="{}"]>'.format(
            self.type_id, self.location_id, self.characteristics_id, self.receipt_date)