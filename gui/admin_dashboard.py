import tkinter as tk
from tkinter import messagebox, ttk
from utils.file_utils import read_file, write_file

def open_admin_dashboard(admin):
    root = tk.Tk()
    root.title(f"Admin Dashboard - {admin.name}")
    root.geometry("600x600")

    def add_user():
        win = tk.Toplevel(root)
        win.title("Add New User")
        win.geometry("350x300")

        tk.Label(win, text="User ID:").pack(pady=2)
        uid_entry = tk.Entry(win)
        uid_entry.pack()

        tk.Label(win, text="Full Name:").pack(pady=2)
        name_entry = tk.Entry(win)
        name_entry.pack()

        tk.Label(win, text="Email:").pack(pady=2)
        email_entry = tk.Entry(win)
        email_entry.pack()

        tk.Label(win, text="Password:").pack(pady=2)
        password_entry = tk.Entry(win, show='*')
        password_entry.pack()

        tk.Label(win, text="Role:").pack(pady=2)
        role_var = tk.StringVar(win)
        role_dropdown = ttk.Combobox(win, textvariable=role_var, values=["student", "admin"])
        role_dropdown.pack()
        role_dropdown.current(0)

        def save():
            uid = uid_entry.get()
            name = name_entry.get()
            email = email_entry.get()
            password = password_entry.get()
            role = role_var.get()
            if uid and name and email and password and role:
                try:
                    admin.add_user(uid, name, email, role, password)
                    messagebox.showinfo("Success", f"{role.title()} added.")
                    win.destroy()
                except Exception as e:
                    messagebox.showerror("Error", str(e))

        tk.Button(win, text="Add User", command=save).pack(pady=10)

    def update_user():
        win = tk.Toplevel(root)
        win.title("Update User")
        users = read_file("data/users.txt")

        for line in users:
            parts = line.strip().split(',')
            if len(parts) == 4:
                uid, name, email, role = parts
                frame = tk.Frame(win, pady=2)
                frame.pack(fill="x")
                tk.Label(frame, text=f"{uid} - {name} ({role})", anchor='w').pack(side="left")
                tk.Button(frame, text="Update", command=lambda u=uid: show_update_form(u)).pack(side="right")

        def show_update_form(uid):
            update_win = tk.Toplevel(win)
            update_win.title("Update User Info")
            tk.Label(update_win, text="New Full Name:").pack()
            name_entry = tk.Entry(update_win)
            name_entry.pack()
            tk.Label(update_win, text="New Email:").pack()
            email_entry = tk.Entry(update_win)
            email_entry.pack()
            def update():
                new_name = name_entry.get()
                new_email = email_entry.get()
                if new_name and new_email:
                    admin.update_user(uid, new_name, new_email)
                    messagebox.showinfo("Updated", f"{uid} updated.")
                    update_win.destroy()
            tk.Button(update_win, text="Save", command=update).pack(pady=10)

    def delete_user():
        win = tk.Toplevel(root)
        win.title("Delete User")
        users = read_file("data/users.txt")

        for line in users:
            parts = line.strip().split(',')
            if len(parts) == 4:
                uid, name, email, role = parts
                frame = tk.Frame(win, pady=2)
                frame.pack(fill="x")
                tk.Label(frame, text=f"{uid} - {name} ({role})", anchor='w').pack(side="left")
                tk.Button(frame, text="Delete", command=lambda u=uid: confirm_delete(u)).pack(side="right")

        def confirm_delete(uid):
            if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete user {uid}?"):
                admin.delete_user(uid)
                messagebox.showinfo("Deleted", f"User {uid} deleted.")
                win.destroy()

    def update_grades():
        uid = tk.simpledialog.askstring("Student ID", "Enter student ID:")
        marks = tk.simpledialog.askstring("Marks", "Enter 5 marks (comma-separated):")
        if uid and marks:
            grades = marks.split(',')
            if len(grades) == 5:
                admin.update_grades(uid, grades)
                messagebox.showinfo("Success", "Grades updated.")
            else:
                messagebox.showerror("Error", "Please enter exactly 5 marks.")

    def update_eca():
        uid = tk.simpledialog.askstring("Student ID", "Enter student ID:")
        activities = tk.simpledialog.askstring("Activities", "Enter activities (semicolon-separated):")
        if uid and activities:
            admin.update_eca(uid, activities.split(';'))
            messagebox.showinfo("Success", "ECA updated.")

    def generate_insights():
        grades = read_file("data/grades.txt")
        eca = read_file("data/eca.txt")

        lines = [line.split(',') for line in grades if len(line.split(',')) == 6]
        total = [0]*5
        count = len(lines)
        if count > 0:
            for line in lines:
                marks = list(map(int, line[1:]))
                for i in range(5):
                    total[i] += marks[i]
            avg = [t / count for t in total]
            grade_report = "\n".join([f"Subject {i+1}: {a:.2f}" for i, a in enumerate(avg)])
        else:
            grade_report = "No grade data available."

        activity_counts = [(line.split(',')[0], len(line.split(',')[1].split(';'))) for line in eca if ',' in line]
        activity_counts.sort(key=lambda x: x[1], reverse=True)
        top_eca = "\n".join([f"{uid} - {count} activities" for uid, count in activity_counts[:3]]) or "No ECA data."

        report = f"--- Average Grades ---\n{grade_report}\n\n--- Top 3 ECA Students ---\n{top_eca}"
        messagebox.showinfo("Insights", report)

    tk.Label(root, text=f"Welcome, Admin {admin.name}", font=("Helvetica", 16)).pack(pady=10)

    tk.Button(root, text="Add User", width=30, command=add_user).pack(pady=5)
    tk.Button(root, text="Update User", width=30, command=update_user).pack(pady=5)
    tk.Button(root, text="Delete User", width=30, command=delete_user).pack(pady=5)
    tk.Button(root, text="Update Grades", width=30, command=update_grades).pack(pady=5)
    tk.Button(root, text="Update ECA", width=30, command=update_eca).pack(pady=5)
    tk.Button(root, text="Generate Insights", width=30, command=generate_insights).pack(pady=5)
    tk.Button(root, text="Logout", width=30, command=root.destroy).pack(pady=20)

    root.mainloop()
