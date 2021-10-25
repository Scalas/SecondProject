from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from controller.db_manager import Base


class DayCalOwner(Base):
    __tablename__ = 'DAYCAL_OWNER'
    name = Column(String, primary_key=True)

    def __init__(self, name):
        self.name = name


class DayCalValues(Base):
    __tablename__ = 'DAYCAL_VALUES'
    datetime = Column(String, primary_key=True)
    owner_name = Column(String, primary_key=True)
    kd_total = Column(Integer)
    kd_fare = Column(Integer)
    kd_drop = Column(Integer)
    match_fee5 = Column(Integer)
    owner_fare = Column(Integer)
    owner_drop = Column(Integer)
    listing_fee4 = Column(Integer)
    kd_pre = Column(Integer)

    def __init__(self, datetime, owner):
        self.datetime = datetime
        self.owner = owner
