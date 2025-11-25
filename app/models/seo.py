from datetime import datetime
from .. import db


class SeoMetaData(db.Model):
    __tablename__ = "seometadata"

    id = db.Column(db.Integer(), primary_key=True)
    page = db.Column(db.String(50), nullable=True)
    date = db.Column(db.DateTime(timezone=True), nullable=True)
    title = db.Column(db.String(200), unique=False, nullable=True)
    description = db.Column(db.String(500), unique=False, nullable=True)
    keywords = db.Column(db.String(500), unique=False, nullable=True)
    # url = db.Column(db.String(100), unique=False, nullable=False)
    # image = db.Column(db.String(100), unique=False, nullable=False)
    # image_alt = db.Column(db.String(100), unique=False, nullable=False)
    # image_title = db.Column(db.String(100), unique=False, nullable=False)
    # image_caption = db.Column(db.String(100), unique=False, nullable=False)
    # image_description = db.Column(db.String(100), unique=False, nullable=False)
    # image_width = db.Column(db.String(100), unique=False, nullable=False)
    # image_height = db.Column(db.String(100), unique=False, nullable=False)
    # image_type = db.Column(db.String(100), unique=False, nullable=False)
    # image_size = db.Column(db.String(100), unique=False, nullable=False)
    # image_url = db.Column(db.String(100), unique=False, nullable=False)
    
    def __init__(self, page, title, description, keywords) -> None:
        self.date = datetime.now()
        self.title = title
        self.page = page
        self.description = description
        self.keywords = keywords