from sqlalchemy import Column, Integer, String, DateTime
from controller.db_manager import Base


# 화주 모델
class DayCalOwner(Base):
    __tablename__ = 'daycal_owner'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)

    def __init__(self, name):
        self.name = name


# 화주별 일일정산 데이터 모델
class DayCalOwnerValues(Base):
    __tablename__ = 'daycal_owner_values'
    datetime = Column(DateTime, primary_key=True)
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


# 일일정산서에 입력될 기타 데이터 모델
class DayCalOtherValues(Base):
    __tablename__ = 'daycal_other_values'
    datetime = Column(DateTime, primary_key=True)
    office_deposit = Column(Integer)
    kd_deposit = Column(Integer)
    direct_exp = Column(Integer)
    our_auc = Column(Integer)
    kd_buy = Column(Integer)

    def __init__(self, datetime):
        self.datetime = datetime
