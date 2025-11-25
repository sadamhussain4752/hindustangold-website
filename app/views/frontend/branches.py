from flask import(
    jsonify,
    render_template,
    request,
    redirect,
    url_for,
    Blueprint
)

from app.views.index import home
from ... import cache, db

from app.models.branches import Branch
from app.models import BranchRelation, BranchReview, State

branch_pages = Blueprint("branches", __name__)

global_states_data = None

@branch_pages.route('/branches/<state_id>/<city_id>/', methods=["GET", "POST"])
@cache.cached(timeout=5, key_prefix='filtered_branches')
def filtered_branches(state_id, city_id):
    global global_states_data
    if not global_states_data:
        states = State.query.all()
        json_states = jsonify(states)
        global_states_data = json_states.json
    
    branches = BranchRelation.query.order_by(
            BranchRelation.id.desc()).filter_by(city_id=city_id, state_id=state_id)
    return render_template("our-branches.html", states=global_states_data, branches=branches)

@branch_pages.route('/branches/', methods=["GET", "POST"])
@cache.cached(timeout=5, key_prefix='branches')
def our_branches():
    global global_states_data

    if not global_states_data:
        states = State.query.all()
        json_states = jsonify(states)
        global_states_data = json_states.json

    if request.method == "GET":
        branches = BranchRelation.query.order_by(
            BranchRelation.id.desc()).limit(10).all()

    if request.method == "POST":
        state_id = request.form.get('state')
        city_id = request.form.get('branches_locactions')
        # branches = BranchRelation.query.order_by(
        #     BranchRelation.id.desc()).filter_by(city_id=city_id, state_id=state_id)
        return redirect(url_for("branches.filtered_branches", state_id=state_id, city_id=city_id))
    return render_template("our-branches.html", states=global_states_data, branches=branches)



@branch_pages.route('/branches/<branch_id>/', methods=["GET", "POST"])
# @cache.cached(timeout=40, key_prefix='searched_branch')
def searched_branch(branch_id):
    full_branch_name = branch_id.replace('-', ' ').strip()
    branch_name = full_branch_name.replace("hindustan gold company", "").strip()
    branch_place = branch_name.replace("hindustan gold company", "").strip()
    if len(branch_place.split()) == 2:
        branch_str = branch_place.split()
        title_branch = branch_str[0].upper() +" "+ branch_str[1].capitalize()
    else:  
        title_branch = branch_place.capitalize()
    bangalore_place = ['vijayanagar','peenya','tc palya','kengeri','rt nagar','yelahanka','jp nagar','bommanahalli','yeswanthpur','gandhi bazar']
   # branch_name = ' '.join(ele.capitalize() for ele in branch_name.split())
    selected_br = Branch.query.filter(Branch.name.like(branch_name)).first()
    selected_branch = selected_br.branchrelation[0]
    images = selected_branch.imags

    if branch_place.lower() in bangalore_place:
        location = "bangalore"
    else:
        location = selected_branch.state.name
    
    for image in images:
        if image.tag == "main_images":
            image_path = image.image_path
            break
        else:
            image_path = None

    if request.method == "POST":
        username = request.form.get('username')
        email = request.form.get('email')
        contact_no = request.form.get('contact_no')

        rating = request.form.get("rating")
        review = request.form.get('review')
        branch_review = BranchReview(branch_id=selected_branch.id, user_name=username, user_email=email,
                                     user_contact_no=contact_no, rating=rating,
                                     review=review)
        db.session.add(branch_review)
        db.session.commit()
        return render_template("review-success.html")
    reviews = BranchReview.query.filter_by(branch_id=selected_branch.id)[:5]
    return render_template("branch_review.html",
                           selected_branch=selected_branch,
                           branch_img=image_path,
                           reviews=reviews, title_branch=title_branch, location=location)


@branch_pages.route('/nearest-branches/', methods=["GET"])
@cache.cached(timeout=40, key_prefix='nearest-branches')
def nearest_branches():
    return render_template("our-branches.html")
