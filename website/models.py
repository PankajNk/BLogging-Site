from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer,primary_key= True)
    email = db.Column(db.String(150), unique = True)
    username = db.Column(db.String(150), unique = True)
    password = db.Column(db.String(150))
    #date_created = db.Column(db.Date(timezone=True),default=func.now())
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    #after creating Pst
    posts = db.relationship('Post', backref='user', passive_deletes=True)
    comments = db.relationship('Comment', backref='user', passive_deletes=True)

class Post(db.Model):
    id = db.Column(db.Integer,primary_key= True)  #!to many relationship
    text = db.Column(db.Text,nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete="CASCADE"), nullable=False)
        #user.id is User db just that u is store small letter in db
    comments = db.relationship('Comment', backref='post', passive_deletes=True)  
    
class Comment(db.Model):
    id = db.Column(db.Integer,primary_key= True)  #!to many relationship
    text = db.Column(db.String(200),nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete="CASCADE"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey(
        'post.id', ondelete="CASCADE"), nullable=False)