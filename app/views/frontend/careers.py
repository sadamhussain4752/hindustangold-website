import os

from flask import(
    jsonify,
    render_template,
    request,
    redirect,
    url_for,
    Blueprint
)
from app import app
from ...models.contactus import Career, CareerPosition
from ... import cache, db

career_pages = Blueprint("branches_pages", __name__)


@career_pages.route('/careers/', methods=["GET"])
@cache.cached(timeout=40, key_prefix='careers')
def careers():
    careers = CareerPosition.query.all()
    return render_template("careers.html", careers=careers)


@career_pages.route('/apply-careers/<string:position>/', methods=["GET", "POST"])
def appy_careers(position):
    if request.method == "POST":
        full_name = request.form.get('name', '')
        email = request.form.get('email', '')
        phone_no = request.form.get('phone', '')
        cover_letter = request.form.get('cover_letter', '')
        resume_file = request.files.get('resume')
        #path = os.path.join("static/upload", resume_file.filename)
        file_name = full_name + "-" + resume_file.filename
        resume_file.save(os.path.join(app.config['RESUME_FOLDER'], file_name))
        career = Career(
            full_name=full_name,
            email=email,
            phone_no=phone_no,
            resume=file_name,
            cover_letter=cover_letter,
            position=position

        )
        db.session.add(career)
        try:
            db.session.commit()
        except Exception as ex:
            print(ex)
            db.session.rollback()
        return render_template("thank_you.html")
    return render_template("apply_careers.html", position=position)

