
import os
import random
import string
import requests
import re
from datetime import datetime


from flask import Blueprint, render_template, request, redirect, url_for, send_from_directory
from flask import Flask, jsonify

from app.models import BranchRelation, State, BranchReview
from app.models.branches import Branch

from app import app
from app.models.goldprice import HindustanGoldPrice

from .. import db, cache
from ..models import ContactUs

from app import global_states_data

home = Blueprint("home", __name__)

gold_gloal_prices = None
all_meta_datas = None

otp_global = None

@home.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),'img/gold-buyers.png',mimetype='image/vnd.microsof.icon')

@home.route('/', methods=["GET"])
@cache.cached(timeout=40, key_prefix='home_page')
def index():
    return render_template("index.html")


@home.route('/about/', methods=["GET"])
# @cache.cached(timeout=40, key_prefix='about_us')
def about_us():
    return render_template("about-us.html")

def send_otp_via_kaleyra(phone_number, otp):
    url = "https://api.kaleyra.io/v1/HXIN1740312932IN/messages"  # Use the correct SID (seems to be your API key here)
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',  # As per Kaleyra's docs
        'api-key': 'Adc65983a53915ef93f71e0f115cf5888',  # Your provided API key
    }
    payload = {
        'to': phone_number,  # The recipient's phone number
        'type': 'OTP',  # Message type, here it's OTP
        'sender': 'HGCGLD',  # Your Sender ID
        'body': f'Hi CMM Hindustan Gold. Your OSP for approval is {otp}.',  # Updated body matching the template
        'template_id': 1107166443888182075  # Correct template ID for this message
    }

    # Send the request and handle exceptions
    try:
        response = requests.post(url, headers=headers, data=payload)
        
        # Debugging: print the request details
        print("Sending request with payload:")
        print(f"URL: {url}")
        print(f"Headers: {headers}")
        print(f"Payload: {payload}")
        
        # Check response status
        if response.status_code == 202:
            print("OTP request accepted, message is being processed!")
        elif response.status_code == 200:
            print("OTP sent successfully!")
        else:
            print(f"Failed to send OTP. Status code: {response.status_code}, Response: {response.text}")
        
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

    return response


def generate_otp(length=6):
    global otp_global
    otp_global = ''.join(random.choices(string.digits, k=length))
    return otp_global

def format_phone_number(phone):
    # Remove leading +91, 91, or 0 if present
    formatted_phone = re.sub(r"^(\+91|91|0)", "", phone)
    return formatted_phone



@home.route('/verify', methods=["POST"])
def verifyPhone():
    data = request.get_json()
    phone = data.get('phone')
    formatted_phone = "+91"+format_phone_number(phone)
    otp = generate_otp()
    otp_global = otp
    response = send_otp_via_kaleyra(formatted_phone, otp)
    if response.status_code == 202:
        return jsonify({'success': True, 'message': 'OTP sent successfully'})
        
    else:
        return jsonify({'success': False, 'message': 'Something went wrong!'})

    

@home.route('/verify-otp', methods=["POST"])
def verifyOtp():
    data = request.get_json()
    print("TEST:",data.get('otp'))
    print(otp_global)
    
    if(otp_global == data.get('otp')):
        return jsonify({'success': True, 'message': 'Phone number verified successfully'})
    else:
        return jsonify({'success': False, 'message': 'Something went wrong!'})


@home.route('/contact/', methods=["GET", "POST"])
# @cache.cached(timeout=40, key_prefix='contact_us')
def contact_us():
    if request.method == "POST":
        full_name = request.form.get('name')
        email = request.form.get('email')
        phone_number = request.form.get('phone')
        subject = request.form.get('subject')
        message = request.form.get('message')
        contact_us_obj = ContactUs(full_name=full_name, email=email,
                                   phone_number=phone_number, subject=subject,
                                   message=message, status=1)
        try:
            db.session.add(contact_us_obj)
            db.session.commit()
        except Exception as ex:
            print(ex)
            db.session.rollback()
        return redirect(url_for('home.success'))

    return render_template("contact-us.html")


@home.route('/terms/', methods=["GET"])
# @cache.cached(timeout=40, key_prefix='terms')
def terms():
    return render_template("terms.html")

@home.route('/check-gold-price/', methods=["GET", "POST"])
def check_gold_price():
    states = State.query.all()
    today_date = datetime.today()
    prices = None
    if request.method == "POST":
        state_id = request.form.get('state_id', '')
        prices_24 = HindustanGoldPrice.query.order_by(HindustanGoldPrice.date.desc()).filter_by(state_id= state_id, carat="24").first()
        prices_22 = HindustanGoldPrice.query.order_by(HindustanGoldPrice.date.desc()).filter_by(state_id= state_id, carat="22").first()
        
                
        prices = {
                "prices_24" : prices_24.price if prices_24 else "call for price",
                "prices_22" : prices_22.price if prices_22 else "call for price",
            }
        
    return render_template("check_price.html", states = states, today_date=today_date, prices = prices)


@home.route('/branch-review/', methods=["GET"])
def branch_review():
    return render_template("branch_review.html")


    

@home.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=edge'
    response.headers['Cache-Control'] = 'public, max-age=10'
    return response

@home.route('/success/', methods=["GET"])
@cache.cached(timeout=40, key_prefix='terms')
def success():
    return render_template("success.html")

@home.route('/callform/', methods=["GET"])
@cache.cached(timeout=40, key_prefix='terms')
def callform():
    return render_template("callsuccess.html")
    

@home.route('/requestform/', methods=["GET"])
@cache.cached(timeout=40, key_prefix='terms')
def requestform():
    return render_template("requestsucess.html")




@home.route('/gold-buyers/', methods=["GET"])
def gold_buyers():
    return render_template("gold-buyers.html")