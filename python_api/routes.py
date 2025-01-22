from flask import request, jsonify
from app import app, db
from models import Book, User, Activity

@app.route('/api/v1/books', methods=['GET'])
def get_books():
  books = Book.query.all()
  return jsonify([{
    'id': book.id,
    'title': book.title,
    'author': book.author,
    'availability': book.availability,
    'barcode': book.barcode
    
  } for book in books])
  

@app.route('/api/v1/books', methods=['POST'])
def add_book():
  data = request.json
  if not data or 'title' not in data or 'author' not in data or 'barcode' not in data:
    return jsonify({'error': 'Missing required fields'}), 400
  new_book = Book(
    title=data['title'],
    author=data['author'],
    barcode=data['barcode'],
    availability=data.get('availability', 'available') 
  )
  db.session.add(new_book)
  db.session.commit()
  return jsonify({'message': 'Book Added Successfully!'}), 201


@app.route('/api/v1/books/<int:id>', methods=['GET'])
def get_book(id):
  book = Book.query.get_or_404(id)
  return jsonify({
    'id': book.id,
    'title': book.title,
    'author': book.author,
    'availability': book.availability,
    'barcode': book.barcode
  })
  

@app.route('/api/v1/books/<int:id>', methods=['PUT'])
def update_book(id):
  book = Book.query.get_or_404(id)
  data = request.json
  book.title = data.get('title', book.title)
  book.author = data.get('author', book.author)
  book.availability = data.get('availability', book.availability)
  db.session.commit()
  return jsonify({'message': 'Book updated successfully!'})


@app.route('/api/v1/books/<int:id>', methods=['DELETE'])
def delete_book(id): 
  book = Book.query.get_or_404(id)
  db.session.delete(book)
  db.session.commit()
  return jsonify({'message': 'Book Deleted Successfully!'})


@app.route('/api/v1/books/<string:barcode>', methods=['GET'])
def show_by_barcode(barcode):
  book = Book.query.filter_by(barcode=barcode).first()
  if book:
    return jsonify({
      'id': book.id,
      'title': book.title,
      'author': book.author,
      'barcode': book.barcode,
      'availability': book.availability
    }), 200 # OK
  else:
    return jsonify({'error': 'Sorry, Book not found'}), 404 # NOT FOUND

#USERS

@app.route('/api/v1/users', methods=['GET'])
def get_users():
  users = User.query.all()
  return jsonify([{
    'id': user.id,
    'name': user.name,
    'role': user.role,
    'school_id': user.school_id,
    'email': user.email
  } for user in users])
  

@app.route('/api/v1/users', methods=['POST'])
def add_user():
  data = request.json
  if not data or 'name' not in data or 'role' not in data or 'school_id' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
  new_user = User(
    name=data['name'],
    role=data['role'],
    school_id=data['school_id'],
    email=data['email']
  )
  db.session.add(new_user)
  db.session.commit()
  return jsonify({'message': 'User Added Successfully!'}), 201

@app.route('/api/v1/users/<int:id>', methods=['GET'])
def get_user(id):
  user = User.query.get_or_404(id)
  return jsonify({
    'id': user.id,
    'name': user.name,
    'role': user.role,
    'school_id': user.school_id,
    'email': user.email
  })
  
  
@app.route('/api/v1/users/<int:id>', methods=['PUT'])
def update_user(id):
  user = User.query.get_or_404(id)
  data = request.json
  user.name = data.get('name', user.name)
  user.role = data.get('role', user.role)
  user.school_id = data.get('school_id', user.school_id)
  user.email = data.get('email', user.email)
  db.session.commit()
  return jsonify({'message': 'User updated successfully!'})


@app.route('/api/v1/users/<int:id>', methods=['DELETE'])
def delete_user(id):
  user = User.query.get_or_404(id)
  db.session.delete(user)
  db.session.commit()
  return jsonify({'message': 'User Deleted Successfully!'})

@app.route('/api/v1/users/<string:school_id>', methods=['GET'])
def show_by_school_id(school_id):
  user = User.query.filter_by(school_id=school_id).first()
  if user:
    return jsonify({
      'id': user.id,
      'name': user.name,
      'role': user.role,
      'school_id': user.school_id,
      'email': user.email
    }), 200 # OK
  else:
    return jsonify({'error': 'Sorry, User not found'}), 404 # NOT FOUND
  
  
  
  # ACTIVITIES
  
@app.route('/api/v1/activities', methods=['GET'])
def get_activities():
  activities = Activity.query.all()
  return jsonify([{
    'id': activity.id,
    'user_id': activity.user_id,
    'book_id': activity.book_id, 
    'checkout': activity.checkout,
    'checkin': activity.checkin,
    'status': activity.status
  } for activity in activities])
  
  
@app.route('/api/v1/activities', methods=['POST'])
def add_activity():
  data = request.json
  if not data or 'user_id' not in data or 'book_id' not in data or 'checkout' not in data or 'status' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
      
  new_activity = Activity(
    user_id=data['user_id'],
    book_id=data['book_id'],
    checkout=data['checkout'],
    status=data['status']
  )
  db.session.add(new_activity)
  db.session.commit()
  return jsonify({'message': 'Entry Created Successfully!'}), 201


@app.route('/api/v1/activities/<int:id>', methods=['POST'])
def update_activity(id):
  activity = Activity.query.get_or_404(id)
  data = request.json
  activity.checkin = data.get('checkin', activity.checkin)
  db.session.commit()
  return jsonify({'message': 'Entry updated successfully!'})

  
@app.route('/api/v1/activities/<int:id>', methods=['DELETE'])
def delete_activity(id):
  activity = Activity.query.get_or_404(id)
  db.session.delete(activity)
  db.session.commit()
  return jsonify({'message': 'Entry Deleted Successfully!'})


@app.route('/api/v1/activities', methods=['GET'])
def show_by_user_book_id():
  user_id = request.args.get('user_id')
  book_id = request.args.get('book_id')
  
  if not user_id or not book_id:
    return jsonify({'error': 'Missing user_id or book_id'}), 400  # Bad Request
  
  activity = Activity.query.filter_by(user_id=user_id, book_id=book_id, status='Checked Out').order_by(Activity.checkout.desc()).first()
  
  if activity:
    return jsonify({
      'id': activity.id,
      'user_id': activity.user_id,
      'book_id': activity.book_id,
      'checkout': activity.checkout,
      'checkin': activity.checkin,
      'status': activity.status
    }), 200 # OK
  else:
    return jsonify({'error': 'Sorry, Entry not found'}), 404 # NOT FOUND