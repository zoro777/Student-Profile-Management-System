import tkinter as tk
from tkinter import messagebox, simpledialog

def open_student_dashboard(student):
    root = tk.Tk()
    root.title(f"Student Dashboard - {student.name}")
    root.geometry("400x400")

    # Load username and email from users.txt
    user_data = {
        "username": "",
        "email": ""
    }

    try:
        with open("data/users.txt", "r") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) >= 5 and parts[0] == student.user_id:
                    # Format: user_id, username, name, email, role
                    user_data["username"] = parts[1]
                    student.name = parts[2]  # Correct full name
                    user_data["email"] = parts[3]
                    student.role = parts[4]
                    break
    except FileNotFoundError:
        messagebox.showerror("Error", "User data file not found.")
        root.destroy()
        return

    def view_profile():
        info = (
            f"ID: {student.user_id}\n"
            f"Username: {user_data['username']}\n"
            f"Name: {student.name}\n"
            f"Email: {user_data['email']}\n"
            f"Role: {student.role}"
        )
        messagebox.showinfo("Profile Info", info)

    def update_profile():
        update_window = tk.Toplevel(root)
        update_window.title("Update Profile")
        update_window.geometry("300x250")
        update_window.grab_set()

        tk.Label(update_window, text="Username:").pack(pady=(10, 0))
        username_entry = tk.Entry(update_window)
        username_entry.insert(0, user_data["username"])
        username_entry.pack()

        tk.Label(update_window, text="Full Name:").pack(pady=(10, 0))
        name_entry = tk.Entry(update_window)
        name_entry.insert(0, student.name)
        name_entry.pack()

        tk.Label(update_window, text="Email:").pack(pady=(10, 0))
        email_entry = tk.Entry(update_window)
        email_entry.insert(0, user_data["email"])
        email_entry.pack()

        def save_updates():
            new_username = username_entry.get().strip()
            new_name = name_entry.get().strip()
            new_email = email_entry.get().strip()

            if not new_username or not new_name or not new_email:
                messagebox.showerror("Error", "All fields are required.")
                return

            # Update local values
            user_data["username"] = new_username
            user_data["email"] = new_email
            student.name = new_name

            # Update file properly (match by user_id)
            try:
                with open("data/users.txt", "r") as f:
                    lines = f.readlines()

                with open("data/users.txt", "w") as f:
                    for line in lines:
                        parts = line.strip().split(",")
                        if parts[0] == student.user_id:
                            updated_line = f"{student.user_id},{new_username},{new_name},{new_email},{student.role}\n"
                            f.write(updated_line)
                        else:
                            f.write(line)
                messagebox.showinfo("Success", "Profile updated successfully!")
                update_window.destroy()

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
