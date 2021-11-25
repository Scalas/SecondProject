from sqlalchemy import Column, Integer, String, Date
from controller.db_manager import Base


# 화주 모델
class DayCalOwner(Base):
    __tablename__ = 'daycal_owner'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    owner_type = Column(Integer, nullable=False)

    # type 0: 냉동 / 1: 생물
    def __init__(self, name, owner_type):
        self.name = name
        self.owner_type = owner_type

    def get(self, idx):
        if idx == 0:
            return self.id
        elif idx == 1:
            return self.name
        elif idx == 2:
            return self.owner_type

    def set(self, idx, val):
        if idx == 0:
            self.id = val
        elif idx == 1:
            self.name = val
        elif idx == 2:
            self.owner_type = val

    def to_list(self):
        return [self.id, self.name, self.owner_type]


# 화주별 일일정산 데이터 모델
class DayCalOwnerValues(Base):
    __tablename__ = 'daycal_owner_values'
    date = Column(Date, primary_key=True)
    owner_id = Column(Integer, primary_key=True)
    owner_name = Column(String, nullable=False)
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

    def __init__(self, date, owner_id, owner_name):
        self.date = date
        self.owner_id = owner_id
        self.owner_name = owner_name
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

    def get(self, idx):
        if idx == 0:
            return self.kd_total
        elif idx == 1:
            return self.kd_fare
        elif idx == 2:
            return self.kd_drop
        elif idx == 3:
            return self.kd_fee4
        elif idx == 4:
            return self.after_deduction
        elif idx == 5:
            return self.match_fee5
        elif idx == 6:
            return self.owner_fare
        elif idx == 7:
            return self.owner_drop
        elif idx == 8:
            return self.listing_fee4
        elif idx == 9:
            return self.kd_pre
        elif idx == 10:
            return self.deduction_total
        elif idx == 11:
            return self.total_include_pre

    def set(self, idx, val):
        if idx == 0:
            self.kd_total = val
        elif idx == 1:
            self.kd_fare = val
        elif idx == 2:
            self.kd_drop = val
        elif idx == 3:
            self.kd_fee4 = val
        elif idx == 4:
            self.after_deduction = val
        elif idx == 5:
            self.match_fee5 = val
        elif idx == 6:
            self.owner_fare = val
        elif idx == 7:
            self.owner_drop = val
        elif idx == 8:
            self.listing_fee4 = val
        elif idx == 9:
            self.kd_pre = val
        elif idx == 10:
            self.deduction_total = val
        elif idx == 11:
            self.total_include_pre = val

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

    def get(self, idx):
        if idx == 0:
            return self.office_deposit
        elif idx == 1:
            return self.kd_deposit
        elif idx == 2:
            return self.direct_exp
        elif idx == 3:
            return self.our_auc
        elif idx == 4:
            return self.kd_buy

    def set(self, idx, val):
        if idx == 0:
            self.office_deposit = val
        elif idx == 1:
            self.kd_deposit = val
        elif idx == 2:
            self.direct_exp = val
        elif idx == 3:
            self.our_auc = val
        elif idx == 4:
            self.kd_buy = val

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

    def get(self, idx):
        if idx == 0:
            return self.kd_total
        elif idx == 1:
            return self.kd_fare
        elif idx == 2:
            return self.kd_drop
        elif idx == 3:
            return self.kd_fee4
        elif idx == 4:
            return self.after_deduction
        elif idx == 5:
            return self.match_fee5
        elif idx == 6:
            return self.owner_fare
        elif idx == 7:
            return self.owner_drop
        elif idx == 8:
            return self.listing_fee4
        elif idx == 9:
            return self.auc_check
        elif idx == 10:
            return self.auc_diff
        elif idx == 11:
            return self.match_fee5_final
        elif idx == 12:
            return self.auc_profit

    def set(self, idx, val):
        if idx == 0:
            self.kd_total = val
        elif idx == 1:
            self.kd_fare = val
        elif idx == 2:
            self.kd_drop = val
        elif idx == 3:
            self.kd_fee4 = val
        elif idx == 4:
            self.after_deduction = val
        elif idx == 5:
            self.match_fee5 = val
        elif idx == 6:
            self.owner_fare = val
        elif idx == 7:
            self.owner_drop = val
        elif idx == 8:
            self.listing_fee4 = val
        elif idx == 9:
            self.auc_check = val
        elif idx == 10:
            self.auc_diff = val
        elif idx == 11:
            self.match_fee5_final = val
        elif idx == 12:
            self.auc_profit = val

    def to_list(self):
        return [self.kd_total, self.kd_fare, self.kd_drop, self.kd_fee4, self.after_deduction,
                self.match_fee5, self.owner_fare, self.owner_drop, self.listing_fee4, self.auc_check,
                self.auc_diff, self.match_fee5_final, self.auc_profit]
