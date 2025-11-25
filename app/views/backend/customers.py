import os
from flask import Blueprint, redirect, render_template, request, url_for, abort, send_file
from flask_login import UserMixin, current_user, login_required, login_user
from flask_sqlalchemy import Pagination
from app import db 
from ... import app
from ...models.user import User
from ...models.goldprice import UserGoldPrice
from ...models.contactus import ContactUs, RequestCallBack, Career



customers = Blueprint('customers', __name__)



############### DATA TABLES ##############################
def paginate(query, page, per_page=20, error_out=True):
    if error_out and page < 1:
        abort(404)
    items = query.limit(per_page).offset((page - 1) * per_page).all()
    if not items and page != 1 and error_out:
        abort(404)
    if page == 1 and len(items) < per_page:
        total = len(items)
    else:
        total = query.order_by(None).count()
    return Pagination(query, page, per_page, total, items) 

@customers.route('/admin/contact-us-list', methods=['GET'])
@login_required
def contact_us_datatable():
    list_of_contacts = ContactUs.query.order_by(ContactUs.id.desc())#.limit(20)
    if request.args.get('page'):
        page = int(request.args.get('page'))
    else :
        page = 1
    list_of_contacts = paginate(list_of_contacts, page, 20)
    return render_template("backend/datatables/contact_us_datatable.html", list_of_contacts=list_of_contacts)


@customers.route('/admin/request-forms-list', methods=["GET", "POST"])
@login_required
def request_forms_datatable():
    list_of_contacts = RequestCallBack.query.order_by(RequestCallBack.id.desc())#.limit(20)
    if request.method == "POST":
        status = request.form.get('status')
        id = request.form.get('id')
        callback = RequestCallBack.query.get(id)
        callback.status = status
        db.session.commit()
    if request.args.get('page'):
        page = int(request.args.get('page'))
    else :
        page = 1
    list_of_contacts = paginate(list_of_contacts, page, 20)
    return render_template("backend/datatables/callback_datatable.html", list_of_contacts=list_of_contacts)


@customers.route('/admin/user-gold-price-enquiry', methods=["GET", "POST"])
@login_required
def gold_price_enquiry():
    list_of_contacts = UserGoldPrice.query.order_by(UserGoldPrice.id.desc())
    
    if request.method == "POST":
        status = request.form.get('status')
        id = request.form.get('id')
        gold_price = UserGoldPrice.query.get(id)
        gold_price.status = status
        db.session.commit()

    if request.args.get('page'):
        page = int(request.args.get('page'))
    else :
        page = 1
    list_of_contacts = paginate(list_of_contacts, page, 20)
    return render_template("backend/datatables/price_enqiry_datatable.html", list_of_contacts=list_of_contacts)


@customers.route('/admin/career-enquiry', methods=['GET'])
@login_required
def career_enquiry():
    list_of_contacts = Career.query.order_by(Career.id.desc())
    if request.args.get('page'):
        page = int(request.args.get('page'))
    else :
        page = 1
    list_of_contacts = paginate(list_of_contacts, page, 20)
    return render_template("backend/datatables/career_enqiry_datatable.html", list_of_contacts=list_of_contacts)

@customers.route('/download-resume/<filename>')
@login_required
def download_resume(filename):
    #For windows you need to use drive name [ex: F:/Example.pdf]
    path = os.path.join(app.config['RESUME_FOLDER'], filename)
    return send_file(path, as_attachment=True)
