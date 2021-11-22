from sqlalchemy import Column, Integer, String, Date
from controller.db_manager import Base


# 화주 모델
class DayCalOwner(Base):
    __tablename__ = 'daycal_owner'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)

    def __init__(self, name):
        self.name = name

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def set_id(self, owner_id):
        self.id = owner_id

    def set_name(self, name):
        self.name = name


# 화주별 일일정산 데이터 모델
class DayCalOwnerValues(Base):
    __tablename__ = 'daycal_owner_values'
    date = Column(Date, primary_key=True)
    owner_id = Column(Integer, primary_key=True)
    kd_total = Column(Integer, nullable=False)
    kd_fare = Column(Integer, nullable=False)
    kd_drop = Column(Integer, nullable=False)
    kd_fee4 = Column(Integer, nullable=False)
    after_deduction = Column(Integer, nullable=False)
    match_fee5 = Column(Integer, nullable=False)
    owner_fare = Column(Integer, nullable=False)
    owner_drop = Column(Integer, nullable=False)
    listing_fee4 = Column(Integer, nullable=False)
    kd_pre = Column(Integer, nullable=False)
    deduction_total = Column(Integer, nullable=False)
    total_include_pre = Column(Integer, nullable=False)

    def __init__(self, date, owner_id):
        self.date = date
        self.owner_id = owner_id
        self.kd_total = 0
        self.kd_fare = 0
        self.kd_drop = 0
        self.kd_fee4 = 0
        self.after_deduction = 0
        self.match_fee5 = 0
        self.owner_fare = 0
        self.owner_drop = 0
        self.listing_fee4 = 0
        self.kd_pre = 0
        self.deduction_total = 0
        self.total_include_pre = 0

    def to_list(self):
        return [self.kd_total, self.kd_fare, self.kd_drop, self.kd_fee4, self.after_deduction,
                self.match_fee5, self.owner_fare, self.owner_drop, self.listing_fee4, self.kd_pre,
                self.deduction_total, self.total_include_pre]


# 일일정산서 기타 데이터 모델
class DayCalOtherValues(Base):
    __tablename__ = 'daycal_other_values'
    date = Column(Date, primary_key=True)
    office_deposit = Column(Integer)
    kd_deposit = Column(Integer)
    direct_exp = Column(Integer)
    our_auc = Column(Integer)
    kd_buy = Column(Integer)

    def __init__(self, date):
        self.date = date
        self.office_deposit = 0
        self.kd_deposit = 0
        self.direct_exp = 0
        self.our_auc = 0
        self.kd_buy = 0

    def to_list(self):
        return [self.office_deposit, self.kd_deposit, self.direct_exp, self.our_auc, self.kd_buy]


# 일일정산서 결과 모델
class DayCalResult(Base):
    __tablename__ = 'daycal_result'
    date = Column(Date, primary_key=True)
    kd_total = Column(Integer, nullable=False)
    kd_fare = Column(Integer, nullable=False)
    kd_drop = Column(Integer, nullable=False)
    kd_fee4 = Column(Integer, nullable=False)
    after_deduction = Column(Integer, nullable=False)
    match_fee5 = Column(Integer, nullable=False)
    owner_fare = Column(Integer, nullable=False)
    owner_drop = Column(Integer, nullable=False)
    listing_fee4 = Column(Integer, nullable=False)
    auc_check = Column(Integer, nullable=False)
    auc_diff = Column(Integer, nullable=False)
    match_fee5_final = Column(Integer, nullable=False)
    auc_profit = Column(Integer, nullable=False)

    def __init__(self, date):
        self.date = date
        self.kd_total = 0
        self.kd_fare = 0
        self.kd_drop = 0
        self.kd_fee4 = 0
        self.after_deduction = 0
        self.match_fee5 = 0
        self.owner_fare = 0
        self.owner_drop = 0
        self.listing_fee4 = 0
        self.auc_check = 0
        self.auc_diff = 0
        self.match_fee5_final = 0
        self.auc_profit = 0

    def to_list(self):
        return [self.kd_total, self.kd_fare, self.kd_drop, self.kd_fee4, self.after_deduction,
                self.match_fee5, self.owner_fare, self.owner_drop, self.listing_fee4, self.auc_check,
                self.auc_diff, self.match_fee5_final, self.auc_profit]
