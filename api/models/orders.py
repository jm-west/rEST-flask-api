
from ..utils import db
from enum import Enum

class Size(Enum): #Makes choisces for the size of the pizza
    SMALL = 'small'
    MEDIUM = 'medium'
    LARGE = 'large'
    XLARGE = 'xlarge'

class Status(Enum): #Makes choices for the status of the order
    PENDING = 'pending'
    IN_TRANSIT = 'in_transit'
    DELIVERED = 'delivered'

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    size = db.Column(db.Enum(Size),default=Size.SMALL)
    status = db.Column(db.Enum(Status), default=Status.PENDING) 
    flavor = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer)
    users=db.Column(db.Integer,db.ForeignKey('users.id')) #Foreign key to the users table in other py file

    def __str__(self):
        return f"<Order {self.id}>"

    def save(self):
        db.session.add(self)
        db.session.commit()