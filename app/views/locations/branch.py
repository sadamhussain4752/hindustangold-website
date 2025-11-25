from datetime import datetime
import json
from collections import OrderedDict
import os
from flask import Blueprint, request, redirect, url_for, render_template
from flask_login import login_required
from werkzeug.utils import secure_filename

from ... import db
from ...models.locations import State, City
from ...models.branches import Branch, BranchRelation, BranchImages
from app import app
from ..backend.customers import paginate
branch = Blueprint('branch', __name__)

def city_to_json(city):
    return {
        'id': city.id,
        #'state_id': city.state_id,
        'name': city.name,
   #     'state': city.state.name
    }

@branch.route('/admin/location/branch/datatable/', methods=['GET', 'POST'])
@login_required
def datatable():
    branches = BranchRelation.query.order_by(BranchRelation.id.desc()).limit(50)
    if request.args.get('page'):
        page = int(request.args.get('page'))
    else :
        page = 1
    branches = paginate(branches, page, 50)
    return render_template("backend/datatables/branches_datatable.html", branches = branches)

@branch.route('/admin/location/branch/create/', methods=['GET', 'POST'])
@login_required
def create():
    cities = City.query.all()
    states = State.query.all()
    # branchs = Branch.query.all()
    # branch_relations = BranchRelation.query.all()
    # state_ids = [city.state_id for city in cities]
    cities_list = OrderedDict()
    for city in cities:
        if city.state_id in cities_list:
            cities_list[city.state_id].append({ "id" : city.id, "name" : city.name})
        else:
            cities_list[city.state_id] = [{ "id" : city.id, "name" : city.name}]


        
    
    if request.method == "POST":
        name = request.form.get('name').strip()       
        files  =request.files.getlist('files[]')       
        file_names = []
        for file in files:
            new_file_name = "hindustangold-branch-" + name + "-" + secure_filename(file.filename)[secure_filename(file.filename).index('.'):]
            relative_path = os.path.join("static/upload", new_file_name)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_file_name))
            file_names.append((new_file_name, relative_path))

        map_location_image = request.files.get('map_location')        
        map_new_file_name = "hindustangold-branch-map-location-" + name + "-" + secure_filename(map_location_image.filename)[secure_filename(map_location_image.filename).index('.'):]
        map_relative_path = os.path.join("static/upload", map_new_file_name)
        map_location_image.save(os.path.join(app.config['UPLOAD_FOLDER'], map_new_file_name))

        email = request.form.get('email').strip()
        contact_no = request.form.get('contact_no').strip()
        address = request.form.get('address').strip()
        pincode = request.form.get('pincode').strip()
        city_id = request.form.get('city_id')
        state_id = request.form.get('state_id')
        gmap_location = request.form.get('gmap_location').strip()
        description = request.form.get('description').strip()
        # title = request.form.get('title').strip()
        # metadescription = request.form.get('metadescription').strip()
        # metakeywords = request.form.get('metakeywords').strip()
        
        branch = Branch(name=name, email=email, contact_no=contact_no,
                        address=address, pincode=pincode, gmap_link=gmap_location,
                        description=description)
        db.session.add(branch)
        try:
            db.session.commit()
        except Exception as ex:
            print(ex)
            db.session.rollback()

        branch_relation = BranchRelation(branch_id=branch.id, city_id=city_id, state_id=state_id)
        db.session.add(branch_relation)
        try:
            db.session.commit()
        except Exception as ex:
            print(ex)
            db.session.rollback()
            
        for file_name, relative_path in file_names:
            branch_image = BranchImages(branch_id=branch_relation.id, image=file_name, image_path=relative_path, tag="main_images")
            db.session.add(branch_image)
        map_branch_image = BranchImages(branch_id=branch_relation.id, image=map_new_file_name, image_path=map_relative_path, tag="map_images")
        db.session.add(map_branch_image)
        try:
            db.session.commit()
        except Exception as ex:
            print(ex)
            db.session.rollback()
        
        return redirect(url_for('branch.create'))
    return render_template('backend/location/branch/create.html', cities = cities,
                                                                  states = states,
                                                               #   branches = branchs,
                                                                 # branch_relations = branch_relations,
                                                                  cities_list = json.dumps(cities_list))
@branch.route('/admin/location/branch/edit/<id>/', methods=['GET', 'POST'])
@login_required
def edit(id):
    cities = City.query.all()
    states = State.query.all()
    cities_list = OrderedDict()
    for city in cities:
        if city.state_id in cities_list:
            cities_list[city.state_id].append({ "id" : city.id, "name" : city.name})
        else:
            cities_list[city.state_id] = [{ "id" : city.id, "name" : city.name}]
    if request.method == "GET":
        branch = BranchRelation.query.get(id)
        return render_template("backend/location/branch/edit.html", 
                                    branch=branch,
                                    states=states,
                                    cities = cities,
                                      cities_list = json.dumps(cities_list))
    
    if request.method == "POST":
        branch = BranchRelation.query.get(id)
        branch.state_id = request.form['state_id']
        branch.city_id = request.form['city_id']
        branch.branch.pincode = request.form['pincode'].strip()
        branch.branch.address = request.form['address'].strip()
        branch.branch.contact_no = request.form['contact_no']
        branch.branch.email = request.form['email'].strip()
        branch.branch.gmap_link = request.form['gmap_location']
        name = request.form.get('name').strip()   
        branch.branch.description = request.form.get('description').strip()
        # branch.branch.title = request.form.get('title').strip()
        # branch.branch.metadescription = request.form.get('metadescription').strip()
        # branch.branch.metakeywords = request.form.get('metakeywords').strip()
        branch.branch.name = name
        file  =request.files.get('files', '')  
        
        if file.filename != '' :                
            new_file_name = "hindustangold-branch-" + name + "-" + secure_filename(file.filename)[secure_filename(file.filename).index('.'):]
            relative_path = os.path.join("static/upload", new_file_name)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_file_name))
            branch.imags[0].image_path = relative_path
            branch.imags[0].image = new_file_name
            
        map_location_image = request.files.get('map_location', '')
        if map_location_image.filename != '':
            map_new_file_name = "hindustangold-branch-map-location-" + name + "-" + secure_filename(map_location_image.filename)[secure_filename(map_location_image.filename).index('.'):]
            map_relative_path = os.path.join("static/upload", map_new_file_name)
            map_location_image.save(os.path.join(app.config['UPLOAD_FOLDER'], map_new_file_name))
            branch.imags[1].image = map_new_file_name
            branch.imags[1].image_path = map_relative_path
        db.session.commit()
    branch = BranchRelation.query.get(id)
    return render_template("backend/location/branch/edit.html",  branch=branch,
                                    states=states,
                                    cities = cities,
                                    cities_list = json.dumps(cities_list))



@branch.route('/admin/location/branch/delete/<id>/', methods=['GET', 'POST'])
@login_required
def delete(id):
    branch = BranchRelation.query.get(id)
    main_branch = Branch.query.filter_by(id=branch.id).first()
    skill_obj = BranchImages.query.filter_by(branch_id=branch.id).all()
    for skills in skill_obj:
        db.session.delete(skills)
    db.session.delete(main_branch)
    db.session.delete(branch)
    db.session.commit()
    return render_template("success.html")