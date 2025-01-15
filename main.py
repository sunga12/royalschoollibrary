import tkinter as tk
import requests

class LibraryApp(tk.Tk):
  def __init__(self):
    super().__init__()
    self.title("Library System")
    self.geometry("400x300")
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

  
  def checkout_book(self):
    
    # is book.status avaliable? 
    # => get request for the book.avaliability
    barcode = self.barcode_entry.get()
    response = requests.get(f'http://localhost:3000/api/v1/books/barcode/{barcode}')
    if response.status_code == 200:
      book = response.json()

    if book['avaliability'] == 'avaliable':
      
      self.status_label = tk.Label(self, text="Choose the new book status")
      self.status_label.pack()
      
      status_options = ["Avaliable", "Checked Out", "Unavaliable"]
      
      new_status = tk.StringVar(self)
      new_status.set(status_options[0])
      
      status_dropdown = tk.OptionMenu(self, new_status, *status_options)
      status_dropdown.pack()
      
      self.school_id_label = tk.Label(self, text="Enter the School ID number")
      self.school_id_label.pack()
    
      self.school_id_entry = tk.Entry(self)
      self.school_id_entry.pack()
      self.school_id_entry.bind("<Return>", self.search_user)

      self.id_result_label = tk.Label(self, text="")
      self.id_result_label.pack()
      
      
      # data = {
      #   user_id
      # }
      
      # requests.post(http://localhost:3000/api/v1/activities/)
      
    else:
      self.status_label = tk.Label(self, text="Book is not avaliable")
      self.status_label.pack()
    
      
    
  def search_user(self, event): 
    school_id = self.school_id_entry.get()
    response = requests.get(f'http://localhost:3000/api/v1/users/school_id/{school_id}')
    
    if response.status_code == 200:
      user = response.json()
      self.id_result_label.config(text=f"User: {user['name']}. Role: {user['role']}. System ID: {user['id']}.")
    else:
      self.id_result_label.config(text="User not found")
    # yes: 
    # => school_id? => new tranaction post, update book status put
    # => Activity.create(user_id: 1, book_id: 1, checkout: Time.now,  status: "Checkout")
    # => Book.update(avaliability: "Checked out")
    
    
    # no: 
    # => return error message 
    
    pass
  
  
  def return_book(self):
  
    pass
  
  
  
if __name__ == "__main__":
  app = LibraryApp()
  app.mainloop()
  
  
  