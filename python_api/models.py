from app import db

class Book(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(100), nullable=False)
  author = db.Column(db.String(100), nullable=False)
  availability = db.Column(db.String(20), default="available")
  barcode = db.Column(db.String(50), unique=True, nullable=False)
  
  #relationship to Activity
  activities = db.relationship('Activity', backref='book', lazy=True)
  
  
class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), nullable=False)
  role = db.Column(db.String(100), nullable=False)
  school_id = db.Column(db.String(20), unique=True, nullable=False)
  email = db.Column(db.String(100), nullable=False)
 
  #relationship to Activity
  activities = db.relationship('Activity', backref='user', lazy=True)

class Activity(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  checkout = db.Column(db.DateTime, nullable=False)
  checkin = db.Column(db.DateTime, nullable=True) #Nullable if not yet returned to library
  status = db.Column(db.String(20), nullable=False)
