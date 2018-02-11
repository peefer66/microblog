from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from hashlib import md5

# create an associate table called followers  for the many to many relationship
# not delclaring  this as a model  since it willhave no data other 
# than the foreign keys

followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    # One to Many relationship
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    # Many to Many relationship. users on both sides of the relationship
    followed = db.relationship('User', secondary=followers,
    primaryjoin=(followers.c.follower_id == id),
    secondaryjoin=(followers.c.followed_id == id),
    backref=db.backref('followers', lazy='dynamic'),
    lazy='dynamic'
    )

    def __repr__(self):
        return '<user {}'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)
    '''
    Need to re-read the book associated with followers to get my head around
    all of this!!!! pg 95 ish
    '''
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
    
    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(self)

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def followed_post(self):
        followed =  Post.query.join(
            followers, (followers.c.followed_id == Post.user.id)).filter(
                followers.c.follower_id == self.id).order_by(Post.timestamp.desc())
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())
            
        


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}'.format(self.body)


'''
 provide a user_loader callback. This callback is used to reload the user object
 from the user ID stored in the session.
 It should take the unicode ID of a user, and return the corresponding user object.
'''
@login.user_loader # Part of Flask-Login functionality
def load_user(id):
    return User.query.get(int(id))
