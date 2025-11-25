from datetime import datetime
from pytz import timezone
from .. import db
from sqlalchemy.orm import relationship

STATUS = {
    "1" : 'Requested',
    "2" : 'Processing',
    "3" : 'Completed',
    "4" : 'Pending',    
}

class ContactUs(db.Model):
    __tablename__ = "contact_us"
    id = db.Column(db.Integer(), primary_key=True)
    full_name = db.Column(db.String(100), unique=False, nullable=True) 
    email = db.Column(db.String(100), unique=False, nullable=True) 
    phone_number = db.Column(db.String(50), unique=False, nullable=True) 
    subject = db.Column(db.String(50), unique=False, nullable=True) 
    message = db.Column(db.String(500), unique=False, nullable=True) 
    status = db.Column(db.Integer(), nullable=True)
    date = db.Column(db.DateTime(timezone=True))
    def __init__(self, full_name, email, phone_number, subject, message, status) -> None:
        self.full_name = full_name
        self.email = email
        self.phone_number = phone_number
        self.subject = subject
        self.message = message
        self.status = status
        self.date = datetime.now(timezone("Asia/Kolkata"))


class RequestCallBack(db.Model):
    __tablename__ = "request_callback"
    id = db.Column(db.Integer(), primary_key=True)
    full_name = db.Column(db.String(100), unique=False, nullable=True)
    phone_number = db.Column(db.String(50), unique=False, nullable=True)
    selectoption = db.Column(db.String(50), unique=False, nullable=True)
    status = db.Column(db.Integer(), nullable=True)
    date = db.Column(db.DateTime(timezone=True))

    def __init__(self, full_name, phone_number,selectoption, status) -> None:
        self.full_name = full_name
        self.phone_number = phone_number
        self.selectoption = selectoption
        self.date = datetime.now(timezone("Asia/Kolkata"))
        self.status = status

class Career(db.Model):
    __tablename__ = "career"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    position = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    phone_no = db.Column(db.String(50), nullable=True)
    resume = db.Column(db.String(100), nullable=True)
    cover_letter = db.Column(db.String(1000), nullable=True)
    date = db.Column(db.DateTime(timezone=True))
    status = db.Column(db.Integer(), nullable=True)

    def __init__(self, full_name, email, phone_no, resume, cover_letter, position, status=1) -> None:
          self.name = full_name
          self.email = email
          self.phone_no = phone_no
          self.resume = resume
          self.cover_letter = cover_letter
          self.position = position
          self.status = status
          self.date = datetime.now(timezone("Asia/Kolkata"))


class CareerPosition(db.Model):
    __tablename__ = "careerposition"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    branch_id = db.Column(db.Integer(), db.ForeignKey('branchrelation.id'), nullable=False)
    qualifications = db.Column(db.String(100), nullable=True)
    experience = db.Column(db.String(50), nullable=True)
    job_type = db.Column(db.String(50), nullable=True)
    job_timings = db.Column(db.String(50), nullable=True)
    contact_no = db.Column(db.String(50), nullable=True)
    contact_email = db.Column(db.String(50), nullable=True)
    salary = db.Column(db.String(50), nullable=True)    
    date = db.Column(db.DateTime(timezone=True))

    postion_relation = relationship("CareerPositionReltation", backref="branchrelation")
    def __init__(self, name, branch_id, qualifications, experience, job_type, job_timings, contact_no, contact_email, salary) -> None:
          self.name = name
          self.branch_id = branch_id
          self.qualifications = qualifications
          self.experience = experience
          self.job_type = job_type
          self.job_timings = job_timings
          self.contact_no = contact_no
          self.contact_email = contact_email
          self.salary = salary          
          self.date = datetime.now()

class CareerPositionReltation(db.Model):
    __tablename__ = "careerpostionrelation"
    id = db.Column(db.Integer, primary_key=True)
    career_position_id = db.Column(db.Integer(), db.ForeignKey('careerposition.id'), nullable=False)
    skill = db.Column(db.String(100), nullable=True)

    def __init__(self, career_position_id, skill) -> None:
        self.career_position_id = career_position_id
        self.skill = skill
        
class VerifiedPhone(db.Model):
    __tablename__ = "verified_phone"
    id = db.Column(db.Integer(), primary_key=True)
    phone_number = db.Column(db.String(50), unique=False, nullable=True)
    is_phone_verified = db.Column(db.Boolean, default=False, nullable=False)
    def __init__(self, phone_number, is_phone_verified) -> None:
        self.phone_number = phone_number
        self.is_phone_verified = is_phone_verified
        