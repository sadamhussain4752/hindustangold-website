from .. import db, app
from flask_login import UserMixin, login_manager

@app.login_manager.user_loader
def get_user(ident):
  return User.query.get(int(ident))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
