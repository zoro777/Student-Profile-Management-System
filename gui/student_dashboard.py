import tkinter as tk
from tkinter import messagebox

def open_student_dashboard(student):
    root = tk.Tk()
    root.title(f"Student Dashboard - {student.name}")
    root.geometry("400x400")

    user_data = {
        "username": "",
        "email": "",
        "role": ""
    }

    try:
        with open("data/users.txt", "r") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) >= 4 and parts[0] == student.user_id:
                    user_data["username"] = parts[0]
                    student.name = parts[1]
                    user_data["email"] = parts[2]
                    user_data["role"] = parts[3]
                    break
    except FileNotFoundError:
        messagebox.showerror("Error", "User data file not found.")
        root.destroy()
        return

    def view_profile():
        info = (
            f"Username: {user_data['username']}\n"
            f"Full Name: {student.name}\n"
            f"Email: {user_data['email']}\n"
            f"Role: {user_data['role']}"
        )
        messagebox.showinfo("Profile Info", info)

    def update_profile():
        update_window = tk.Toplevel(root)
        update_window.title("Update Profile")
        update_window.geometry("300x200")
        update_window.grab_set()

        tk.Label(update_window, text="Full Name:").pack(pady=(10, 0))
        name_entry = tk.Entry(update_window)
        name_entry.insert(0, student.name)
        name_entry.pack()

        tk.Label(update_window, text="Email:").pack(pady=(10, 0))
        email_entry = tk.Entry(update_window)
        email_entry.insert(0, user_data["email"])
        email_entry.pack()

        def save_updates():
            new_name = name_entry.get().strip()
            new_email = email_entry.get().strip()

            if not new_name or not new_email:
                messagebox.showerror("Error", "All fields are required.")
                return

            student.name = new_name
            user_data["email"] = new_email

            updated = False
            try:
                with open("data/users.txt", "r") as f:
                    lines = f.readlines()

                with open("data/users.txt", "w") as f:
                    for line in lines:
                        parts = line.strip().split(",")
                        if len(parts) >= 4 and parts[0] == user_data["username"]:
                            new_line = f"{user_data['username']},{new_name},{new_email},{user_data['role']}\n"
                            f.write(new_line)
                            updated = True
                        else:
                            f.write(line)

                if updated:
                    messagebox.showinfo("Success", "Profile updated successfully!")
                    update_window.destroy()
                else:
                    messagebox.showerror("Error", "User ID not found. No changes made.")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to update profile: {e}")

        tk.Button(update_window, text="Save", command=save_updates).pack(pady=20)

    def view_grades():
        grades = student.get_grades()
        if grades:
            messagebox.showinfo("Grades", "\n".join([f"Subject {i+1}: {m}" for i, m in enumerate(grades)]))
        else:
            messagebox.showinfo("Grades", "No grades available.")

    def view_eca():
        eca = student.get_eca()
        if eca:
            messagebox.showinfo("ECA", "Activities:\n" + "\n".join(eca))
        else:
            messagebox.showinfo("ECA", "No extracurricular activities recorded.")

    tk.Label(root, text=f"Welcome, {student.name}", font=("Helvetica", 16)).pack(pady=10)
    tk.Button(root, text="View Profile", width=25, command=view_profile).pack(pady=5)
    tk.Button(root, text="Update Profile", width=25, command=update_profile).pack(pady=5)
    tk.Button(root, text="View Grades", width=25, command=view_grades).pack(pady=5)
    tk.Button(root, text="View ECA", width=25, command=view_eca).pack(pady=5)
    tk.Button(root, text="Logout", width=25, command=root.destroy).pack(pady=20)

    root.mainloop()
