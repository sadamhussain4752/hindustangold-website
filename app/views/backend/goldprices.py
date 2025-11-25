from datetime import datetime
import json
from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import login_required

from ... import app, db
from ...models.user import User
from ...models.goldprice import GoldPrice, HindustanGoldPrice
from ...models.locations import State
from .customers import paginate
gold_prices = Blueprint('gold_prices', __name__)

####################  Add gold prices ####################

def exception_handler(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        return str(e)


@gold_prices.route('/admin/add-gold-prices', methods=['GET', 'POST'])
@login_required
def create():
    states = State.query.all()
    if request.method == "POST":
        price = request.form.get('gold_price').strip()
        carat = request.form.get('karat_list')
        location = request.form.get('state')
        date = datetime.today()        
        try:                
            gold_cal = HindustanGoldPrice(price=price, date=date, state_id=location, carat=carat)
            db.session.add(gold_cal)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(e)             
    list_of_today_price = HindustanGoldPrice.query.order_by(HindustanGoldPrice.date).filter_by(date=datetime.today().strftime('%Y-%m-%d'))
    return render_template("backend/gold_prices/create.html",
                                 gold_prices=list_of_today_price,
                                 states = states)

@gold_prices.route('/admin/edit-gold-prices/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    states = State.query.all()
    gold_price = HindustanGoldPrice.query.get(id)
    if request.method == "POST":
        price = request.form.get('gold_price').strip()
        carat = request.form.get('karat_list')
        location = request.form.get('state')
        
        gold_price.price = price
        gold_price.carat = carat
        gold_price.state_id = location        
        db.session.commit()
        return render_template("backend/gold_prices/edit.html", gold_price=gold_price, states = states)
    return render_template("backend/gold_prices/edit.html", gold_price=gold_price, states = states)

@gold_prices.route('/admin/list-gold-prices', methods=['GET', 'POST'])
@login_required
def list():
    states = State.query.all()
    if request.args.get('page'):
        page = int(request.args.get('page'))
    else :
        page = 1
    
    if request.method == "POST":
        state = request.form.get('state')
        carat = request.form.get('karat_list')
        date = request.form.get('date')
        list_of_today_price = HindustanGoldPrice.query.filter_by(state_id = state, carat=carat, date=date)#.all()
        list_of_today_price = paginate(list_of_today_price, page, 20)    
        return render_template('backend/gold_prices/list.html',  gold_prices=list_of_today_price,states = states)

    list_of_today_price = HindustanGoldPrice.query.order_by(HindustanGoldPrice.date.desc())#.filter_by(date=datetime.today().strftime('%Y-%m-%d'))    
    list_of_today_price = paginate(list_of_today_price, page, 20)    
    return render_template('backend/gold_prices/list.html',  gold_prices=list_of_today_price, states = states)

