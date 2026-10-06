"""
teachers.py - Teacher Management Module
"""
from models import Teacher
from utils import (load_json, save_json, get_input,
                   print_header, print_success, print_error,
                   print_info, print_divider, confirm, Colors, cprint)


TEACHER_FILE = "teachers.json"


def _load_teachers() -> list[Teacher]:
    return [Teacher.from_dict(d) for d in load_json(TEACHER_FILE)]

def _save_teachers(teachers: list[Teacher]):
    save_json(TEACHER_FILE, [t.to_dict() for t in teachers])

def _find_teacher(teachers: list[Teacher], tid: str) -> Teacher | None:
    return next((t for t in teachers if t.person_id == tid), None)


class TeacherManager:

    def add_teacher(self):
        print_header("ADD TEACHER")
        teachers = _load_teachers()
        tid = get_input("Teacher ID (e.g. TCH001)")
        if _find_teacher(teachers, tid):
            print_error("Teacher ID already exists.")
            return

        name  = get_input("Full Name")
        email = get_input("Email")
        pwd   = get_input("Password (min 6 chars)")
        dept  = get_input("Department")
        desig = get_input("Designation (e.g. Lecturer, Professor)")
        phone = get_input("Phone", required=False)

        try:
            teacher = Teacher(tid, name, email, pwd, dept, desig, phone)
            teachers.append(teacher)
            _save_teachers(teachers)
            print_success(f"Teacher '{name}' added successfully.")
        except ValueError as e:
            print_error(str(e))

    def assign_subjects(self):
        print_header("ASSIGN SUBJECTS TO TEACHER")
        teachers = _load_teachers()
        tid = get_input("Teacher ID")
        teacher = _find_teacher(teachers, tid)
        if not teacher:
            print_error("Teacher not found.")
            return

        course_id = get_input("Course ID to assign")
        teacher.assign_subject(course_id)
        _save_teachers(teachers)
        print_success(f"Course '{course_id}' assigned to {teacher.name}.")

    def view_teacher(self):
        print_header("VIEW TEACHER DETAILS")
        teachers = _load_teachers()
        tid = get_input("Teacher ID")
        teacher = _find_teacher(teachers, tid)
        if not teacher:
            print_error("Teacher not found.")
            return
        print_divider()
        cprint(teacher.display_info(), Colors.CYAN)
        cprint(f"  Subjects assigned: {', '.join(teacher.subjects) or 'None'}", Colors.YELLOW)

    def display_all_teachers(self):
        print_header("ALL TEACHERS")
        teachers = _load_teachers()
        if not teachers:
            print_info("No teachers registered.")
            return
        for t in teachers:
            print_divider()
            cprint(t.display_info(), Colors.CYAN)
        print_divider()
        print_info(f"Total: {len(teachers)} teacher(s)")

    def update_teacher(self):
        print_header("UPDATE TEACHER")
        teachers = _load_teachers()
        tid = get_input("Teacher ID to update")
        teacher = _find_teacher(teachers, tid)
        if not teacher:
            print_error("Teacher not found.")
            return
        print_info(f"Updating: {teacher.name}  (leave blank to skip)")
        name  = get_input("New Name", required=False) or teacher.name
        email = get_input("New Email", required=False) or teacher.email
        dept  = get_input("New Department", required=False) or teacher.department
        desig = get_input("New Designation", required=False) or teacher.designation
        phone = get_input("New Phone", required=False) or teacher.phone

        try:
            teacher.name        = name
            teacher.email       = email
            teacher.department  = dept
            teacher.designation = desig
            teacher.phone       = phone
            _save_teachers(teachers)
            print_success("Teacher updated.")
        except ValueError as e:
            print_error(str(e))

    def menu(self):
        while True:
            print_header("TEACHER MANAGEMENT")
            options = [
                "1. Add Teacher",
                "2. Update Teacher",
                "3. Assign Subject",
                "4. View Teacher Details",
                "5. Display All Teachers",
                "0. Back",
            ]
            for o in options: cprint(o, Colors.YELLOW)
            choice = input("\n  Select option: ").strip()
            if   choice == "1": self.add_teacher()
            elif choice == "2": self.update_teacher()
            elif choice == "3": self.assign_subjects()
            elif choice == "4": self.view_teacher()
            elif choice == "5": self.display_all_teachers()
            elif choice == "0": break
            else: print_error("Invalid option.")
