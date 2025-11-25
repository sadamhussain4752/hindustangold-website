import email
import os
from flask import Flask, render_template, request, jsonify

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_caching import Cache
from flask_migrate import Migrate

import logging
from flask_minify import minify



cache = Cache(config={'CACHE_TYPE': 'SimpleCache', "CACHE_THRESHOLD": 50})

app  = Flask(__name__)
minify(app=app, html=True, js=True, cssless=False)
app.config.from_pyfile("settings.py")

#DATABASE CREDENTIONAS
print(app.config.get("ENVIRONMENT"))

if app.config.get("ENVIRONMENT") == 'development':    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hindustangold.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'True'
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static/upload')
    app.config['CACHE_DIR'] = '/tmp/my_site_cache/' 
    app.config['CACHE_TYPE'] = 'FileSystemCache' 
    app.config['CACHE_THRESHOLD'] = 10000
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 300

    if not os.path.exists(os.path.join(app.root_path, 'static/resumes')):
        os.makedirs(os.path.join(app.root_path, 'static/resumes'))

    app.config['RESUME_FOLDER'] = os.path.join(app.root_path, 'static/resumes')
    db = SQLAlchemy(app)   
    app.secret_key = app.config.get("SECRET_KEY")
    login_manager = LoginManager()
    login_manager.init_app(app)
    
    # from app.models.goldprice import *
    # from app.models.user import *
    # from app.models.contactus import *
    # from app.models.locations import * 
    # from app.models.branches import *
    from app.models import *
    app.app_context().push()
    db.session.flush()
    db.create_all()

    cache.init_app(app)
    migrate = Migrate(app, db)

    # admin_user = User(email="rathod@gmail.com", password="8861")
    # db.session.add(admin_user)
    # db.session.commit()

elif app.config.get("ENVIRONMENT") == 'production':
    DATABASE = 'hindustan_production'
    USERNAME = 'hindustan_web_admin'
    PASSWORD = 'gmJAH9dM99f!123'
    SERVER = '0.0.0.0'
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://{}:{}@{}:3306/{}".format(USERNAME, PASSWORD, SERVER, DATABASE)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'True'
    app.config['CACHE_DIR'] = '/tmp/my_site_cache/' 
    app.config['CACHE_TYPE'] = 'FileSystemCache' 
    app.config['CACHE_THRESHOLD'] = 10000
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 300
    
    if not os.path.exists(os.path.join(app.root_path, 'static/upload')):
        os.makedirs(os.path.join(app.root_path, 'static/upload'))

    if not os.path.exists(os.path.join(app.root_path, 'static/resumes')):
        os.makedirs(os.path.join(app.root_path, 'static/resumes'))

    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static/upload')
    app.config['RESUME_FOLDER'] = os.path.join(app.root_path, 'static/resumes')
    db = SQLAlchemy(app)
    app.secret_key = app.config.get("SECRET_KEY")
    login_manager = LoginManager()
    login_manager.init_app(app)
    # from app.models.goldprice import *
    # from app.models.user import *
    # from app.models.contactus import *
    # from app.models.locations import * 
    # from app.models.branches import *
    from app.models import *
    app.app_context().push()
    db.session.flush()
    db.create_all()
    
    cache.init_app(app)
    migrate = Migrate(app, db)
else:
    print("Please set environmentkey in .env")
    import sys
    sys.exit(1)




@app.errorhandler(404)
def not_found(e):
  return render_template('common/error.html'), 404



# @app.after_request
# def add_header(response):
#     """
#     Add headers to both force latest IE rendering engine or Chrome Frame,
#     and also to cache the rendered page for 10 minutes.
#     """
#     response.headers['X-UA-Compatible'] = 'IE=edge'
#     response.headers['Cache-Control'] = 'public, max-age=0'
#     return response

all_meta_data = None
global_states_data = None


import json
@app.context_processor
def inject_meta():
    global global_states_data
    global all_meta_data
    if not global_states_data:                 
        states = State.query.all()
        json_states = jsonify(states)
        global_states_data = json_states.json

    if app.config.get("ENVIRONMENT") == 'development':
        meta_data_file = 'app/data/meta_data_dev.json'
    else:
        meta_data_file = 'app/data/meta_data.json'
    

    if not all_meta_data:        
        with open(meta_data_file) as json_file:
            all_meta_data = json.load(json_file)
   
    endpoint = request.endpoint
    cur_url = request.url 

    
    try:            
        if endpoint == 'branches.searched_branch':
            branch = request.path.strip().replace('?', '').strip().split('/')[2]
            branch_name = branch.replace('-', ' ').strip()
            return dict(meta_data=all_meta_data['individual_branch'][branch_name], states = global_states_data, cur_url = cur_url)

        elif endpoint == 'blogs.selected_blog':
            blog = request.path.strip().replace('?', '').strip().split('/')[2]
            blog_name = blog.replace('-', ' ').strip()
            return dict(meta_data=all_meta_data['individual_blog'][blog_name],states = global_states_data, cur_url = cur_url)

        elif endpoint == 'services.selected_service':
            service = request.path.strip().replace('?', '').strip().split('/')[2]
            service_name = service.replace('-', ' ').strip()
            return dict(meta_data=all_meta_data['individual_services'][service_name],states = global_states_data, cur_url = cur_url)
   
    except Exception as e:
        logging.error(e)
        pass       
        
    
    if endpoint == 'branches.our_branches' or endpoint == 'branches.searched_branch':
        return dict(meta_data=all_meta_data['page']['branches'],states = global_states_data, cur_url = cur_url)
   

    elif endpoint == 'home.contact_us':
        return dict(meta_data=all_meta_data['page']['contact_us'],states = global_states_data, cur_url = cur_url)
    
    elif endpoint == 'home.about_us':
        return dict(meta_data=all_meta_data['page']['about_us'],states = global_states_data, cur_url = cur_url)
    
    elif endpoint == 'home.index':
        return dict(meta_data=all_meta_data['page']['home'],states = global_states_data, cur_url = cur_url)

    elif endpoint == 'home.terms':
        return dict(meta_data=all_meta_data['page']['terms'],states = global_states_data, cur_url = cur_url)
    elif endpoint == 'home.gold_buyers':
        return dict(meta_data=all_meta_data['page']['gold_buyers'],states = global_states_data, cur_url = cur_url)
    
    elif endpoint == 'home.check_gold_price':
        return dict(meta_data=all_meta_data['page']['check_gold_price'],states = global_states_data, cur_url = cur_url)

    elif endpoint == 'branches_pages.careers':
        return dict(meta_data=all_meta_data['page']['careers'],states = global_states_data, cur_url = cur_url)

    elif endpoint == 'branches_pages.appy_careers':
        return dict(meta_data=all_meta_data['page']['appy_careers'],states = global_states_data, cur_url = cur_url)

            
    elif endpoint == 'services.our_service':
        return dict(meta_data=all_meta_data['page']['services'],states = global_states_data, cur_url = cur_url)
    
    elif endpoint == 'blogs.blogs':
        return dict(meta_data=all_meta_data['page']['blog'], states = global_states_data, cur_url = cur_url)

    elif endpoint == 'blogs.more_blogs':
        return dict(meta_data=all_meta_data['individual_blog']['more blogs'],states = global_states_data, cur_url = cur_url)
    
    else:
        return dict(meta_data={}, states = global_states_data, cur_url = cur_url)

@app.template_filter()
def format_branch_url(value):
    
    if value: value = value.replace(' ', '-').lower()
    
    return value
