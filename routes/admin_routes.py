from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from models import db, Admin, Doctor, DoctorSpecialization, User, Appointment, TblPatient, TblBilling, TblBloodReport, TblContactUs, TblPage, DoctorLog, UserLog
from utils import admin_required
import hashlib
from datetime import datetime

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        admin = Admin.query.filter_by(username=username).first()
        if admin and admin.check_password(password):
            session['admin_id'] = admin.id
            session['admin_name'] = admin.username
            flash('Admin login successful!', 'success')
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid admin credentials.', 'danger')

    return render_template('admin/login.html')

@admin_bp.route('/logout')
def logout():
    session.pop('admin_id', None)
    session.pop('admin_name', None)
    flash('Admin logged out.', 'info')
    return redirect(url_for('admin.login'))

@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    total_users = User.query.count()
    total_doctors = Doctor.query.count()
    total_appointments = Appointment.query.count()
    total_patients = TblPatient.query.count()
    unread_queries = TblContactUs.query.filter_by(IsRead=0).count()
    return render_template('admin/dashboard.html',
                           total_users=total_users,
                           total_doctors=total_doctors,
                           total_appointments=total_appointments,
                           total_patients=total_patients,
                           unread_queries=unread_queries)

@admin_bp.route('/doctor-specialization', methods=['GET', 'POST'])
@admin_required
def doctor_specialization():
    if request.method == 'POST':
        spec_name = request.form.get('doctorspecilization')
        if spec_name:
            spec = DoctorSpecialization(specilization=spec_name)
            db.session.add(spec)
            db.session.commit()
            flash('Specialization added successfully!', 'success')
        return redirect(url_for('admin.doctor_specialization'))

    specs = DoctorSpecialization.query.all()
    return render_template('admin/doctor_specialization.html', specs=specs)

@admin_bp.route('/delete-specialization/<int:id>')
@admin_required
def delete_specialization(id):
    spec = DoctorSpecialization.query.get_or_404(id)
    db.session.delete(spec)
    db.session.commit()
    flash('Specialization deleted.', 'info')
    return redirect(url_for('admin.doctor_specialization'))

@admin_bp.route('/add-doctor', methods=['GET', 'POST'])
@admin_required
def add_doctor():
    if request.method == 'POST':
        spec = request.form.get('Doctorspecialization')
        doc_name = request.form.get('docname')
        address = request.form.get('clinicaddress')
        doc_fees = request.form.get('docfees')
        contact = request.form.get('doccontact')
        email = request.form.get('docemail')
        password = request.form.get('npass')

        existing = Doctor.query.filter_by(docEmail=email).first()
        if existing:
            flash('Doctor email already exists!', 'warning')
            return redirect(url_for('admin.add_doctor'))

        doc = Doctor(
            specilization=spec,
            doctorName=doc_name,
            address=address,
            docFees=doc_fees,
            contactno=int(contact) if contact else None,
            docEmail=email
        )
        doc.set_password(password)
        db.session.add(doc)
        db.session.commit()

        flash('Doctor added successfully!', 'success')
        return redirect(url_for('admin.manage_doctors'))

    specializations = DoctorSpecialization.query.all()
    return render_template('admin/add_doctor.html', specializations=specializations)

@admin_bp.route('/manage-doctors')
@admin_required
def manage_doctors():
    doctors = Doctor.query.all()
    return render_template('admin/manage_doctors.html', doctors=doctors)

@admin_bp.route('/delete-doctor/<int:id>')
@admin_required
def delete_doctor(id):
    doc = Doctor.query.get_or_404(id)
    db.session.delete(doc)
    db.session.commit()
    flash('Doctor record deleted.', 'info')
    return redirect(url_for('admin.manage_doctors'))

@admin_bp.route('/edit-doctor/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_doctor(id):
    doc = Doctor.query.get_or_404(id)
    if request.method == 'POST':
        doc.specilization = request.form.get('Doctorspecialization')
        doc.doctorName = request.form.get('docname')
        doc.address = request.form.get('clinicaddress')
        doc.docFees = request.form.get('docfees')
        doc.contactno = request.form.get('doccontact')
        db.session.commit()
        flash('Doctor details updated!', 'success')
        return redirect(url_for('admin.manage_doctors'))

    specs = DoctorSpecialization.query.all()
    return render_template('admin/edit_doctor.html', doctor=doc, specs=specs)

@admin_bp.route('/manage-users')
@admin_required
def manage_users():
    users = User.query.all()
    return render_template('admin/manage_users.html', users=users)

@admin_bp.route('/delete-user/<int:id>')
@admin_required
def delete_user(id):
    usr = User.query.get_or_404(id)
    db.session.delete(usr)
    db.session.commit()
    flash('User account deleted.', 'info')
    return redirect(url_for('admin.manage_users'))

@admin_bp.route('/manage-patients')
@admin_required
def manage_patients():
    patients = TblPatient.query.all()
    return render_template('admin/manage_patients.html', patients=patients)

@admin_bp.route('/view-patient/<int:id>')
@admin_required
def view_patient(id):
    patient = TblPatient.query.get_or_404(id)
    return render_template('admin/view_patient.html', patient=patient)

@admin_bp.route('/appointment-history')
@admin_required
def appointment_history():
    appointments = db.session.query(Appointment, Doctor, User)\
        .join(Doctor, Appointment.doctorId == Doctor.id)\
        .join(User, Appointment.userId == User.id)\
        .order_by(Appointment.id.desc()).all()

    return render_template('admin/appointment_history.html', appointments=appointments)

@admin_bp.route('/unread-queries')
@admin_required
def unread_queries():
    queries = TblContactUs.query.filter_by(IsRead=0).all()
    return render_template('admin/queries.html', queries=queries, title="Unread Queries")

@admin_bp.route('/read-queries')
@admin_required
def read_queries():
    queries = TblContactUs.query.filter_by(IsRead=1).all()
    return render_template('admin/queries.html', queries=queries, title="Read Queries")

@admin_bp.route('/query-details/<int:id>', methods=['GET', 'POST'])
@admin_required
def query_details(id):
    query = TblContactUs.query.get_or_404(id)
    if request.method == 'POST':
        query.AdminRemark = request.form.get('adminremark')
        query.IsRead = 1
        db.session.commit()
        flash('Query status updated!', 'success')
        return redirect(url_for('admin.unread_queries'))

    query.IsRead = 1
    db.session.commit()
    return render_template('admin/query_details.html', query=query)

@admin_bp.route('/manage-bills')
@admin_required
def manage_bills():
    bills = db.session.query(TblBilling, TblPatient, Doctor)\
        .join(TblPatient, TblBilling.PatientID == TblPatient.ID)\
        .join(Doctor, TblBilling.DoctorID == Doctor.id).all()

    return render_template('admin/manage_bills.html', bills=bills)

@admin_bp.route('/add-bill', methods=['GET', 'POST'])
@admin_required
def add_bill():
    patients = TblPatient.query.all()
    doctors = Doctor.query.all()

    if request.method == 'POST':
        bill_no = f"BILL{datetime.now().strftime('%Y%m%d%H%M%S')}"
        pid = request.form.get('patient_id')
        did = request.form.get('doctor_id')
        c_fee = float(request.form.get('consultation_fee') or 0)
        m_fee = float(request.form.get('medicine_charge') or 0)
        l_fee = float(request.form.get('lab_charge') or 0)
        r_fee = float(request.form.get('room_charge') or 0)
        o_fee = float(request.form.get('other_charge') or 0)
        disc = float(request.form.get('discount') or 0)
        gst = float(request.form.get('gst') or 18)
        mode = request.form.get('payment_mode')
        status = request.form.get('payment_status')

        subtotal = c_fee + m_fee + l_fee + r_fee + o_fee - disc
        total = subtotal + (subtotal * (gst / 100))

        bill = TblBilling(
            BillNumber=bill_no,
            PatientID=int(pid),
            DoctorID=int(did),
            ConsultationFee=c_fee,
            MedicineCharge=m_fee,
            LabCharge=l_fee,
            RoomCharge=r_fee,
            OtherCharge=o_fee,
            Discount=disc,
            GST=gst,
            TotalAmount=total,
            PaymentMode=mode,
            PaymentStatus=status
        )
        db.session.add(bill)
        db.session.commit()

        flash('Invoice generated successfully!', 'success')
        return redirect(url_for('admin.manage_bills'))

    return render_template('admin/add_bill.html', patients=patients, doctors=doctors)

@admin_bp.route('/print-bill/<int:id>')
@admin_required
def print_bill(id):
    bill = db.session.query(TblBilling, TblPatient, Doctor)\
        .join(TblPatient, TblBilling.PatientID == TblPatient.ID)\
        .join(Doctor, TblBilling.DoctorID == Doctor.id)\
        .filter(TblBilling.ID == id).first_or_404()

    return render_template('admin/print_bill.html', bill=bill[0], patient=bill[1], doctor=bill[2])

@admin_bp.route('/delete-bill/<int:id>')
@admin_required
def delete_bill(id):
    bill = TblBilling.query.get_or_404(id)
    db.session.delete(bill)
    db.session.commit()
    flash('Bill deleted.', 'info')
    return redirect(url_for('admin.manage_bills'))

@admin_bp.route('/user-logs')
@admin_required
def user_logs():
    logs = UserLog.query.order_by(UserLog.id.desc()).all()
    return render_template('admin/user_logs.html', logs=logs)

@admin_bp.route('/doctor-logs')
@admin_required
def doctor_logs():
    logs = DoctorLog.query.order_by(DoctorLog.id.desc()).all()
    return render_template('admin/doctor_logs.html', logs=logs)

@admin_bp.route('/about-us-cms', methods=['GET', 'POST'])
@admin_required
def about_us_cms():
    page = TblPage.query.filter_by(PageType='aboutus').first()
    if request.method == 'POST':
        if not page:
            page = TblPage(PageType='aboutus')
            db.session.add(page)
        page.PageTitle = request.form.get('pagetitle')
        page.PageDescription = request.form.get('pagedescription')
        db.session.commit()
        flash('About Us page updated successfully!', 'success')
        return redirect(url_for('admin.about_us_cms'))

    return render_template('admin/cms_page.html', page=page, page_type="About Us")

@admin_bp.route('/contact-us-cms', methods=['GET', 'POST'])
@admin_required
def contact_us_cms():
    page = TblPage.query.filter_by(PageType='contactus').first()
    if request.method == 'POST':
        if not page:
            page = TblPage(PageType='contactus')
            db.session.add(page)
        page.PageTitle = request.form.get('pagetitle')
        page.PageDescription = request.form.get('pagedescription')
        page.Email = request.form.get('email')
        page.MobileNumber = request.form.get('mobilenumber')
        page.OpenningTime = request.form.get('timing')
        db.session.commit()
        flash('Contact Us page updated successfully!', 'success')
        return redirect(url_for('admin.contact_us_cms'))

    return render_template('admin/cms_contact.html', page=page)
