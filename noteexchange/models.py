from noteexchange import db
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime, date, time, timedelta


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    name = db.Column(db.String(20))
    password = db.Column(db.String(20))
    admin = db.Column(db.Boolean)
    listings = db.relationship('Listing')

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def is_active(self):
        return True

    def get_id(self):
        return unicode(self.id)

    # Returns overall rating for a user
    def get_rating(self):
        score = 0
        for listing in self.listings:
            score += float(sum(listing.ratings)/5)
        return score / len(self.listings)

    def __init__(self, username, name, password, admin=False):
        self.username = username
        self.name = name
        self.password = password
        self.admin = admin


class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversations.id'))
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    sender = db.relationship('User')
    content = db.Column(db.String(511))
    sent_at = db.Column(db.DateTime(), default=datetime.utcnow)
    read = db.Column(db.Boolean())

    def read_msg(self):
        self.read = True

    def __init__(self, conversation_id, sender, content, read=False):
        self.conversation_id = conversation_id
        self.sender_id = sender
        self.content = content
        self.read = read


class Conversation(db.Model):
    __tablename__  = 'conversations'
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer)
    receiver_id = db.Column(db.Integer)
    subject = db.Column(db.String(100))
    messages = db.relationship('Message', backref='conversation')

    def __init__(self, sender_id, receiver_id, subject):
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.subject = subject


class Listing(db.Model):
    __tablename__ = 'listings'
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    file_name = db.Column(db.String(50))
    course = db.Column(db.String(20))
    term = db.Column(db.String(50))
    course_date = db.Column(db.DateTime())
    upload_date = db.Column(db.DateTime(), default=datetime.utcnow)
    price = db.Column(db.Float())
    ratings = db.relationship('Rating')

    def __init__(self, owner_id, file_name, course, price,
                    term=None, course_date=None):
        self.owner_id = owner_id
        self.file_name = file_name
        self.course = course
        self.price = price
        # Term should not be required.
        self.term = term
        self.course_date = course_date


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    text = db.Column(db.String(4000))
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    owner = db.relationship('User')
    post_time = db.Column(db.DateTime(), default=datetime.utcnow)

    def __init__(self, text, owner_id, title=None):
        self.title = title
        self.text = text
        self.owner_id = owner_id


class Rating(db.Model):
    __tablename__ = 'rating'
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    listing_id = db.Column(db.Integer, db.ForeignKey('listings.id'))
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'))
    comment = db.relationship('Comment')

    def __init__(self, score, sender_id, comment_id=None):
        self.score = score
        self.sender_id = sender_id
        self.comment_id = comment_id

    def __repr__(self):
        return self.score
