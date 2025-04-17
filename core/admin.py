from core.user import User
from utils.file_utils import read_file, write_file, update_line, delete_line

class Admin(User):
    def __init__(self, user_id, name):
        super().__init__(user_id, name, "admin")

    def add_user(self, user_id, name, email, role, password):
        from utils.file_utils import update_line
        update_line("data/users.txt", user_id, f"{user_id},{name},{email},{role}")
        update_line("data/passwords.txt", user_id, f"{user_id},{password}")



    def update_user(self, user_id, new_name):
        lines = read_file("data/users.txt")
        for i, line in enumerate(lines):
            uid, _, role = line.split(',')
            if uid == user_id:
                lines[i] = f"{uid},{new_name},{role}"
                break
        write_file("data/users.txt", lines)

    def delete_user(self, user_id):
        for filename in ["data/users.txt", "data/passwords.txt", "data/grades.txt", "data/eca.txt"]:
            delete_line(filename, user_id)

    def update_grades(self, user_id, grades):
        update_line("data/grades.txt", user_id, f"{user_id},{','.join(grades)}")

    def update_eca(self, user_id, activities):
        update_line("data/eca.txt", user_id, f"{user_id},{';'.join(activities)}")
