from ..utils import db

class User(db.Model):
    __tablename__ = 'users'
    id= db.Column(db.Integer, primary_key=True)
    username= db.Column(db.String(25), unique=True, nullable=False)
    email= db.Column(db.String(50), unique=True, nullable=False)
    passwordHash= db.Column(db.Text(), nullable=False)
    is_staff= db.Column(db.Boolean, default=False)
    is_active= db.Column(db.Boolean, default=True)
    orders= db.relationship('Order', backref='user', lazy=True)


    def __repr__(self):
        return f"<User {self.usernames}>" 
    
    def save(self):
        db.session.add(self)
        db.session.commit()
