
from dataclasses import dataclass
from .locations import State
from pymysql import Date

from .. import db
from sqlalchemy.orm import relationship


# class City(db.Model):
#     __tablename__ = "city"
#     id = db.Column(db.Integer(), primary_key=True)
#     name = db.Column(db.String(100), unique=False, nullable=True) 

#     def __init__(self, name) -> None:
#         self.name = name

@dataclass
class HindustanGoldPrice(db.Model):
    id : int
    price : str
    date : str
    state_id : State
    carat: str


    __tablename__ = "hindustangoldprice"
    id = db.Column(db.Integer(), primary_key=True)
    price = db.Column(db.String(50), unique=False, nullable=True) 
    date = db.Column(db.DATE(), nullable=True)
    state_id = db.Column(db.Integer(), db.ForeignKey("state.id"), nullable=False)
    carat = db.Column(db.String(50), unique=False, nullable=True)   
    
    #state = relationship("HindustanGoldPrice", backref="state")

    def __init__(self, price, date, state_id, carat) -> None:
        self.price = price
        self.date = date
        self.state_id = state_id
        self.carat = carat

class GoldPrice(db.Model):
    __tablename__ = "goldprice"
    id = db.Column(db.Integer(), primary_key=True)
    price = db.Column(db.String(50), unique=False, nullable=True) 
    date = db.Column(db.DATE(), nullable=True)
    city=db.Column(db.String(50), unique=False, nullable=True)
    timestamp = db.Column(db.String(50), nullable=False)    
    price_gram_24k = db.Column(db.String(50), nullable=False)
    price_gram_22k = db.Column(db.String(50), nullable=False)
    price_gram_21k = db.Column(db.String(50), nullable=False)
    price_gram_20k = db.Column(db.String(50), nullable=False)
    price_gram_18k = db.Column(db.String(50), nullable=False)

    def __init__(self, price, date, timestamp, price_gram_24k, price_gram_22k, price_gram_21k, price_gram_20k, price_gram_18k, city="All",) -> None:
        self.price = price
        self.date = date
        self.timestamp = timestamp
        self.city = city        
        self.price_gram_24k = price_gram_24k
        self.price_gram_22k = price_gram_22k
        self.price_gram_21k = price_gram_21k
        self.price_gram_20k = price_gram_20k
        self.price_gram_18k = price_gram_18k


class UserGoldPrice(db.Model):
    __tablename__ = "usergoldprice"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), unique=False, nullable=True) 
    mobile_no = db.Column(db.String(50), unique=False, nullable=True) 
    gross_weight = db.Column(db.String(50), unique=False, nullable=True) 
    stone_weight = db.Column(db.String(50), unique=False, nullable=True) 
    net_weight = db.Column(db.String(50), unique=False, nullable=True) 
    price = db.Column(db.String(50), unique=False, nullable=True)     
    state_id=db.Column(db.Integer(), db.ForeignKey("state.id"), nullable=True)
    carat =db.Column(db.String(20), nullable=False)
    status = db.Column(db.Integer(), nullable=True)
    date = db.Column(db.DateTime(timezone=False))

    
    def __init__(self, name, mobile_no, gross_weight, stone_weight, net_weight, price, state_id, carat, date, status) -> None:
        self.name = name
        self.mobile_no = mobile_no
        self.gross_weight = gross_weight
        self.stone_weight = stone_weight
        self.net_weight = net_weight
        self.price = price
        self.state_id = state_id
        self.carat = carat
        self.date = date
        self.status = status
        