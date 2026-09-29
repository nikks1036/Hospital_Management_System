from flask import Blueprint, render_template, request, flash, redirect, url_for
from models import db, TblContactUs, TblPage

public_bp = Blueprint('public', __name__)

@public_bp.route('/')
def index():
    about_page = TblPage.query.filter_by(PageType='aboutus').first()
    contact_page = TblPage.query.filter_by(PageType='contactus').first()
    return render_template('public/index.html', about=about_page, contact=contact_page)

@public_bp.route('/contact-submit', methods=['POST'])
def contact_submit():
    name = request.form.get('fullname')
    email = request.form.get('emailid')
    mobile = request.form.get('mobileno')
    message = request.form.get('description')

    if name and email and mobile and message:
        contact_entry = TblContactUs(
            fullname=name,
            email=email,
            contactno=mobile,
            message=message,
            IsRead=0
        )
        db.session.add(contact_entry)
        db.session.commit()
        flash('Your query has been successfully submitted!', 'success')
    else:
        flash('Please fill in all fields.', 'danger')

    return redirect(url_for('public.index') + '#contact_us')
