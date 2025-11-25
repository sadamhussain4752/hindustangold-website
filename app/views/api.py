
from datetime import datetime

from app import global_states_data
from app.models import State
from app.views.index import home
from app.views.utils.frontend import indian_formatted_currency
from flask import Blueprint, jsonify, request,render_template

from .. import cache, db
from ..models.goldprice import HindustanGoldPrice, UserGoldPrice
from ..models.contactus import RequestCallBack

api = Blueprint('api', __name__)

@api.route('/api/get-city/', methods=['POST'])
def api_get_city():
    global global_states_data
    state_id = request.form.get('state_id')    
    if not global_states_data:
        states = State.query.all()
        global_states_data = states
        json_states = jsonify(states)
        global_states_data = json_states.json    
    cities = [ state for state in global_states_data if state['id'] == int(state_id)][0]['city']
    return jsonify(cities)


@home.route('/get-goldprice/', methods=["POST"])
@cache.cached(timeout=40, key_prefix='get_goldprice')
def get_today_goldprice():
    customer_name = request.args.get('customer_name')
    state_city = request.args.get('state_city')
    mobile_no = request.args.get('mobile_no')
    gross_weight = request.args.get('gross_weight')
    stones_weight = request.args.get('stones_weight')
    net_weight_in_grams = request.args.get('net_weight_in_grams')
    carat = request.args.get('karat_list')

    today_date = datetime.today().strftime('%Y-%m-%d')    
    current_gold_price = None

    gold_price = HindustanGoldPrice.query.filter_by(date = today_date, carat=carat, state_id=state_city).first()
    if not gold_price:
        gold_price = HindustanGoldPrice.query.order_by(HindustanGoldPrice.id.desc()).filter_by(carat=carat).first()
    json_gold_price = jsonify(gold_price).json        
    current_gold_price = json_gold_price    
    
    if current_gold_price:
        carat_price = current_gold_price["price"]
        total_weight = float( gross_weight) - float(stones_weight)
        
        # TODO: Reset this part later
        carat_price =carat_price.replace(',', '')
        total_price = float(carat_price) * float(total_weight)
        total_price = round(total_price, 2)
        enquiry_user = UserGoldPrice(
            name=customer_name,
            mobile_no=mobile_no,
            gross_weight=gross_weight,
            stone_weight=stones_weight,
            net_weight=total_weight,
            state_id=state_city,
            carat=carat,
            date=datetime.now(),
            price=total_price,
            status=1
        )

        db.session.add(enquiry_user)
        db.session.commit()

        return jsonify({
            'status': 200,
            'message': 'Gold price fetched successfully',
            'price': total_price,
        })
        
    else:
        return jsonify({
            'status': 400,
            'message': 'Gold price not found',
             'price': "Call for price",
        })

# TODO : Handle exceptions
@home.route('/request-callback-form/', methods=['POST'])
def request_callback():
    full_name = request.form.get('full_name')
    phone_number =request.form.get('phone_number')
    selectoption = request.form.get('selectoption')
    callback = RequestCallBack(
        full_name = full_name,
        phone_number = phone_number,
        selectoption = selectoption,
        status=1, #1 means requested
    )
    try:
        db.session.add(callback)
        db.session.commit()
        return render_template("requestsucess.html")
    except Exception as ex:
        print(ex)
        db.session.rollback()
        return jsonify({
            'status': 400,
            'message': 'Callback User not saved'
        })
# TODO : Handle exceptions
@home.route('/request-callback-sidebar/', methods=['POST'])
def request_callback_sidebar():
    full_name = request.form.get('full_no')
    phone_number =request.form.get('phone_num')
    print(full_name,phone_number)
    callback = RequestCallBack(
        full_name = full_name,
        phone_number = phone_number,
        selectoption = "",
        status=1, #1 means requested
    )
    try:

        db.session.add(callback)
        db.session.commit()
        return jsonify({
            'status': 200,
            'message': 'Callback User Saved successfully'
        })
    except Exception as ex:
        print(ex)
        db.session.rollback()
        return jsonify({
            'status': 400,
            'message': 'Callback User not saved'
        })
