import json
import os
from tkinter import *
from tkinter import messagebox, ttk
from datetime import datetime


DATA_FILE = 'books.json'


class BookApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Учет выдачи учебников - МБОУ Красногорская СОШ")
        self.root.geometry("600x400")
        self.root.resizable(True, True)
        self.init_data_file()
        self.books = self.load_books()
        self.create_widgets()
        self.update_book_list()
    
    def init_data_file(self):
        if not os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=4)

    def load_books(self):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    
    def save_books(self):
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.books, f, ensure_ascii=False, indent=4)