import tkinter as tk
from tkinter import messagebox
from utils.file_utils import read_file
from core.student import Student
from core.admin import Admin
from gui.student_dashboard import open_student_dashboard
from gui.admin_dashboard import open_admin_dashboard

def login_window():
    def login():
        uid = entry_user.get()
        pwd = entry_pass.get()
        creds = read_file("data/passwords.txt")
        for line in creds:
            user, pw = line.strip().split(',')
            if user == uid and pw == pwd:
                users = read_file("data/users.txt")
                for info in users:
                    u, name, email, role = info.strip().split(',')
                    if u == uid:
                        if role == "student":
                            root.destroy()
                            open_student_dashboard(Student(uid, name))
                        elif role == "admin":
                            root.destroy()
                            open_admin_dashboard(Admin(uid, name))
                        return
        messagebox.showerror("Login Failed", "Invalid credentials")

    root = tk.Tk()
    root.title("Login")
    root.geometry("300x200")

    tk.Label(root, text="User ID").pack()
    entry_user = tk.Entry(root)
    entry_user.pack()

    tk.Label(root, text="Password").pack()
    entry_pass = tk.Entry(root, show="*")
    entry_pass.pack()

    tk.Button(root, text="Login", command=login).pack(pady=10)
    root.mainloop()
