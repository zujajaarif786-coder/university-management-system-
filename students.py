"""
students.py - Student Management Module
"""
from models import Student
from utils import (load_json, save_json, get_input, get_int_input,
                   print_header, print_success, print_error,
                   print_info, print_divider, confirm, Colors, cprint)


STUDENT_FILE = "students.json"


def _load_students() -> list[Student]:
    return [Student.from_dict(d) for d in load_json(STUDENT_FILE)]

def _save_students(students: list[Student]):
    save_json(STUDENT_FILE, [s.to_dict() for s in students])

def _find_student(students: list[Student], sid: str) -> Student | None:
    return next((s for s in students if s.person_id == sid), None)


class StudentManager:
    """Handles all student management operations."""

    # ── Add student ───────────────────────────────────────────
    def add_student(self):
        print_header("ADD STUDENT")
        students = _load_students()
        sid = get_input("Student ID (e.g. STU001)")
        if _find_student(students, sid):
            print_error("Student ID already exists.")
            return

        name   = get_input("Full Name")
        email  = get_input("Email")
        pwd    = get_input("Password (min 6 chars)")
        dept   = get_input("Department")
        sem    = get_int_input("Semester (1-8)", 1, 8)
        phone  = get_input("Phone Number", required=False)

        try:
            student = Student(sid, name, email, pwd, dept, sem, phone)
            students.append(student)
            _save_students(students)
            print_success(f"Student '{name}' added successfully.")
        except ValueError as e:
            print_error(str(e))

    # ── Update student ────────────────────────────────────────
    def update_student(self):
        print_header("UPDATE STUDENT")
        students = _load_students()
        sid = get_input("Enter Student ID to update")
        student = _find_student(students, sid)
        if not student:
            print_error("Student not found.")
            return

        print_info(f"Updating: {student.name}  (leave blank to skip)")
        name  = get_input("New Name", required=False) or student.name
        email = get_input("New Email", required=False) or student.email
        dept  = get_input("New Department", required=False) or student.department
        phone = get_input("New Phone", required=False) or student.phone

        try:
            student.name       = name
            student.email      = email
            student.department = dept
            student.phone      = phone
            _save_students(students)
            print_success("Student updated successfully.")
        except ValueError as e:
            print_error(str(e))

    # ── Delete student ────────────────────────────────────────
    def delete_student(self):
        print_header("DELETE STUDENT")
        students = _load_students()
        sid = get_input("Enter Student ID to delete")
        student = _find_student(students, sid)
        if not student:
            print_error("Student not found.")
            return

        print_info(f"About to delete: {student.name}")
        if confirm("Confirm deletion?"):
            students = [s for s in students if s.person_id != sid]
            _save_students(students)
            print_success("Student deleted.")
        else:
            print_info("Deletion cancelled.")

    # ── Search student ────────────────────────────────────────
    def search_student(self):
        print_header("SEARCH STUDENT")
        students = _load_students()
        keyword = get_input("Search by ID or Name").lower()

        results = [s for s in students
                   if keyword in s.person_id.lower() or keyword in s.name.lower()]
        if not results:
            print_error("No students found.")
            return
        for s in results:
            print_divider()
            cprint(s.display_info(), Colors.CYAN)

    # ── Display all ───────────────────────────────────────────
    def display_all_students(self):
        print_header("ALL STUDENTS")
        students = _load_students()
        if not students:
            print_info("No students registered.")
            return
        for s in students:
            print_divider()
            cprint(s.display_info(), Colors.CYAN)
        print_divider()
        print_info(f"Total: {len(students)} student(s)")

    # ── Student menu ──────────────────────────────────────────
    def menu(self):
        while True:
            print_header("STUDENT MANAGEMENT")
            options = [
                "1. Add Student",
                "2. Update Student",
                "3. Delete Student",
                "4. Search Student",
                "5. Display All Students",
                "0. Back",
            ]
            for o in options:
                cprint(o, Colors.YELLOW)
            choice = input("\n  Select option: ").strip()
            if   choice == "1": self.add_student()
            elif choice == "2": self.update_student()
            elif choice == "3": self.delete_student()
            elif choice == "4": self.search_student()
            elif choice == "5": self.display_all_students()
            elif choice == "0": break
            else: print_error("Invalid option.")
