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

    def create_widgets(self):
        top_frame = Frame(self.root, bg='#f0f0f0', pady=10)
        top_frame.pack(fill=X)
        
        Label(top_frame, text="Название учебника:", bg='#f0f0f0', font=('Arial', 10)).pack(side=LEFT, padx=5)
        
        self.book_entry = Entry(top_frame, width=40, font=('Arial', 10))
        self.book_entry.pack(side=LEFT, padx=5)
        self.book_entry.bind('<Return>', lambda e: self.add_book())
        
        Button(top_frame, text="Добавить учебник", command=self.add_book, 
               bg='#4CAF50', fg='white', padx=10, pady=2, font=('Arial', 10)).pack(side=LEFT, padx=5)
        
        Button(top_frame, text="Удалить выбранное", command=self.delete_book,
               bg='#f44336', fg='white', padx=10, pady=2, font=('Arial', 10)).pack(side=LEFT, padx=5)
        
        columns = ('Название', 'Дата добавления', 'Статус')
        self.tree = ttk.Treeview(self.root, columns=columns, show='headings', height=15)
        
        self.tree.heading('Название', text='Название учебника')
        self.tree.heading('Дата добавления', text='Дата добавления')
        self.tree.heading('Статус', text='Статус')
        
        self.tree.column('Название', width=300)
        self.tree.column('Дата добавления', width=150)
        self.tree.column('Статус', width=100)
        
        scrollbar = ttk.Scrollbar(self.root, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)
        scrollbar.pack(side=RIGHT, fill=Y, pady=10)
        
        bottom_frame = Frame(self.root, bg='#e0e0e0', pady=5)
        bottom_frame.pack(fill=X, side=BOTTOM)
        
        self.stats_label = Label(bottom_frame, text="", bg='#e0e0e0', font=('Arial', 9))
        self.stats_label.pack(side=LEFT, padx=10)
        
        Button(bottom_frame, text="Обновить список", command=self.update_book_list,
               bg='#2196F3', fg='white', padx=10).pack(side=RIGHT, padx=10)
        
    def add_book(self):
        book_name = self.book_entry.get().strip()
        
        if not book_name:
            messagebox.showwarning("Предупреждение", "Введите название учебника!")
            return
        
        new_book = {
            'name': book_name,
            'date': datetime.now().strftime('%d.%m.%Y %H:%M'),
            'status': 'В наличии'
        }
        
        self.books.append(new_book)
        
        self.save_books()
        
        self.book_entry.delete(0, END)
        
        self.update_book_list()
        
        messagebox.showinfo("Успех", f"Учебник '{book_name}' добавлен!")
    
    def delete_book(self):
        selected = self.tree.selection()
        
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите учебник для удаления!")
            return
        
        result = messagebox.askyesno("Подтверждение", "Удалить выбранный учебник?")
        
        if result:
            for item in selected:
                item_text = self.tree.item(item)['values'][0]
                for i, book in enumerate(self.books):
                    if book['name'] == item_text:
                        self.books.pop(i)
                        break
            
            self.save_books()
            self.update_book_list()
            messagebox.showinfo("Успех", "Учебник удален!")
    
    def update_book_list(self):
        """Обновляет список книг на экране"""
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        for book in self.books:
            self.tree.insert('', END, values=(book['name'], book['date'], book['status']))
        
        total = len(self.books)
        self.stats_label.config(text=f"Всего учебников: {total}")

if __name__ == "__main__":
    root = Tk()
    app = BookApp(root)
    root.mainloop()
    
   