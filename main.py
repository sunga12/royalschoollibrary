import tkinter as tk
import requests
from datetime import datetime

class LibraryApp(tk.Tk):
  def __init__(self):
    super().__init__()
    self.title("Library System")
    self.geometry("400x300+1200+100")
    self.create_widgets()
    
  def create_widgets(self):
    self.barcode_label = tk.Label(self, text="Scan or Input Barcode:")
    self.barcode_label.pack()
    
    self.barcode_entry = tk.Entry(self)
    self.barcode_entry.pack()
    self.barcode_entry.bind("<Return>", self.search_book)
    
    self.result_label = tk.Label(self, text="")
    self.result_label.pack()
    
    self.checkout_button = tk.Button(self, text="Checkout Book", command=self.checkout_book)
    self.checkout_button.pack()
    
    self.return_button = tk.Button(self, text="Return Book", command=self.return_book)
    self.return_button.pack()
    
    
  def search_book(self, event):
    barcode = self.barcode_entry.get()
    response = requests.get(f'http://localhost:3000/api/v1/books/barcode/{barcode}')
    if response.status_code == 200:
      book = response.json()
      self.result_label.config(text=f"Book: {book['title']} by {book['author']}")
    else:
      self.result_label.config(text="Book not found")

  def search_user(self, event): 
    school_id = self.school_id_entry.get()
    response = requests.get(f'http://localhost:3000/api/v1/users/school_id/{school_id}')
    
    if response.status_code == 200:
    # yes: 
    # => school_id? => new tranaction post, update book status put
    # => Activity.create(user_id: 1, book_id: 1, checkout: Time.now,  status: "Checkout")
    # => Book.update(avaliability: "Checked out")
    
      user = response.json()
      self.user_id = user['id']
      print(self.user_id)
      self.id_result_label.config(text=f"User: {user['name']}. Role: {user['role']}. System ID: {user['id']}.")
    else:
      # no: 
      # => return error message 
      self.id_result_label.config(text="User not found")
      
  def search_activity(self, event=None): 
      book_id = self.book_id
      user_id = self.user_id
      
      response = requests.get(f'http://localhost:3000/api/v1/activities/ids/{book_id}/{user_id}')
      
      if response.status_code == 200:
          activity = response.json()
          self.activity_id = activity['id']
          print(self.activity_id)
          self.activity_id_label.config(text=f"Checkout ID number is:  {activity['id']}.")
      else:
          print(response.status_code)
          self.activity_id_label.config(text="Entry not found")
      
  def checkout_book(self):
    
    # is book.status avaliable? 
    # => get request for the book.avaliability
    barcode = self.barcode_entry.get()
    response = requests.get(f'http://localhost:3000/api/v1/books/barcode/{barcode}')
    if response.status_code == 200:

      book = response.json()
      self.book_id = book['id']
      
      if book['avaliability'] == 'avaliable':
        
        self.status = 'Checked Out'
        
        self.school_id_label = tk.Label(self, text="Enter the School ID number")
        self.school_id_label.pack()
      
        self.school_id_entry = tk.Entry(self)
        self.school_id_entry.pack()
        self.school_id_entry.bind("<Return>", self.search_user)

        self.id_result_label = tk.Label(self, text="")
        self.id_result_label.pack()
        
        self.confirm_checkout = tk.Button(self, text='Confirm', command=self.checkout_activity)
        self.confirm_checkout.pack()
        
      else:
        self.status_label = tk.Label(self, text="Book is not avaliable")
        self.status_label.pack()
    
        
  def checkout_activity(self):
    activity_data = {
      'user_id': self.user_id,
      'book_id': self.book_id,
      'status': self.status
    }
    
    print(activity_data)
    
    activity_response = requests.post('http://localhost:3000/api/v1/activities', json=activity_data)
    
    book_update_data = {
      'avaliability': 'Checked Out'
    }
    
    book_response = requests.put(f'http://localhost:3000/api/v1/books/{self.book_id}', json=book_update_data)
        
    if activity_response.status_code == 201 and book_response.status_code == 200:
      print("Check Out Successful!")
      print("Book is now awaiting Return!")
    else:
      print("Error in checkout or book update") 
      print(activity_response.json())
      print(book_response.json()) 



  def return_book(self):
    # is book.status unavaliable? 
    # => get request for the book.avaliability
    barcode = self.barcode_entry.get()
    response = requests.get(f'http://localhost:3000/api/v1/books/barcode/{barcode}')
    if response.status_code == 200:

      book = response.json()
      self.book_id = book['id']
      
      if book['avaliability'] == 'Checked Out':
        
        self.status = 'Checked In'
      
        self.school_id_label = tk.Label(self, text="Enter the School ID number")
        self.school_id_label.pack()
      
        self.school_id_entry = tk.Entry(self)
        self.school_id_entry.pack()
        self.school_id_entry.bind("<Return>", self.search_user)

        self.id_result_label = tk.Label(self, text="")
        self.id_result_label.pack()
        
        self.check_entry = tk.Button(self, text='Check Entry Number', command=self.search_activity)
        self.check_entry.pack()
        
        self.activity_id_label = tk.Label(self, text="")
        self.activity_id_label.pack()
        
        self.confirm_return = tk.Button(self, text='Confirm', command=self.checkin_activity)
        self.confirm_return.pack()
        
      else:
        self.status_label = tk.Label(self, text="Book is already returned.")
        self.status_label.pack()
        
        
   
  def checkin_activity(self):
    
    now =  datetime.now()
    
    update_data = {
      'user_id': self.user_id,
      'book_id': self.book_id,
      'status': self.status,
      'checkin': now.strftime("%Y-%m-%dT%H:%M:%S")
    }
    
    print(update_data)
    activity_response = requests.put(f'http://localhost:3000/api/v1/activities/{self.activity_id}', json=update_data)
    
    book_update_data = {
      'avaliability': 'avaliable'
    }
    
    book_response = requests.put(f'http://localhost:3000/api/v1/books/{self.book_id}', json=book_update_data)
        
    if activity_response.status_code == 200 and book_response.status_code == 200:
      print("Check In Successful!")
      print("Book is now avaliable for Check Out!")
    else:
      print("Error in checkin or book update")   

        
  
if __name__ == "__main__":
  app = LibraryApp()
  app.mainloop()
  
  
  