from flask import Blueprint, render_template, request, flash, redirect, url_for, session, jsonify
from models import db, User, Doctor, DoctorSpecialization, Appointment, TblPatient, TblMedicalHistory, TblBilling, TblBloodReport, UserLog
from utils import patient_required, get_client_ip
import hashlib
from datetime import datetime

patient_bp = Blueprint('patient', __name__, url_prefix='/patient')

@patient_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(email=username).first()
        if user and user.check_password(password):
            session['patient_id'] = user.id
            session['patient_name'] = user.fullName
            session['patient_email'] = user.email

            # Record user log
            log_entry = UserLog(
                uid=user.id,
                username=user.email,
                userip=get_client_ip(),
                status=1
            )
            db.session.add(log_entry)
            db.session.commit()

            flash(f'Welcome back, {user.fullName}!', 'success')
            return redirect(url_for('patient.dashboard'))
        else:
            # Failed log
            log_entry = UserLog(
                username=username,
                userip=get_client_ip(),
                status=0
            )
            db.session.add(log_entry)
            db.session.commit()

            flash('Invalid email or password.', 'danger')

    return render_template('patient/login.html')

@patient_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        address = request.form.get('address')
        city = request.form.get('city')
        gender = request.form.get('gender')
        email = request.form.get('email')
        password = request.form.get('password')

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered! Please log in.', 'warning')
            return redirect(url_for('patient.login'))

        new_user = User(
            fullName=full_name,
            address=address,
            city=city,
            gender=gender,
            email=email
        )
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('patient.login'))

    return render_template('patient/register.html')

@patient_bp.route('/logout')
def logout():
    session.pop('patient_id', None)
    session.pop('patient_name', None)
    session.pop('patient_email', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('patient.login'))

@patient_bp.route('/dashboard')
@patient_required
def dashboard():
    user = User.query.get(session['patient_id'])
    total_appointments = Appointment.query.filter_by(userId=user.id).count()
    return render_template('patient/dashboard.html', user=user, total_appointments=total_appointments)

@patient_bp.route('/book-appointment', methods=['GET', 'POST'])
@patient_required
def book_appointment():
    if request.method == 'POST':
        spec = request.form.get('Doctorspecialization')
        doctor_id = request.form.get('doctor')
        fees = request.form.get('fees')
        app_date = request.form.get('appdate')
        app_time = request.form.get('apptime')

        appointment = Appointment(
            doctorSpecialization=spec,
            doctorId=int(doctor_id),
            userId=session['patient_id'],
            consultancyFees=int(fees) if fees else 0,
            appointmentDate=app_date,
            appointmentTime=app_time,
            userStatus=1,
            doctorStatus=1
        )
        db.session.add(appointment)
        db.session.commit()

        flash('Appointment booked successfully!', 'success')
        return redirect(url_for('patient.appointment_history'))

    specializations = DoctorSpecialization.query.all()
    return render_template('patient/book_appointment.html', specializations=specializations)

@patient_bp.route('/get-doctors/<spec_name>')
@patient_required
def get_doctors(spec_name):
    doctors = Doctor.query.filter_by(specilization=spec_name).all()
    doc_list = [{'id': doc.id, 'name': doc.doctorName, 'fees': doc.docFees} for doc in doctors]
    return jsonify(doc_list)

@patient_bp.route('/appointment-history', methods=['GET', 'POST'])
@patient_required
def appointment_history():
    if request.method == 'POST' and 'cancel' in request.form:
        app_id = request.form.get('app_id')
        app = Appointment.query.get(app_id)
        if app and app.userId == session['patient_id']:
            app.userStatus = 0
            db.session.commit()
            flash('Appointment canceled.', 'info')
        return redirect(url_for('patient.appointment_history'))

    appointments = db.session.query(Appointment, Doctor)\
        .join(Doctor, Appointment.doctorId == Doctor.id)\
        .filter(Appointment.userId == session['patient_id'])\
        .order_by(Appointment.id.desc()).all()

    return render_template('patient/appointment_history.html', appointments=appointments)

@patient_bp.route('/edit-profile', methods=['GET', 'POST'])
@patient_required
def edit_profile():
    user = User.query.get(session['patient_id'])
    if request.method == 'POST':
        user.fullName = request.form.get('fname')
        user.address = request.form.get('address')
        user.city = request.form.get('city')
        user.gender = request.form.get('gender')
        db.session.commit()
        session['patient_name'] = user.fullName
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('patient.edit_profile'))

    return render_template('patient/edit_profile.html', user=user)

@patient_bp.route('/change-password', methods=['GET', 'POST'])
@patient_required
def change_password():
    if request.method == 'POST':
        c_pass = request.form.get('cpass')
        new_pass = request.form.get('npass')
        user = User.query.get(session['patient_id'])

        if user.check_password(c_pass):
            user.set_password(new_pass)
            db.session.commit()
            flash('Password changed successfully!', 'success')
        else:
            flash('Current password does not match.', 'danger')

    return render_template('patient/change_password.html')

@patient_bp.route('/bills')
@patient_required
def bills():
    # Find patient record linked by email
    user = User.query.get(session['patient_id'])
    patient = TblPatient.query.filter_by(PatientEmail=user.email).first()
    bills_list = []
    if patient:
        bills_list = db.session.query(TblBilling, Doctor)\
            .join(Doctor, TblBilling.DoctorID == Doctor.id)\
            .filter(TblBilling.PatientID == patient.ID).all()

    return render_template('patient/bills.html', bills=bills_list)

@patient_bp.route('/blood-reports')
@patient_required
def blood_reports():
    user = User.query.get(session['patient_id'])
    patient = TblPatient.query.filter_by(PatientEmail=user.email).first()
    reports_list = []
    if patient:
        reports_list = db.session.query(TblBloodReport, Doctor)\
            .join(Doctor, TblBloodReport.DoctorID == Doctor.id)\
            .filter(TblBloodReport.PatientID == patient.ID).all()

    return render_template('patient/blood_reports.html', reports=reports_list)

@patient_bp.route('/medical-history')
@patient_required
def medical_history():
    user = User.query.get(session['patient_id'])
    patient = TblPatient.query.filter_by(PatientEmail=user.email).first()
    history_list = []
    if patient:
        history_list = TblMedicalHistory.query.filter_by(PatientID=patient.ID).all()

    return render_template('patient/medical_history.html', history=history_list, patient=patient)
