from functools import wraps
from flask import session, redirect, url_for, flash, request

def get_client_ip():
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0]
    return request.remote_addr or '127.0.0.1'

def patient_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'patient_id' not in session:
            flash('Please log in to access the patient portal.', 'warning')
            return redirect(url_for('patient.login'))
        return f(*args, **kwargs)
    return decorated_function

def doctor_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'doctor_id' not in session:
            flash('Please log in to access the doctor portal.', 'warning')
            return redirect(url_for('doctor.login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            flash('Please log in to access the admin portal.', 'warning')
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated_function
