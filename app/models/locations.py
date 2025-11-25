from dataclasses import dataclass

from datetime import datetime
from .. import db

from sqlalchemy.orm import relationship

@dataclass
class City(db.Model):
    __tablename__ = "city"

    id: int
    name: str


    id = db.Column(db.Integer(), unique=True, primary_key=True)
    name = db.Column(db.String(100), unique=False, nullable=True)
    state_id = db.Column(db.Integer(), db.ForeignKey("state.id"), nullable=False)
    date = db.Column(db.DateTime(timezone=False), nullable=True)
  

    def __init__(self, name, state_id) -> None:
        self.name = name
        self.state_id = state_id
        self.date = datetime.now()

@dataclass
class State(db.Model):
    
    __tablename__ = "state"
    id: int
    name: str
    city: City

    id = db.Column(db.Integer(), unique=True, primary_key=True)
    name = db.Column(db.String(100), unique=False, nullable=True)
    date = db.Column(db.DateTime(timezone=False), nullable=True)
    city = relationship("City", backref="state")

    goldprice = relationship("HindustanGoldPrice", backref="state")
    states = relationship("UserGoldPrice", backref="state")
    def __init__(self, name) -> None:
        self.name = name
        self.date = datetime.now()
        
        
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'date': self.date
        }

      