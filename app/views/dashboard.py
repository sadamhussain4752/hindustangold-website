
from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import UserMixin, current_user, login_required, login_user
from .. import app
from ..models.user import User
from ..models.goldprice import GoldPrice, UserGoldPrice
from ..models.contactus import ContactUs, RequestCallBack, Career

auth = Blueprint('auth', __name__)

#define global variables here
CONTACT_US_COUNT = None
REQUEST_CALLBACK_COUNT = None
PRICE_ENQUIRY_COUNT = None
CAREER_ENQUIRY_COUNT = None

@auth.route('/admin/login/', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get('username')
        password = request.form.get('password')
        remember = True         
        user = User.query.filter_by(email=email, password=password).first()
        if not user:            
            return redirect(url_for('auth.login'))
        else:
            login_user(user=user, remember=remember)
            return redirect(url_for('auth.dashboard'))            
    return render_template('backend/login.html')

@auth.route('/admin/dashboard/', methods=['GET'])
@login_required
def dashboard():
    global CONTACT_US_COUNT
    global REQUEST_CALLBACK_COUNT
    global PRICE_ENQUIRY_COUNT
    global CAREER_ENQUIRY_COUNT
    if not CONTACT_US_COUNT:        
        CONTACT_US_COUNT  =  ContactUs.query.count()
    
    if not REQUEST_CALLBACK_COUNT:
        REQUEST_CALLBACK_COUNT = RequestCallBack.query.count()
    
    if not PRICE_ENQUIRY_COUNT:
        PRICE_ENQUIRY_COUNT = UserGoldPrice.query.count()

    if not CAREER_ENQUIRY_COUNT:
        CAREER_ENQUIRY_COUNT = Career.query.count()
    # code to validate and add user to database goes here
    return render_template("backend/dashboard.html", dashboard ={
        'CONTACT_US_COUNT': CONTACT_US_COUNT,
        'REQUEST_CALLBACK_COUNT': REQUEST_CALLBACK_COUNT,
        'PRICE_ENQUIRY_COUNT': PRICE_ENQUIRY_COUNT,
        'CAREER_ENQUIRY_COUNT': CAREER_ENQUIRY_COUNT,

    })            

@app.login_manager.unauthorized_handler     # In unauthorized_handler we have a callback URL 
def unauthorized_callback():            # In call back url we can specify where we want to 
       return redirect(url_for('auth.login'))

############### DATA TABLES ##############################

# @auth.route('/admin/contact-us-list', methods=['GET'])
# @login_required
# def contact_us_datatable():
#     list_of_contacts = ContactUs.query.order_by(ContactUs.id.desc())
#     return render_template("backend/datatables/contact_us_datatable.html", list_of_contacts=list_of_contacts)


# @auth.route('/admin/request-forms-list', methods=['GET'])
# @login_required
# def request_forms_datatable():
#     list_of_contacts = RequestCallBack.query.order_by(RequestCallBack.id.desc())
#     return render_template("backend/datatables/callback_datatable.html", list_of_contacts=list_of_contacts)


