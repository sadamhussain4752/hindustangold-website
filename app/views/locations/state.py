from datetime import datetime
from functools import update_wrapper
from flask import Blueprint, request, redirect, url_for, render_template, make_response
from flask_login import login_required

from ... import db, cache
from ...models.locations import State, City

state = Blueprint('state', __name__)
def no_cache(f):
    def new_func(*args, **kwargs):
        resp = make_response(f(*args, **kwargs))
        resp.cache_control.no_cache = True
        return resp
    return update_wrapper(new_func, f)

@state.route('/admin/location/state/index/', methods=['GET'])
@login_required
def index():
    return render_template('backend/locations/index.html')

@state.route('/admin/location/state/create/', methods=['GET', 'POST'])
@login_required
@no_cache
def create():    
    if request.method == "POST":
        state = State(name=request.form.get('state'))
        db.session.add(state)
        db.session.commit()
        
        #return redirect(url_for('state.create'))
    states = State.query.order_by(State.id).all()
    print("Lenght of states {}".format(len(states)))
    return render_template('backend/location/state/create.html', states = states)


@state.route('/admin/location/state/edit/<int:id>/', methods=['GET', 'POST'])
@login_required
def edit(id):
    state = State.query.get_or_404(id)
    if request.method == "POST":
        state.name = request.form['state']
        db.session.commit()
        return redirect(url_for('state.create'))
    return render_template('backend/location/state/edit.html', state=state)

@state.route('/admin/location/state/delete/<int:id>/', methods=['GET'])
@login_required
def delete(id):
    state = State.query.get_or_404(id)   
    db.session.delete(state)
    db.session.commit()
    return redirect(url_for("state.create"))
    
