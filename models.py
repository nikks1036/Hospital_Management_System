from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import hashlib

db = SQLAlchemy()

class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    updationDate = db.Column(db.String(255), nullable=True)

    def check_password(self, pwd):
        # Support raw MD5 and plaintext comparison for legacy compatibility
        md5_pwd = hashlib.md5(pwd.encode('utf-8')).hexdigest()
        return self.password == pwd or self.password == md5_pwd


class DoctorSpecialization(db.Model):
    __tablename__ = 'doctorspecilization'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    specilization = db.Column(db.String(255), nullable=True)
    creationDate = db.Column(db.DateTime, default=datetime.utcnow)
    updationDate = db.Column(db.DateTime, onupdate=datetime.utcnow)


class Doctor(db.Model):
    __tablename__ = 'doctors'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    specilization = db.Column(db.String(255), nullable=True)
    doctorName = db.Column(db.String(255), nullable=True)
    address = db.Column(db.Text, nullable=True)
    docFees = db.Column(db.String(255), nullable=True)
    contactno = db.Column(db.BigInteger, nullable=True)
    docEmail = db.Column(db.String(255), nullable=True)
    password = db.Column(db.String(255), nullable=True)
    creationDate = db.Column(db.DateTime, default=datetime.utcnow)
    updationDate = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def check_password(self, pwd):
        md5_pwd = hashlib.md5(pwd.encode('utf-8')).hexdigest()
        return self.password == pwd or self.password == md5_pwd

    def set_password(self, pwd):
        self.password = hashlib.md5(pwd.encode('utf-8')).hexdigest()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fullName = db.Column(db.String(255), nullable=True)
    address = db.Column(db.Text, nullable=True)
    city = db.Column(db.String(255), nullable=True)
    gender = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(255), nullable=True)
    password = db.Column(db.String(255), nullable=True)
    regDate = db.Column(db.DateTime, default=datetime.utcnow)
    updationDate = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def check_password(self, pwd):
        md5_pwd = hashlib.md5(pwd.encode('utf-8')).hexdigest()
        return self.password == pwd or self.password == md5_pwd

    def set_password(self, pwd):
        self.password = hashlib.md5(pwd.encode('utf-8')).hexdigest()


class Appointment(db.Model):
    __tablename__ = 'appointment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    doctorSpecialization = db.Column(db.String(255), nullable=True)
    doctorId = db.Column(db.Integer, nullable=True)
    userId = db.Column(db.Integer, nullable=True)
    consultancyFees = db.Column(db.Integer, nullable=True)
    appointmentDate = db.Column(db.String(255), nullable=True)
    appointmentTime = db.Column(db.String(255), nullable=True)
    postingDate = db.Column(db.DateTime, default=datetime.utcnow)
    userStatus = db.Column(db.Integer, default=1)   # 1 = active, 0 = canceled by user
    doctorStatus = db.Column(db.Integer, default=1) # 1 = active, 0 = canceled by doctor
    updationDate = db.Column(db.DateTime, onupdate=datetime.utcnow)


class TblPatient(db.Model):
    __tablename__ = 'tblpatient'
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Docid = db.Column(db.Integer, nullable=True)
    PatientName = db.Column(db.String(200), nullable=True)
    PatientContno = db.Column(db.BigInteger, nullable=True)
    PatientEmail = db.Column(db.String(200), nullable=True)
    PatientGender = db.Column(db.String(50), nullable=True)
    PatientAdd = db.Column(db.Text, nullable=True)
    PatientAge = db.Column(db.Integer, nullable=True)
    PatientMedhis = db.Column(db.Text, nullable=True)
    CreationDate = db.Column(db.DateTime, default=datetime.utcnow)
    UpdationDate = db.Column(db.DateTime, onupdate=datetime.utcnow)


class TblMedicalHistory(db.Model):
    __tablename__ = 'tblmedicalhistory'
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    PatientID = db.Column(db.Integer, nullable=True)
    BloodPressure = db.Column(db.String(200), nullable=True)
    BloodSugar = db.Column(db.String(200), nullable=True)
    Weight = db.Column(db.String(100), nullable=True)
    Temperature = db.Column(db.String(200), nullable=True)
    MedicalPres = db.Column(db.Text, nullable=True)
    CreationDate = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class TblBilling(db.Model):
    __tablename__ = 'tblbilling'
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    BillNumber = db.Column(db.String(30), nullable=False)
    PatientID = db.Column(db.Integer, nullable=False)
    DoctorID = db.Column(db.Integer, nullable=False)
    ConsultationFee = db.Column(db.Numeric(10, 2), default=0.00)
    MedicineCharge = db.Column(db.Numeric(10, 2), default=0.00)
    LabCharge = db.Column(db.Numeric(10, 2), default=0.00)
    RoomCharge = db.Column(db.Numeric(10, 2), default=0.00)
    OtherCharge = db.Column(db.Numeric(10, 2), default=0.00)
    Discount = db.Column(db.Numeric(10, 2), default=0.00)
    GST = db.Column(db.Numeric(10, 2), default=0.00)
    TotalAmount = db.Column(db.Numeric(10, 2), nullable=False)
    PaymentMode = db.Column(db.String(50), nullable=True)
    PaymentStatus = db.Column(db.String(20), default='Pending')
    BillDate = db.Column(db.DateTime, default=datetime.utcnow)


class TblBloodReport(db.Model):
    __tablename__ = 'tblbloodreport'
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    PatientID = db.Column(db.Integer, nullable=False)
    DoctorID = db.Column(db.Integer, nullable=False)
    Hemoglobin = db.Column(db.String(20), nullable=True)
    WBC = db.Column(db.String(20), nullable=True)
    RBC = db.Column(db.String(20), nullable=True)
    Platelets = db.Column(db.String(20), nullable=True)
    BloodGroup = db.Column(db.String(10), nullable=True)
    BloodSugar = db.Column(db.String(20), nullable=True)
    Cholesterol = db.Column(db.String(20), nullable=True)
    DoctorRemark = db.Column(db.Text, nullable=True)
    ReportFile = db.Column(db.String(255), nullable=True)
    ReportPDF = db.Column(db.String(255), nullable=True)
    ReportDate = db.Column(db.String(50), nullable=True)
    CreationDate = db.Column(db.DateTime, default=datetime.utcnow)


class TblContactUs(db.Model):
    __tablename__ = 'tblcontactus'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fullname = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(255), nullable=True)
    contactno = db.Column(db.BigInteger, nullable=True)
    message = db.Column(db.Text, nullable=True)
    PostingDate = db.Column(db.DateTime, default=datetime.utcnow)
    AdminRemark = db.Column(db.Text, nullable=True)
    LastupdationDate = db.Column(db.DateTime, onupdate=datetime.utcnow)
    IsRead = db.Column(db.Integer, nullable=True)


class TblPage(db.Model):
    __tablename__ = 'tblpage'
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    PageType = db.Column(db.String(200), nullable=True)
    PageTitle = db.Column(db.String(200), nullable=True)
    PageDescription = db.Column(db.Text, nullable=True)
    Email = db.Column(db.String(120), nullable=True)
    MobileNumber = db.Column(db.BigInteger, nullable=True)
    UpdationDate = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    OpenningTime = db.Column(db.String(255), nullable=True)


class DoctorLog(db.Model):
    __tablename__ = 'doctorslog'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.Integer, nullable=True)
    username = db.Column(db.String(255), nullable=True)
    userip = db.Column(db.String(255), nullable=True)
    loginTime = db.Column(db.DateTime, default=datetime.utcnow)
    logout = db.Column(db.String(255), nullable=True)
    status = db.Column(db.Integer, nullable=True)


class UserLog(db.Model):
    __tablename__ = 'userlog'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.Integer, nullable=True)
    username = db.Column(db.String(255), nullable=True)
    userip = db.Column(db.String(255), nullable=True)
    loginTime = db.Column(db.DateTime, default=datetime.utcnow)
    logout = db.Column(db.String(255), nullable=True)
    status = db.Column(db.Integer, nullable=True)
