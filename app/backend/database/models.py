# import
from sqlalchemy import Column, ForeignKey, Identity, func, Integer, String, Boolean, LargeBinary, DateTime, Date, Float, Time
from sqlalchemy.dialects.mysql import DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY

# local import
from app.backend.database.config import BASE


# MODEL CLASSES

# province
class Province(BASE):
    __tablename__ = 'province'
    __table_args__ = {'schema': 'refer'}
    id_record = Column(Integer, Identity(start=10, increment=1, cycle=False), primary_key=True)
    name = Column(String(75), nullable=False)
    log_date = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    # backward relationship
    cantons = relationship('Canton', back_populates='province', cascade='all, delete-orphan')

    # __rep__
    def __repr__(self):
        return f"<Province(id_record={self.id_record}, name={self.name}, log_date={self.log_date})>"


class Canton(BASE):
    __tablename__ = 'canton'
    __table_args__ = {'schema': 'refer'}
    id_record = Column(Integer, Identity(start=20, increment=1, cycle=True), primary_key=True)
    name = Column(String(75), nullable=False)
    id_province = Column(Integer, ForeignKey('refer.province.id_record'), nullable=False)
    log_date = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    # backward relationship
    province = relationship('Province', back_populates='cantons')
    districts = relationship('District', back_populates='canton', cascade='all, delete-orphan')

    # __rep__
    def __repr__(self):
        return (f"<Canton(id_record={self.id_record}, name={self.name}, id_province={self.id_province},"
                f" log_date={self.log_date})>")


class District(BASE):
    __tablename__ = 'district'
    __table_args__ = {'schema': 'refer'}
    id_record = Column(Integer, Identity(start=30, increment=1, cycle=True), primary_key=True)
    name = Column(String(75), nullable=False)
    id_canton = Column(Integer, ForeignKey('refer.canton.id_record'), nullable=False)
    log_date = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    # backward relationship
    canton = relationship('Canton', back_populates='districts')
    addresses = relationship('Address', back_populates='district', cascade='all, delete-orphan')

    # __rep__
    def __repr__(self):
        return (f"<District(id_record={self.id_record}, name={self.name}, id_canton={self.id_canton},"
                f" log_date={self.log_date})>")


class User(BASE):
    __tablename__ = 'user'
    __table_args__ = {'schema': 'entity'}
    id_record = Column(Integer, Identity(start=40, increment=1, cycle=True), primary_key=True)
    identification = Column(String(25), nullable=False, unique=True)
    name = Column(String(75), nullable=False)
    lastname = Column(String(75), nullable=False)
    lastname2 = Column(String(75), nullable=False)
    birthday = Column(Date, nullable=False)
    email = Column(String(120), nullable=False, unique=True)
    phone = Column(String(25), nullable=False, unique=True)
    gender = Column(String(25), nullable=False, server_default='No Indica')
    marital_status = Column(String(25), nullable=False)
    children = Column(Integer, nullable=False, server_default='0')
    password = Column(String(275), nullable=False)
    # do revision to set column to nullable=True
    # temp_password = Column(String(275), nullable=False)
    temp_password = Column(String(275), nullable=True)
    is_temp = Column(Boolean, nullable=False, server_default='TRUE')
    log_date = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    # backward relationship
    addresses = relationship('Address', back_populates='user', cascade='all, delete-orphan')
    user_roles = relationship('User_Role', back_populates='user', cascade='all, delete-orphan')

    # __rep__
    def __repr__(self):
        return (f"<User(id_record={self.id_record}, identification={self.identification}, name={self.name}, "
                f"lastname={self.lastname}, lastname2={self.lastname2}, birthday={self.birthday},"
                f" email={self.email}, phone={self.phone}, gender={self.gender},"
                f" marital_status={self.marital_status}, children={self.children}, log_date={self.log_date})>")


class Address(BASE):
    __tablename__ = 'address'
    __table_args__ = {'schema': 'refer'}
    id_record = Column(Integer, Identity(start=50, increment=1, cycle=True), primary_key=True)
    details = Column(String(255), nullable=False)
    # revision -> drop create and update columns
    # date_create = Column(Date, nullable=False)
    # date_update = Column(Date, nullable=False)
    # revision -> add postal code field
    postal_code = Column(String(15), nullable=False)
    id_district = Column(Integer, ForeignKey('refer.district.id_record'), nullable=False)
    id_user = Column(Integer, ForeignKey('entity.user.id_record'), nullable=False)
    # revision -> add log_date column
    log_date = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    # backward relationship
    user = relationship('User', back_populates='addresses')
    district = relationship('District', back_populates='addresses')

    # __rep__
    def __repr__(self):
        return (f"<Address(id_record={self.id_record}, details={self.details}, log_date={self.log_date}, "
                f"id_district={self.id_district}, id_user={self.id_user})>")


class Schedule(BASE):
    __tablename__ = 'schedule'
    __table_args__ = {'schema': 'refer'}
    id_record = Column(Integer, Identity(start=60, increment=1, cycle=True), primary_key=True)
    name = Column(String(75), nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    hours = Column(Integer, nullable=False, server_default='0')
    date_create = Column(Date, nullable=False)
    date_update = Column(Date, nullable=False)
    # backward relationship
    roles = relationship('Role', back_populates='schedule', cascade='all, delete-orphan')

    # __rep__
    def __repr__(self):
        return (f"<Schedule(id_record={self.id_record}, name={self.name}, start_time={self.start_time}, "
                f"end_time={self.end_time}, hours={self.hours}, date_create={self.date_create}, "
                f"date_update={self.date_update})>")


class Department(BASE):
    __tablename__ = 'department'
    __table_args__ = {'schema': 'refer'}
    id_record = Column(Integer, Identity(start=70, increment=1, cycle=True), primary_key=True)
    name = Column(String(75), nullable=False)
    date_create = Column(Date, nullable=False)
    date_update = Column(Date, nullable=False)
    # backward relationship
    roles = relationship('Role', back_populates='department', cascade='all, delete-orphan')

    # __rep__
    def __repr__(self):
        return (f"<Department(id_record={self.id_record}, name={self.name}, date_create={self.date_create}, "
                f"date_update={self.date_update})>")


class Role(BASE):
    __tablename__ = 'role'
    __table_args__ = {'schema': 'entity'}
    id_record = Column(Integer, Identity(start=80, increment=1, cycle=True), primary_key=True)
    name = Column(String(75), nullable=False)
    type = Column(String(75), nullable=False)
    date_create = Column(Date, nullable=False)
    date_update = Column(Date, nullable=False)
    id_schedule = Column(Integer, ForeignKey('refer.schedule.id_record'), nullable=False)
    id_department = Column(Integer, ForeignKey('refer.department.id_record'), nullable=False)
    # backward relationship
    schedule = relationship('Schedule', back_populates='roles')
    department = relationship('Department', back_populates='roles')
    user_roles = relationship('User_Role', back_populates='role', cascade='all, delete-orphan')

    # __rep__
    def __repr__(self):
        return (f"<Role(id_record={self.id_record}, name={self.name}, type={self.type}, date_create={self.date_create}, "
                f"date_update={self.date_update}, id_schedule={self.id_schedule}, id_department={self.id_department})>")


class User_Role(BASE):
    __tablename__ = 'user_role'
    __table_args__ = {'schema': 'entity'}
    id_record = Column(Integer, Identity(start=90, increment=1, cycle=True), primary_key=True)
    gross_income = Column(DECIMAL(10,2), nullable=False, server_default='0.00')
    status = Column(Boolean, nullable=False, server_default='TRUE')
    hire_date = Column(Date, nullable=False)
    termination_date = Column(Date, nullable=True)
    # revision -> id approver
    approver = Column(Integer, nullable=False)
    # -------------------------------------------
    id_user = Column(Integer, ForeignKey('entity.user.id_record'), nullable=False)
    id_role = Column(Integer, ForeignKey('entity.role.id_record'), nullable=False)
    log_date = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    # backward relationship
    user = relationship('User', back_populates='user_roles')
    role = relationship('Role', back_populates='user_roles')
    payroll_user = relationship('Payroll_User', back_populates='user', cascade='all, delete-orphan')

    # __rep__
    def __repr__(self):
        return (
            f"<User_Role(id_record={self.id_record}, gross_income={self.gross_income}, status={self.status}, "
            f"hire_date={self.hire_date}, termination_date={self.termination_date}, id_user={self.id_user}, "
            f"id_role={self.id_role}, log_date={self.log_date})>")


class Extra_Hour(BASE):
    __tablename__ = 'extra_hour'
    __table_args__ = {'schema': 'serv'}
    id_record = Column(Integer, Identity(start=100, increment=1, cycle=True), primary_key=True)
    hours = Column(Integer, nullable=False, server_default='0')
    date_request = Column(Date, nullable=False)
    is_holiday = Column(Boolean, nullable=False, server_default='FALSE')
    id_subject = Column(Integer, ForeignKey('entity.user_role.id_record'), nullable=False)
    # do revision in here --> drop column foreign key
    # id_approver = Column(Integer, ForeignKey('entity.user_role.id_record'), nullable=False)
    # ----------
    log_date = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    # backward relationship
    subject = relationship('User_Role', foreign_keys=[id_subject])
    # approver = relationship('User_Role', foreign_keys=[id_approver])

    # __rep__
    def __repr__(self):
        return (
            f"<Extra_Hour(id_record={self.id_record}, hours={self.hours}, date_request={self.date_request}, "
            f"is_holiday={self.is_holiday}, id_subject={self.id_subject}, log_date={self.log_date})>")


class Vacation(BASE):
    __tablename__ = 'vacation'
    __table_args__ = {'schema': 'serv'}
    id_record = Column(Integer, Identity(start=110, increment=1, cycle=True), primary_key=True)
    available = Column(Integer, nullable=False, server_default='11')
    used_days = Column(Integer, nullable=False, server_default='0')
    id_subject = Column(Integer, ForeignKey('entity.user_role.id_record'), nullable=False)
    # do revision in here --> drop column foreign key
    # id_approver = Column(Integer, ForeignKey('entity.user_role.id_record'), nullable=False)
    log_date = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    # backward relationship
    subject = relationship('User_Role', foreign_keys=[id_subject])
    # approver = relationship('User_Role', foreign_keys=[id_approver])

    # __rep__
    def __repr__(self):
        return (
            f"<Extra_Hour(id_record={self.id_record}, available={self.available}, used_days={self.used_days}, "
            f"id_subject={self.id_subject}, log_date={self.log_date})>")


class Request_Extra_Hour(BASE):
    __tablename__ = 'request_extra_hour'
    __table_args__ = {'schema': 'serv'}
    id_record = Column(Integer, Identity(start=120, increment=1, cycle=True), primary_key=True)
    hours = Column(Integer, nullable=False, server_default='0')
    date_request = Column(Date, nullable=False)
    type = Column(String(25), nullable=False, server_default='Horas Extra')
    status = Column(String(25), nullable=False, server_default='En Proceso') # En Proceso, Aprobado, Rechazado
    id_subject = Column(Integer, ForeignKey('entity.user_role.id_record'), nullable=False)
    # do revision in here --> drop column foreign key
    # id_approver = Column(Integer, ForeignKey('entity.user_role.id_record'), nullable=False)
    log_date = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    # backward relationship
    subject = relationship('User_Role', foreign_keys=[id_subject])
    # approver = relationship('User_Role', foreign_keys=[id_approver])

    # __rep__
    def __repr__(self):
        return (
            f"<Request_Extra_Hour(id_record={self.id_record}, hours={self.hours}, date_request={self.date_request}, "
            f"type={self.type}, status={self.status}, id_subject={self.id_subject}, log_date={self.log_date})>")


class Request_Vacation(BASE):
    __tablename__ = 'request_vacation'
    __table_args__ = {'schema': 'serv'}
    id_record = Column(Integer, Identity(start=130, increment=1, cycle=True), primary_key=True)
    days = Column(Integer, nullable=False, server_default='0')
    date_start = Column(Date, nullable=False)
    date_return = Column(Date, nullable=False)
    type = Column(String(25), nullable=False, server_default='Vacaciones')
    status = Column(String(25), nullable=False, server_default='En Proceso') # En Proceso, Aprobado, Rechazado
    id_subject = Column(Integer, ForeignKey('entity.user_role.id_record'), nullable=False)
    # do revision in here --> drop column foreign key
    # id_approver = Column(Integer, ForeignKey('entity.user_role.id_record'), nullable=False)
    log_date = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    # backward relationship
    subject = relationship('User_Role', foreign_keys=[id_subject])
    # approver = relationship('User_Role', foreign_keys=[id_approver])

    # __rep__
    def __repr__(self):
        return (
            f"<Request_Vacation(id_record={self.id_record}, days={self.days}, date_start={self.date_start}, "
            f"date_return={self.date_return}, type={self.type}, status={self.status}, id_subject={self.id_subject}, "
            f"log_date={self.log_date})>")


class Bonus(BASE):
    __tablename__ = 'bonus'
    __table_args__ = {'schema': 'serv'}
    id_record = Column(Integer, Identity(start=140, increment=1, cycle=True), primary_key=True)
    total_amount = Column(DECIMAL(10,2), nullable=False, server_default='0.00')
    month_amount = Column(DECIMAL(10,2), nullable=False, server_default='0.00')
    # do revision in here --> add year column
    year = Column(Integer, nullable=False, server_default='1900')
    month = Column(String(25), nullable=False)
    id_subject = Column(Integer, ForeignKey('entity.user_role.id_record'), nullable=False)
    # do revision in here --> drop column foreign key
    # id_approver = Column(Integer, ForeignKey('entity.user_role.id_record'), nullable=False)
    log_date = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    # backward relationship
    subject = relationship('User_Role', foreign_keys=[id_subject])
    # approver = relationship('User_Role', foreign_keys=[id_approver])

    # __rep__
    def __repr__(self):
        return (
            f"<Bonus(id_record={self.id_record}, total_amount={self.total_amount}, month_amount={self.month_amount}, "
            f"month={self.month}, id_subject={self.id_subject}, log_date={self.log_date})>")


class Settlement(BASE):
    __tablename__ = 'settlement'
    __table_args__ = {'schema': 'serv'}
    id_record = Column(Integer, Identity(start=150, increment=1, cycle=True), primary_key=True)
    total_amount = Column(DECIMAL(10,2), nullable=False, server_default='0.00')
    # revision -> create cesantia, vacations, aguinaldo, payment
    cesantia = Column(DECIMAL(10,2), nullable=False, server_default='0.00')
    vacations = Column(DECIMAL(10, 2), nullable=False, server_default='0.00')
    bonus = Column(DECIMAL(10, 2), nullable=False, server_default='0.00')
    payroll = Column(DECIMAL(10, 2), nullable=False, server_default='0.00')
    status = Column(String(25), nullable=False, server_default='En Proceso') # En Proceso, Aprobado
    type = Column(String(25), nullable=False)
    details = Column(String(250), nullable=False)
    id_subject = Column(Integer, ForeignKey('entity.user_role.id_record'), nullable=False)
    # do revision in here --> drop column foreign key
    # id_approver = Column(Integer, ForeignKey('entity.user_role.id_record'), nullable=False)
    log_date = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    # backward relationship
    subject = relationship('User_Role', foreign_keys=[id_subject])
    # approver = relationship('User_Role', foreign_keys=[id_approver])

    # __rep__
    def __repr__(self):
        return (
            f"<Settlement(id_record={self.id_record}, total_amount={self.total_amount}, status={self.status}, "
            f"type={self.type}, details={self.details}, id_subject={self.id_subject}, log_date={self.log_date})>")


class Inability(BASE):
    __tablename__ = 'inability'
    __table_args__ = {'schema': 'serv'}
    id_record = Column(Integer, Identity(start=160, increment=1, cycle=True), primary_key=True)
    date_start = Column(Date, nullable=False)
    date_return = Column(Date, nullable=False)
    # revision -> drop days and type columns
    # days = Column(Integer, nullable=False, server_default='0')
    # type = Column(String(75), nullable=False)
    details = Column(String(275), nullable=False)
    document = Column(LargeBinary, nullable=False)
    doc_number = Column(String(75), nullable=False, unique=True)
    status = Column(String(25), nullable=False, server_default='En Proceso') # En Proceso, Aprobado, Rechazado
    id_subject = Column(Integer, ForeignKey('entity.user_role.id_record'), nullable=False)
    # do revision in here --> drop column foreign key
    # id_approver = Column(Integer, ForeignKey('entity.user_role.id_record'), nullable=False)
    log_date = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    # backward relationship
    subject = relationship('User_Role', foreign_keys=[id_subject])
    # approver = relationship('User_Role', foreign_keys=[id_approver])

    # __rep__
    def __repr__(self):
        return (
            f"<Inability(id_record={self.id_record}, date_start={self.date_start}, date_return={self.date_return}, "
            f"details={self.details}, document={self.document}, "
            f"doc_number={self.doc_number}, status={self.status}, id_subject={self.id_subject}, "
            f"log_date={self.log_date})>")


class Evaluation_Type(BASE):
    __tablename__ = 'evaluation_type'
    __table_args__ = {'schema': 'serv'}
    id_record = Column(Integer, Identity(start=170, increment=1, cycle=True), primary_key=True)
    type = Column(String(75), nullable=False)
    status = Column(Boolean, nullable=False, server_default='FALSE')
    log_date = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    # backward relationship
    questions = relationship('Evaluation_Question', back_populates='type', cascade='all, delete-orphan')

    # __rep__
    def __repr__(self):
        return (
            f"<Evaluation_Type(id_record={self.id_record}, type={self.type}, status={self.status}, "
            f"log_date={self.log_date})>")


class Evaluation_Question(BASE):
    __tablename__ = 'evaluation_question'
    __table_args__ = {'schema': 'serv'}
    id_record = Column(Integer, Identity(start=180, increment=1, cycle=True), primary_key=True)
    question = Column(String(250), nullable=False)
    id_evaluation_type = Column(Integer, ForeignKey('serv.evaluation_type.id_record'), nullable=False)
    log_date = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    # backward relationship
    type = relationship('Evaluation_Type', back_populates='questions')

    # __rep__
    def __repr__(self):
        return (
            f"<Evaluation_Question(id_record={self.id_record}, question={self.question}, "
            f"id_evaluation_type={self.id_evaluation_type}, log_date={self.log_date})>")


class Evaluation(BASE):
    __tablename__ = 'evaluation'
    __table_args__ = {'schema': 'serv'}
    id_record = Column(Integer, Identity(start=190, increment=1, cycle=True), primary_key=True)
    score = Column(ARRAY(Integer), nullable=False)
    average = Column(Float, nullable=False, server_default='0.0')
    details = Column(String(250), nullable=False)
    questions = Column(ARRAY(Integer), nullable=False)
    id_subject = Column(Integer, ForeignKey('entity.user_role.id_record'), nullable=False)
    # revision -> remove id_approver fk
    # id_approver = Column(Integer, ForeignKey('entity.user_role.id_record'), nullable=False)
    log_date = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    # backward relationship
    subject = relationship('User_Role', foreign_keys=[id_subject])

    # __rep__
    def __repr__(self):
        return (
            f"<Evaluation(id_record={self.id_record}, score={self.score}, average={self.average}, details={self.details},"
            f"questions={self.questions}, id_subject={self.id_subject}, log_date={self.log_date})>")


class Deduction(BASE):
    __tablename__ = 'deduction'
    __table_args__ = {'schema': 'serv'}
    id_record = Column(Integer, Identity(start=200, increment=1, cycle=True), primary_key=True)
    name = Column(String(75), nullable=False)
    percentage = Column(Float, nullable=False, server_default='0.0')
    log_date = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    # __rep__
    def __repr__(self):
        return (
            f"<Deduction(id_record={self.id_record}, name={self.name}, percentage={self.percentage}, "
            f"log_date={self.log_date})>")

# revision -> drop Deduction_Payroll
# class Deduction_Payroll(BASE):
#     __tablename__ = 'deduction_payroll'
#     __table_args__ = {'schema': 'serv'}
#     id_record = Column(Integer, Identity(start=210, increment=1, cycle=True), primary_key=True)
#     amount = Column(DECIMAL(10,2), nullable=False, server_default='0.00')
#     id_user = Column(Integer, ForeignKey('entity.user_role.id_record'), nullable=False)
#     id_deduction = Column(Integer, ForeignKey('serv.deduction.id_record'), nullable=False)
#     log_date = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
#     # backward relationship
#     user = relationship('User_Role', back_populates='deduction_payroll')
#     deduction = relationship('Deduction', back_populates='deduction_payroll')
#     payroll = relationship('Payroll', back_populates='deduction_payroll', cascade='all, delete-orphan')
#
#     # __rep__
#     def __repr__(self):
#         return (
#             f"<Deduction_Payroll(id_record={self.id_record}, amount={self.amount}, id_user={self.id_user}, "
#             f"id_deduction={self.id_deduction}, log_date={self.log_date})>")

class Payment_Date(BASE):
    __tablename__ = 'payment_date'
    __table_args__ = {'schema': 'serv'}
    id_record = Column(Integer, Identity(start=220, increment=1, cycle=True), primary_key=True)
    date_payment = Column(Date, nullable=False)
    date_payment2 = Column(Date, nullable=False)
    frecuency = Column(String(25), nullable=False, server_default='Quincenal') # Mensual
    log_date = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    # backward relationship
    payroll = relationship('Payroll_User', back_populates='payment_date', cascade='all, delete-orphan')

    # __rep__
    def __repr__(self):
        return (
            f"<Payment_Date(id_record={self.id_record}, date_payment={self.date_payment}, "
            f"date_payment2={self.date_payment2}, frecuency={self.frecuency}, log_date={self.log_date})>")

# revision -> drop Deduction_Payroll
# class Payroll(BASE):
#     __tablename__ = 'payroll'
#     __table_args__ = {'schema': 'serv'}
#     id_record = Column(Integer, Identity(start=230, increment=1, cycle=True), primary_key=True)
#     net_amount = Column(DECIMAL(10,2), nullable=False, server_default='0.00')
#     details = Column(String(250), nullable=False)
#     id_deduction_payroll = Column(Integer, ForeignKey('serv.deduction_payroll.id_record'), nullable=False)
#     id_payment_date = Column(Integer, ForeignKey('serv.payment_date.id_record'), nullable=False)
#     log_date = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
#     # backward relationship
#     deduction_payroll = relationship('Deduction_Payroll', back_populates='payroll')
#     payment_date = relationship('Payment_Date', back_populates='payroll')
#
#     # __rep__
#     def __repr__(self):
#         return (
#             f"<Payroll(id_record={self.id_record}, net_amount={self.net_amount}, details={self.details}, "
#             f"id_deduction_payroll={self.id_deduction_payroll}, id_payment_date={self.id_payment_date}, "
#             f"log_date={self.log_date})>")


# revision -> new Payroll_User
class Payroll_User(BASE):
    __tablename__ = 'payroll_user'
    __table_args__ = {'schema': 'serv'}
    id_record = Column(Integer, Identity(start=230, increment=1, cycle=True), primary_key=True)
    net_amount = Column(DECIMAL(10, 2), nullable=False, server_default='0.00')
    ccss_ivm = Column(DECIMAL(10, 2), nullable=False, server_default='0.00')
    ccss_eme = Column(DECIMAL(10, 2), nullable=False, server_default='0.00')
    ccss_rop = Column(DECIMAL(10, 2), nullable=False, server_default='0.00')
    renta_tax = Column(DECIMAL(10, 2), nullable=False, server_default='0.00')
    child_support = Column(DECIMAL(10, 2), nullable=False, server_default='0.00')
    debts = Column(DECIMAL(10, 2), nullable=False, server_default='0.00')
    association = Column(DECIMAL(10, 2), nullable=False, server_default='0.00')
    others = Column(DECIMAL(10, 2), nullable=False, server_default='0.00')
    id_user = Column(Integer, ForeignKey('entity.user_role.id_record'), nullable=False)
    id_payment_date = Column(Integer, ForeignKey('serv.payment_date.id_record'), nullable=False)
    log_date = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    # backward relationship
    payment_date = relationship('Payment_Date', back_populates='payroll')
    user = relationship('User_Role', back_populates='payroll_user')


# revision -> create checkin tracker
class Checkin_Tracker(BASE):
    __tablename__ = 'checkin_tracker'
    __table_args__ = {'schema': 'serv'}
    id_record = Column(Integer, Identity(start=330, increment=1, cycle=True), primary_key=True)
    start_hour = Column(Time, nullable=False)
    end_hour = Column(Time, nullable=False)
    hours = Column(Integer, nullable=False, server_default='0')
    status = Column(String(25), nullable=False, server_default='Completado')
    id_subject = Column(Integer, ForeignKey('entity.user_role.id_record'), nullable=False)
    log_date = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    # backward relationship
    subject = relationship('User_Role', foreign_keys=[id_subject])

    # __rep__
    def __repr__(self):
        return (
            f"<Checkin_Tracker(id_record={self.id_record}, start_hour={self.start_hour}, end_hour={self.end_hour}, "
            f"hours={self.hours}, id_subject={self.id_subject}, log_date={self.log_date})>")
