from datetime import datetime
from flask import Blueprint, request, redirect, url_for, render_template
from flask_login import login_required

from ... import db
from ...models.locations import State, City

city = Blueprint('city', __name__)

@city.route('/admin/location/city/create/', methods=['GET', 'POST'])
@login_required
def create():
    cities = City.query.all()
    states = State.query.all()
    if request.method == "POST":
        city = City(name=request.form.get('city').strip(), state_id=request.form.get('state_id').strip())
        db.session.add(city)
        db.session.commit()
        return redirect(url_for('city.create'))
    return render_template('backend/location/city/create.html', cities = cities, states = states)


@city.route('/admin/location/state/city/<int:id>/', methods=['GET', 'POST'])
@login_required
def edit(id):
    city = City.query.get_or_404(id)
    states = State.query.all()
    if request.method == "POST":
        city.state_id = request.form['state_id']
        city.name = request.form['city']
        db.session.commit()
        return redirect(url_for('city.create'))
    return render_template('backend/location/city/edit.html', city=city, states=states)



@city.route('/admin/location/state/index/', methods=['GET'])
@login_required
def index():
    return render_template('backend/locations/index.html')
