import json
from flask import Blueprint, render_template, request, redirect
from flask_login import login_required

from app import db
from . import paginate
from ...models import SeoMetaData, Branch

seo = Blueprint("seo", __name__)




in_blog = ['More Blogs', 'Spot Cash Gold Near Me', 'Jewellery Buyer Near Me', 'Cash For Gold Near Me',
            'Sell Gold Near Me', 'Selling Gold', 'simple Sell Gold','Release Pledged Gold Near me','Gold buyers near me',
            'Sell Gold for Cash', 'Money for Gold' , 'Gold Buyers in Bangalore', 'Gold Price Today',
            'Buy Gold', 'Sell Your Gold for Cash', 'Sell Your Gold', 'I went to Sell Gold',
            'Gold Online Rate','Value of Gold', 'Gold Biscuit', 'Gold Earnings with Price' ]
            
in_services = ['BEST GOLD', 'RELEASE PLEDGED GOLD', 'SELL GOLD', 'Doorstep GOLD Buyers', 
                'VALUE FOR GOLD', 'Check Gold Price']



def writ_to_json(meta_data, page, pagename, is_indivual_branch):
    if not is_indivual_branch:

        json_meta = json.load(open('app/data/meta_data.json'))
        json_meta["page"][page]['title'] = meta_data.title
        json_meta["page"][page]['keywords'] = meta_data.keywords
        json_meta["page"][page]['description'] = meta_data.description
        json.dump(json_meta, open('app/data/meta_data.json', 'w'), indent=4)
    else:
        page = page.lower()
        # newdata = {page :{'title': meta_data.title,
        #            'keywords': meta_data.keywords,
        #            'description': meta_data.description}
        # }

        data = {'title': meta_data.title,
                   'keywords': meta_data.keywords,
                   'description': meta_data.description}

        
        json_meta = json.load(open('app/data/meta_data.json'))
        json_meta[pagename][page] = data
        json.dump(json_meta, open('app/data/meta_data.json', 'w'), indent=4)

@seo.route('/admin/seo/create', methods=['GET', 'POST'])
@login_required
def create():
    branches = Branch.query.all()
    is_indivual_branch = False
    if request.method == "POST":
        pagename = page = request.form.get('page', '').strip()
        
        if page == "individual_branch":
            page = request.form.get('branch_page', '').strip()
            is_indivual_branch = True
        elif page == "individual_blog":
            page = request.form.get('blog_page', '').strip()
            is_indivual_branch = True
        elif page == "individual_services":
            page = request.form.get('service_page', '').strip()
            is_indivual_branch = True

        title = request.form.get('title', '').strip()
        keywords = request.form.get('keywords', '').strip()
        description = request.form.get('description', '').strip()
        meta_data = SeoMetaData(
            page=page,
            title=title,
            description=description,
            keywords=keywords
        )
        try:
            db.session.add(meta_data)
            db.session.commit()
        except Exception as ex:
            print(ex)
            db.session.rollback()
        writ_to_json(meta_data, page, pagename, is_indivual_branch=is_indivual_branch)
    list_of_meta = SeoMetaData.query.order_by(SeoMetaData.id.desc()).all()
    return render_template("backend/seo/create.html", list_of_meta=list_of_meta, branches=branches, in_services=in_services, in_blog=in_blog)


@seo.route('/admin/seo/edit/<int:id>', methods=["GET", "POST"])
@login_required
def edit(id):
    branches = Branch.query.all()
    is_indivual_branch = False
    edit_meta_data = SeoMetaData.query.get(id)
    if request.method == "POST":
        pagename = page = request.form.get('page', '').strip()
        if page == "individual_branch":
            page = request.form.get('branch_page', '').strip()
            is_indivual_branch = True
        elif page == "individual_blog":
            page = request.form.get('blog_page', '').strip()
            is_indivual_branch = True
        elif page == "individual_services":
            page = request.form.get('service_page', '').strip()
            is_indivual_branch = True
        edit_meta_data.page = page
        edit_meta_data.title = request.form.get('title', '').strip()
        edit_meta_data.keywords = request.form.get('keywords', '').strip()
        edit_meta_data.description = request.form.get(
            'description', '').strip()
        try:
            db.session.commit()
        except Exception as ex:
            print(ex)
            db.session.rollback()
        writ_to_json(edit_meta_data, edit_meta_data.page, pagename, is_indivual_branch)
    return render_template("backend/seo/edit.html", meta_data=edit_meta_data, branches=branches, in_services=in_services, in_blog=in_blog)


@seo.route('/admin/seo/list', methods=['GET'])
@login_required
def list():
    list_of_metas = SeoMetaData.query.order_by(SeoMetaData.id.desc())
    if request.args.get('page'):
        page = int(request.args.get('page'))
    else:
        page = 1
    list_of_metas = paginate(list_of_metas, page, 20)
    return render_template('backend/seo/list.html', list_of_contacts=list_of_metas)

@seo.route('/admin/seo/delete/<int:id>', methods=["GET", "POST"])
@login_required
def delete(id):
    delete_meta_data = SeoMetaData.query.get(id)
    print(delete_meta_data)
    db.session.delete(delete_meta_data)
    db.session.commit()
    return redirect('/admin/seo/list')


