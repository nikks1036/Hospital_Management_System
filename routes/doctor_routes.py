from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from models import db, Doctor, Appointment, TblPatient, TblMedicalHistory, TblBloodReport, DoctorLog, User
from utils import doctor_required, get_client_ip
from werkzeug.utils import secure_filename
import os

doctor_bp = Blueprint('doctor', __name__, url_prefix='/doctor')

@doctor_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        doc = Doctor.query.filter_by(docEmail=username).first()
        if doc and doc.check_password(password):
            session['doctor_id'] = doc.id
            session['doctor_name'] = doc.doctorName
            session['doctor_email'] = doc.docEmail

            log_entry = DoctorLog(
                uid=doc.id,
                username=doc.docEmail,
                userip=get_client_ip(),
                status=1
            )
            db.session.add(log_entry)
            db.session.commit()

            flash(f'Welcome, Dr. {doc.doctorName}!', 'success')
            return redirect(url_for('doctor.dashboard'))
        else:
            log_entry = DoctorLog(
                username=username,
                userip=get_client_ip(),
                status=0
            )
            db.session.add(log_entry)
            db.session.commit()

            flash('Invalid doctor credentials.', 'danger')

    return render_template('doctor/login.html')

@doctor_bp.route('/logout')
def logout():
    session.pop('doctor_id', None)
    session.pop('doctor_name', None)
    session.pop('doctor_email', None)
    flash('Doctor logged out successfully.', 'info')
    return redirect(url_for('doctor.login'))

@doctor_bp.route('/dashboard')
@doctor_required
def dashboard():
    doc_id = session['doctor_id']
    total_patients = TblPatient.query.filter_by(Docid=doc_id).count()
    total_appointments = Appointment.query.filter_by(doctorId=doc_id).count()
    return render_template('doctor/dashboard.html', total_patients=total_patients, total_appointments=total_appointments)

@doctor_bp.route('/appointment-history', methods=['GET', 'POST'])
@doctor_required
def appointment_history():
    doc_id = session['doctor_id']
    if request.method == 'POST':
        app_id = request.form.get('app_id')
        action = request.form.get('action')
        app = Appointment.query.get(app_id)
        if app and app.doctorId == doc_id:
            if action == 'cancel':
                app.doctorStatus = 0
                flash('Appointment canceled by doctor.', 'info')
            elif action == 'approve':
                app.doctorStatus = 1
                flash('Appointment approved.', 'success')
            db.session.commit()
        return redirect(url_for('doctor.appointment_history'))

    appointments = db.session.query(Appointment, User)\
        .join(User, Appointment.userId == User.id)\
        .filter(Appointment.doctorId == doc_id)\
        .order_by(Appointment.id.desc()).all()

    return render_template('doctor/appointment_history.html', appointments=appointments)

@doctor_bp.route('/add-patient', methods=['GET', 'POST'])
@doctor_required
def add_patient():
    if request.method == 'POST':
        pname = request.form.get('patname')
        pcont = request.form.get('patcontact')
        pemail = request.form.get('patemail')
        pgender = request.form.get('gender')
        padd = request.form.get('pataddress')
        page = request.form.get('patage')
        pmedhis = request.form.get('medhis')

        patient = TblPatient(
            Docid=session['doctor_id'],
            PatientName=pname,
            PatientContno=int(pcont) if pcont else None,
            PatientEmail=pemail,
            PatientGender=pgender,
            PatientAdd=padd,
            PatientAge=int(page) if page else None,
            PatientMedhis=pmedhis
        )
        db.session.add(patient)
        db.session.commit()

        flash('Patient record added successfully!', 'success')
        return redirect(url_for('doctor.manage_patient'))

    return render_template('doctor/add_patient.html')

@doctor_bp.route('/manage-patient')
@doctor_required
def manage_patient():
    patients = TblPatient.query.filter_by(Docid=session['doctor_id']).all()
    return render_template('doctor/manage_patient.html', patients=patients)

@doctor_bp.route('/view-patient/<int:id>', methods=['GET', 'POST'])
@doctor_required
def view_patient(id):
    patient = TblPatient.query.get_or_404(id)

    if request.method == 'POST':
        bp = request.form.get('bp')
        bs = request.form.get('bs')
        weight = request.form.get('weight')
        temp = request.form.get('temp')
        pres = request.form.get('pres')

        history = TblMedicalHistory(
            PatientID=patient.ID,
            BloodPressure=bp,
            BloodSugar=bs,
            Weight=weight,
            Temperature=temp,
            MedicalPres=pres
        )
        db.session.add(history)
        db.session.commit()

        flash('Medical history record added!', 'success')
        return redirect(url_for('doctor.view_patient', id=id))

    medical_records = TblMedicalHistory.query.filter_by(PatientID=patient.ID).all()
    return render_template('doctor/view_patient.html', patient=patient, medical_records=medical_records)

@doctor_bp.route('/edit-patient/<int:id>', methods=['GET', 'POST'])
@doctor_required
def edit_patient(id):
    patient = TblPatient.query.get_or_404(id)
    if request.method == 'POST':
        patient.PatientName = request.form.get('patname')
        patient.PatientContno = request.form.get('patcontact')
        patient.PatientEmail = request.form.get('patemail')
        patient.PatientGender = request.form.get('gender')
        patient.PatientAdd = request.form.get('pataddress')
        patient.PatientAge = request.form.get('patage')
        patient.PatientMedhis = request.form.get('medhis')
        db.session.commit()

        flash('Patient details updated!', 'success')
        return redirect(url_for('doctor.manage_patient'))

    return render_template('doctor/edit_patient.html', patient=patient)

@doctor_bp.route('/add-blood-report', methods=['GET', 'POST'])
@doctor_required
def add_blood_report():
    patients = TblPatient.query.filter_by(Docid=session['doctor_id']).all()
    if request.method == 'POST':
        pid = request.form.get('patient_id')
        hb = request.form.get('hb')
        wbc = request.form.get('wbc')
        rbc = request.form.get('rbc')
        platelets = request.form.get('platelets')
        bg = request.form.get('bg')
        bs = request.form.get('bs')
        chol = request.form.get('chol')
        remark = request.form.get('remark')
        report_date = request.form.get('report_date')

        report = TblBloodReport(
            PatientID=int(pid),
            DoctorID=session['doctor_id'],
            Hemoglobin=hb,
            WBC=wbc,
            RBC=rbc,
            Platelets=platelets,
            BloodGroup=bg,
            BloodSugar=bs,
            Cholesterol=chol,
            DoctorRemark=remark,
            ReportDate=report_date
        )
        db.session.add(report)
        db.session.commit()

        flash('Blood report generated!', 'success')
        return redirect(url_for('doctor.manage_blood_report'))

    return render_template('doctor/add_blood_report.html', patients=patients)

@doctor_bp.route('/manage-blood-report')
@doctor_required
def manage_blood_report():
    reports = db.session.query(TblBloodReport, TblPatient)\
        .join(TblPatient, TblBloodReport.PatientID == TblPatient.ID)\
        .filter(TblBloodReport.DoctorID == session['doctor_id']).all()

    return render_template('doctor/manage_blood_report.html', reports=reports)

@doctor_bp.route('/search-patient', methods=['GET', 'POST'])
@doctor_required
def search_patient():
    patients = []
    search_query = ''
    if request.method == 'POST':
        search_query = request.form.get('searchdata', '')
        patients = TblPatient.query.filter(
            (TblPatient.PatientName.like(f'%{search_query}%')) |
            (TblPatient.PatientContno.like(f'%{search_query}%'))
        ).all()

    return render_template('doctor/search.html', patients=patients, search_query=search_query)

@doctor_bp.route('/edit-profile', methods=['GET', 'POST'])
@doctor_required
def edit_profile():
    doc = Doctor.query.get(session['doctor_id'])
    if request.method == 'POST':
        doc.doctorName = request.form.get('docname')
        doc.address = request.form.get('clinicaddress')
        doc.docFees = request.form.get('docfees')
        doc.contactno = request.form.get('doccontact')
        db.session.commit()
        session['doctor_name'] = doc.doctorName
        flash('Doctor profile updated!', 'success')
        return redirect(url_for('doctor.edit_profile'))

    return render_template('doctor/edit_profile.html', doctor=doc)

@doctor_bp.route('/change-password', methods=['GET', 'POST'])
@doctor_required
def change_password():
    if request.method == 'POST':
        c_pass = request.form.get('cpass')
        new_pass = request.form.get('npass')
        doc = Doctor.query.get(session['doctor_id'])

        if doc.check_password(c_pass):
            doc.set_password(new_pass)
            db.session.commit()
            flash('Password updated successfully!', 'success')
        else:
            flash('Current password is incorrect.', 'danger')

    return render_template('doctor/change_password.html')
