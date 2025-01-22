from app import app, db
from models import Book, User, Activity

with app.app_context():
  db.create_all()
  print("Database Initialized!")
  
#  app.app_context(): This ensures that the Flask application context 
#  is active while running the db.create_all() command.
#  with statement: It creates and tears down the application context
#  automatically, ensuring proper resource management.