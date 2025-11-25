from app import db 
from flask import  Blueprint, render_template, request, redirect, url_for
from flask_login import  login_required
from ...models import CareerPosition, CareerPositionReltation, BranchRelation
from . import  paginate

careers = Blueprint("careers", __name__)

@careers.route('/admin/career/create', methods=["GET", "POST"])
@login_required
def create():
    branches = BranchRelation.query.all()
    if request.method == "POST":
        branch_id = request.form.get('branch_id', '').strip()
        name = request.form.get('name', '').strip()
        salary = request.form.get('salary', '').strip()        
        experience = request.form.get('experience', '').strip()
        qualifications = request.form.get('qualifications', '').strip()
        job_type = request.form.get('job_type', '').strip()
        job_timings = request.form.get('job_timings', '').strip()
        contact_no = request.form.get('contact_no', '').strip()
        contact_email = request.form.get('contact_email', '').strip()
        skills = request.form.get('skills', '').strip().split()
        career = CareerPosition(
            name=name,
            branch_id=branch_id,
            salary=salary,
            experience=experience,
            qualifications=qualifications,
            job_type=job_type,
            job_timings=job_timings,
            contact_no=contact_no,
            contact_email=contact_email,            
        )
        try:
            db.session.add(career)
            db.session.commit()
            for skill in skills:                    
                skill_obj = CareerPositionReltation(
                    career_position_id=career.id,
                    skill=skill
                )
                db.session.add(skill_obj)
                db.session.commit()
        except Exception as ex:
            db.session.rollback()
            print(ex)
            
    return render_template("backend/careers/create.html", branches=branches)

@careers.route('/admin/career/list', methods=["GET"])
@login_required
def list():
    list_of_careers = CareerPosition.query.order_by(CareerPosition.id)
    if request.args.get('page'):
        page = int(request.args.get('page'))
    else :
        page = 1
    list_of_careers = paginate(list_of_careers, page, 20)    
    return render_template('backend/careers/list.html', list_of_contacts = list_of_careers)




@careers.route('/admin/career/edit-vacancies/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    branches = BranchRelation.query.all()
    vacancy_detail = CareerPosition.query.get(id)
    career_relation = vacancy_detail.postion_relation
    if request.method == "POST":
        branch_id = request.form.get('branch_id', '').strip()
        name = request.form.get('name', '').strip()
        salary = request.form.get('salary', '').strip()        
        experience = request.form.get('experience', '').strip()
        qualifications = request.form.get('qualifications', '').strip()
        job_type = request.form.get('job_type', '').strip()
        job_timings = request.form.get('job_timings', '').strip()
        contact_no = request.form.get('contact_no', '').strip()
        contact_email = request.form.get('contact_email', '').strip()
        skills = request.form.get('skills', '').strip().split()    
        
        vacancy_detail.branch = branch_id
        vacancy_detail.name = name
        vacancy_detail.experience = experience
        vacancy_detail.qualifications = qualifications
        vacancy_detail.salary = salary
        vacancy_detail.job_type = job_type
        vacancy_detail.job_timings = job_timings       
        vacancy_detail.contact_no = contact_no
        vacancy_detail.contact_email = contact_email 


        vacancy_skill = CareerPositionReltation.query.filter_by(career_position_id=id).all()
        for v_skills in vacancy_skill:
                db.session.delete(v_skills)

        for skill in skills:                    
                skill_obj = CareerPositionReltation(
                    career_position_id=id,
                    skill=skill
                )
                db.session.add(skill_obj)


       
        db.session.commit()
        return redirect('/admin/career/list')
    return render_template("backend/careers/edit.html", vacancy_detail = vacancy_detail, branches = branches, career_relation= career_relation)


@careers.route('/admin/career/delete-vacancies/<int:id>', methods=['GET', 'POST'])
def delete(id):
    careerposition = CareerPosition.query.filter_by(id=id).first()
    skill_obj = CareerPositionReltation.query.filter_by(career_position_id=id).all()
    
    if request.method == 'POST':
        if careerposition:
            db.session.delete(careerposition)
            for skills in skill_obj:
                db.session.delete(skills)
            
            
            db.session.commit()
            return redirect('/admin/career/create')
        else:
            return "note deleted"
    return render_template("backend/careers/delete.html")








    


