import os
from app import create_app
from models import db, Admin, DoctorSpecialization, Doctor, User, TblPage, TblPatient, TblBilling, TblBloodReport, TblMedicalHistory, Appointment, TblContactUs
import hashlib

app = create_app()

def init_database():
    with app.app_context():
        # Create upload folder if not exists
        upload_dir = app.config['UPLOAD_FOLDER']
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir, exist_ok=True)

        db.create_all()
        print("Database tables created successfully.")

        # Seed Admin if empty
        if not Admin.query.first():
            admin = Admin(
                username='admin',
                password='Test@12345',
                updationDate='04-03-2024 11:42:05 AM'
            )
            db.session.add(admin)
            print("Default admin created.")

        # Seed Specializations if empty
        if not DoctorSpecialization.query.first():
            specs = [
                'Orthopedics', 'Internal Medicine', 'Obstetrics and Gynecology',
                'Dermatology', 'Pediatrics', 'Radiology', 'General Surgery',
                'Ophthalmology', 'Anesthesia', 'Pathology', 'ENT', 'Dental Care',
                'Dermatologists', 'Endocrinologists', 'Neurologists'
            ]
            for s in specs:
                db.session.add(DoctorSpecialization(specilization=s))
            print("Doctor specializations seeded.")

        # Seed Default Doctors if empty
        if not Doctor.query.first():
            d1 = Doctor(
                specilization='ENT',
                doctorName='Anuj kumar',
                address='A 123 XYZ Apartment Raj Nagar Ext Ghaziabad',
                docFees='500',
                contactno=142536250,
                docEmail='anujk123@test.com',
                password=hashlib.md5('Test@123'.encode('utf-8')).hexdigest()
            )
            d2 = Doctor(
                specilization='Endocrinologists',
                doctorName='Charu Dua',
                address='X 1212 ABC Apartment Laxmi Nagar New Delhi',
                docFees='800',
                contactno=1231231230,
                docEmail='charudua12@test.com',
                password=hashlib.md5('Test@123'.encode('utf-8')).hexdigest()
            )
            db.session.add_all([d1, d2])
            print("Default doctors seeded.")

        # Seed Default Users if empty
        if not User.query.first():
            u1 = User(
                fullName='John Doe',
                address='A 123 ABC Apartment GZB 201017',
                city='Ghaziabad',
                gender='male',
                email='johndoe12@test.com',
                password=hashlib.md5('Test@123'.encode('utf-8')).hexdigest()
            )
            u2 = User(
                fullName='Amit kumar',
                address='new Delhi india',
                city='New Delhi',
                gender='male',
                email='amitk@gmail.com',
                password=hashlib.md5('Test@123'.encode('utf-8')).hexdigest()
            )
            db.session.add_all([u1, u2])
            print("Default users seeded.")

        # Seed TblPage if empty
        if not TblPage.query.first():
            p1 = TblPage(
                PageType='aboutus',
                PageTitle='About Us',
                PageDescription='The Hospital Management System (HMS) is designed for Any Hospital to replace their existing manual, paper based system. The new system is to control the following information: patient information, room availability, staff and operating room schedules, and patient invoices.'
            )
            p2 = TblPage(
                PageType='contactus',
                PageTitle='Contact Details',
                PageDescription='D-204, Hole Town South West, Delhi-110096, India',
                Email='info@gmail.com',
                MobileNumber=1122334455,
                OpenningTime='9 am To 8 Pm'
            )
            db.session.add_all([p1, p2])
            print("CMS Pages seeded.")

        db.session.commit()
        print("Database initialization complete!")

if __name__ == '__main__':
    init_database()
