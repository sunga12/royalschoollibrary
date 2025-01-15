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
      # print(book['title'])
      self.result_label.config(text=f"Book: {book['title']} by {book['author']}")
    else:
      self.result_label.config(text="Book not found")
      
  
  def checkout_book(self):
    
    pass
  
  
  def return_book(self):
  
    pass
  
  
  
if __name__ == "__main__":
  app = LibraryApp()
  app.mainloop()
  
  
  