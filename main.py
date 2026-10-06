"""
main.py - Entry Point for Advanced University Management System
Course: Python Programming with OOP
"""
import sys
import os

# Ensure the project directory is on the path
sys.path.insert(0, os.path.dirname(__file__))

from auth       import AuthManager
from students   import StudentManager
from teachers   import TeacherManager
from courses    import CourseManager
from attendance import AttendanceManager
from exams      import ExamManager
from fees       import FeeManager
from utils      import (print_header, print_error, print_info,
                        print_divider, Colors, cprint)


def admin_menu(auth: AuthManager):
    sm  = StudentManager()
    tm  = TeacherManager()
    cm  = CourseManager()
    atm = AttendanceManager()
    em  = ExamManager()
    fm  = FeeManager()

    while True:
        print_header("ADMIN DASHBOARD")
        options = [
            "1. Student Management",
            "2. Teacher Management",
            "3. Course Management",
            "4. Attendance System",
            "5. Examination & Results",
            "6. Fee Management",
            "0. Logout",
        ]
        for o in options: cprint(o, Colors.YELLOW)
        choice = input("\n  Select option: ").strip()
        if   choice == "1": sm.menu()
        elif choice == "2": tm.menu()
        elif choice == "3": cm.menu()
        elif choice == "4": atm.menu()
        elif choice == "5": em.menu()
        elif choice == "6": fm.menu()
        elif choice == "0":
            print_info("Logged out.")
            break
        else:
            print_error("Invalid option.")


def teacher_menu(teacher):
    cm  = CourseManager()
    atm = AttendanceManager()
    em  = ExamManager()

    while True:
        print_header(f"TEACHER DASHBOARD — {teacher.name}")
        options = [
            "1. View My Courses",
            "2. Mark Attendance",
            "3. Attendance Report",
            "4. Add / Update Marks",
            "5. Generate Result Cards",
            "0. Logout",
        ]
        for o in options: cprint(o, Colors.YELLOW)
        choice = input("\n  Select option: ").strip()
        if   choice == "1":
            print_divider()
            cprint(f"  Courses: {', '.join(teacher.subjects) or 'None assigned'}", Colors.CYAN)
        elif choice == "2": atm.mark_attendance()
        elif choice == "3": atm.generate_report()
        elif choice == "4": em.add_marks()
        elif choice == "5": em.generate_result_cards()
        elif choice == "0":
            print_info("Logged out.")
            break
        else:
            print_error("Invalid option.")


def student_menu(student):
    atm = AttendanceManager()
    em  = ExamManager()
    fm  = FeeManager()

    while True:
        print_header(f"STUDENT DASHBOARD — {student.name}")
        options = [
            "1. View My Profile",
            "2. View My Attendance",
            "3. View My Results",
            "4. View Fee Status",
            "0. Logout",
        ]
        for o in options: cprint(o, Colors.YELLOW)
        choice = input("\n  Select option: ").strip()
        if choice == "1":
            print_divider()
            cprint(student.display_info(), Colors.CYAN)
        elif choice == "2":
            atm.view_student_attendance()
        elif choice == "3":
            em.view_results()
        elif choice == "4":
            fm.view_dues()
        elif choice == "0":
            print_info("Logged out.")
            break
        else:
            print_error("Invalid option.")


def main():
    auth = AuthManager()

    while True:
        print_header("ADVANCED UNIVERSITY MANAGEMENT SYSTEM")
        cprint("        Python OOP Final Project", Colors.BOLD)
        print_divider()
        options = [
            "1. Admin Login",
            "2. Teacher Login",
            "3. Student Login",
            "0. Exit",
        ]
        for o in options: cprint(o, Colors.YELLOW)
        choice = input("\n  Select option: ").strip()

        if choice == "1":
            admin = auth.login_admin()
            if admin:
                admin_menu(auth)

        elif choice == "2":
            teacher = auth.login_teacher()
            if teacher:
                teacher_menu(teacher)

        elif choice == "3":
            student = auth.login_student()
            if student:
                student_menu(student)

        elif choice == "0":
            cprint("\n  Thank you for using University Management System. Goodbye!\n",
                   Colors.GREEN + Colors.BOLD)
            sys.exit(0)

        else:
            print_error("Invalid option. Please select 0-3.")


if __name__ == "__main__":
    main()
