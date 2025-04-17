from core.user import User
from utils.file_utils import read_file, write_file, update_line

class Student(User):
    def __init__(self, user_id, name):
        super().__init__(user_id, name, "student")

    def update_profile(self, name=None, username=None, email=None):
    # Preserve current values if not updated
        if name is None:
            name = self.name
        if username is None:
            username = self.username
        if email is None:
            email = self.email

    # Update instance attributes
        self.name = name
        self.username = username
        self.email = email

    # Construct the updated line
        updated_line = f"{self.user_id},{self.username},{self.name},{self.email},{self.role}"

    # Call your existing function to update the text file
        update_line("data/users.txt", self.user_id, updated_line)


    def get_grades(self):
        lines = read_file("data/grades.txt")
        for line in lines:
            if line.startswith(self.user_id + ","):
                return line.split(',')[1:]
        return []

    def get_eca(self):
        lines = read_file("data/eca.txt")
        for line in lines:
            if line.startswith(self.user_id + ","):
                return line.split(',')[1].split(';')
        return []
