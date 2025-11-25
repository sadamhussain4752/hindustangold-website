
from datetime import datetime, timezone
from .. import db
from .locations import State, City
from sqlalchemy.orm import relationship

class BranchRelation(db.Model):

    __tablename__ = "branchrelation"

    id = db.Column(db.Integer(), primary_key=True)
    branch_id = db.Column(db.Integer(), db.ForeignKey('branch.id'), nullable=False)
    city_id = db.Column(db.Integer(), db.ForeignKey('city.id'), nullable=False)
    state_id = db.Column(db.Integer(), db.ForeignKey('state.id'), nullable=False)
    date = db.Column(db.DateTime(timezone=False), nullable=True)
    city = relationship("City", backref="branchrelation")
    state = relationship("State", backref="branchrelation")
    branch = relationship("Branch", backref="branchrelation")
    imags = relationship("BranchImages", backref="branchrelation")
    reviews = relationship("BranchReview", backref="branchrelation")
    career_postion = relationship("CareerPosition", backref="branchrelation")
    
class Branch(db.Model):
    __tablename__ = "branch"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), unique=False, nullable=True)
    email = db.Column(db.String(100), unique=False, nullable=True)
    contact_no = db.Column(db.String(50), unique=False, nullable=True)
    address = db.Column(db.String(500), unique=False, nullable=True) 
    pincode = db.Column(db.String(50), unique=False, nullable=True)
    gmap_link = db.Column(db.String(200), unique=False, nullable=True)   
    description = db.Column(db.String(500), nullable=True) 
 
    date = db.Column(db.DateTime(timezone=True), nullable=True)   
    
    def __init__(self, name, email, contact_no, address, pincode, gmap_link, description,) -> None:        
        self.name = name
        self.email = email
        self.contact_no = contact_no
        self.address = address
        self.pincode = pincode
        self.gmap_link = gmap_link
        self.description = description
       
        self.date = datetime.now()

class BranchImages(db.Model):
    __tablename__ = "branchimages"
    id = db.Column(db.Integer(), primary_key=True)
    branch_id = db.Column(db.Integer(), db.ForeignKey('branchrelation.id'), nullable=False)
    image = db.Column(db.String(100), unique=False, nullable=True)
    image_path = db.Column(db.String(100), unique=False, nullable=True)
    tag = db.Column(db.String(100), unique=False, nullable=True)

    def __init__(self, branch_id, image, image_path, tag) -> None:
        self.branch_id = branch_id
        self.image = image
        self.image_path = image_path
        self.tag = tag

class BranchReview(db.Model):
    __tablename__ = "branchreview"
    id = db.Column(db.Integer(), primary_key=True)
    branch_id = db.Column(db.Integer(), db.ForeignKey('branchrelation.id'), nullable=False)
    user_name = db.Column(db.String(100), unique=False, nullable=True)
    user_email = db.Column(db.String(100), unique=False, nullable=True)
    user_contact_no = db.Column(db.String(100), unique=False, nullable=True)
    review = db.Column(db.String(100), unique=False, nullable=True)
    rating = db.Column(db.Integer(), unique=False, nullable=True)
    date = db.Column(db.DateTime(timezone=True), nullable=True)

    def __init__(self, branch_id, user_name, user_email, user_contact_no, review, rating):
        self.branch_id = branch_id
        self.user_name = user_name
        self.user_email = user_email
        self.user_contact_no = user_contact_no
        self.review = review
        self.rating = rating
        self.date = datetime.now()

