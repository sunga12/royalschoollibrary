import tkinter as tk
from tkinter import ttk
import requests
from datetime import datetime

class LibraryApp(tk.Tk):
  def __init__(self):
    super().__init__()
    self.title("Royal School Library System") 
    self.geometry("700x500+1000+100")
    self.create_widgets()
    
  def create_widgets(self):
    
    self.welcome_label = tk.Label(self, text="Welcome to the Royal School Library")
    self.welcome_label.config(font=("Arial", 24, "bold"))
    self.welcome_label.pack(pady="40", padx="10", anchor="center")
    self.barcode_label = tk.Label(self, text="Scan or Input a Book Barcode:")
    self.barcode_label.pack()
    
    self.barcode_entry = ttk.Entry(self)
    self. barcode_entry.config(width=50)
    self.barcode_entry.pack()
    self.barcode_entry.bind("<Return>", self.search_book)
    
    self.result_label = tk.Label(self, text="")
    self.result_label.pack()
    
    self.checkout_button = ttk.Button(self, text="Checkout Book", command=self.checkout_book)
    self.checkout_button.config(width=20)
    self.checkout_button.pack(side="left", padx=20, pady=10, fill="x")
    
    self.return_button = ttk.Button(self, text="Return Book", command=self.return_book)
    self.return_button.config(width=20)
    self.return_button.pack(side="right", padx=20, pady=10, fill="x")
    
    self.addbook_button = ttk.Button(self, text="Add New Book", command=self.add_book)
    self.addbook_button.config(width=20)
    self.addbook_button.pack(side="bottom", padx=20, pady=30, fill="x")
    
  def add_book(self):
    
    #Create new top level sub window
    
    addwindow = tk.Toplevel(self)
    addwindow.title("Add New Book")
    addwindow.geometry("600x600+1200+200")
    
    addwindow.transient(self)
    addwindow.grab_set()
    
    self.new_book_widgets(addwindow)
    
  
  def new_book_widgets(self, window):
    self.book_instruction_title = ttk.Label(window, text="Insert the Details of the New Book")
    self.book_instruction_title.config(font=("Arial", 20, "bold"))
    self.book_instruction_title.pack(pady="40", padx="10", anchor="center")

    self.new_barcode_label = ttk.Label(window, text="Scan or Input the Book Barcode:")
    self.new_barcode_label.pack(pady="20", padx="10")
    
    self.new_barcode_entry = ttk.Entry(window)
    self.new_barcode_entry.config(width=100)
    self.new_barcode_entry.pack(pady="10", padx="20")
    
    self.new_title_label = ttk.Label(window, text="Book Title:")
    self.new_title_label.pack(pady="20", padx="10")
    
    self.new_title_entry = ttk.Entry(window)
    self.new_title_entry.config(width=100)
    self.new_title_entry.pack(pady="10", padx="20")
    
    self.new_author_label = ttk.Label(window, text="Book Author:")
    self.new_author_label.pack(pady="20", padx="10")
    
    self.new_author_entry = ttk.Entry(window)
    self.new_author_entry.config(width=100)
    self.new_author_entry.pack(pady="10", padx="20")
    
    self.postbook_button = ttk.Button(window, text="Add Book", command=lambda: self.post_book(window))
    self.postbook_button.pack(side="bottom", padx=20, pady=30, fill="x")
    
    
  def post_book(self, window):
    book_data = {
      'title': self.new_title_entry.get(),
      'author': self.new_author_entry.get(),
      'avaliability': "avaliable",
      'barcode': self.new_barcode_entry.get()
    }
        
    book_response = requests.post('http://localhost:3000/api/v1/books', json=book_data)    
    
    if book_response.status_code == 201:
      self.new_book_response_label = ttk.Label(window, text=f"New Book Successfully Created: {book_data['title']}, by {book_data['author']}, barcode number: {book_data['barcode']}.", wraplength=300)
      
      self.new_book_response_label.pack(pady="20", padx="10")
      
      self.new_author_entry.delete(0, tk.END)
      self.new_title_entry.delete(0, tk.END)
      self.new_barcode_entry.delete(0, tk.END)


      self.after(10000, self.new_book_response_label.destroy)

    else:
      self.new_book_response_label = ttk.Label(window, text="Failed To Add Book, Please Try again")
      self.new_book_response_label.pack(pady="20", padx="10")
      self.after(5000, self.new_book_response_label.destroy)


  
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
        self.status_label = tk.Label(self, text="Book is not avaliable for Checkout")
        self.status_label.pack()
        self.after(4000, self.status_label.destroy)
        
    else:
      self.get_book_label = tk.Label(self, text="Unable to get Book details")
      self.get_book_label.pack()
      self.after(1000, self.get_book_label.destroy)


        
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
      self.confirm_checkout.destroy()
      self.confirm_label = tk.Label(self, text="Check Out Successful! Book is now awaiting Return!")
      self.confirm_label.pack()      
      self.school_id_label.destroy()
      self.school_id_entry.destroy()
      self.id_result_label.destroy()
      self.result_label.destroy()
      self.result_label = tk.Label(self, text="")
      self.result_label.pack()
          
      if self.status_label:
        self.status_label.destroy()
        
      self.id_result_label.destroy()
      self.barcode_entry.delete(0, tk.END)
      self.after(3000, self.confirm_label.destroy)
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
        self.after(3000, self.status_label.destroy) 
    else:
      self.get_book_label = tk.Label(self, text="Unable to get Book details")
      self.get_book_label.pack()
      self.after(1000, self.get_book_label.destroy)
        
        
  
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
      self.confirm_label = tk.Label(self, text="Check In Successful! Book is now avaliable for Check Out!")
      self.confirm_label.pack()      
      print("Check In Successful!")
      print("Book is now available for check out")
      self.school_id_label.destroy()
      self.school_id_entry.destroy()
      self.id_result_label.destroy()
      self.check_entry.destroy()
      self.activity_id_label.destroy()
      self.status_label.destroy()
      self.result_label.destroy()
      self.result_label = tk.Label(self, text="")
      self.result_label.pack()
      self.confirm_return.destroy()
      self.barcode_entry.delete(0, tk.END)
      self.after(3000, self.confirm_label.destroy)
      
    else:
      print("Error in checkin or book update")   

        
  
if __name__ == "__main__":
  app = LibraryApp()
  app.mainloop()
  
  
  