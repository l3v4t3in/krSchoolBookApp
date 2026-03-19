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
        
