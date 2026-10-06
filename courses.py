"""
courses.py - Course Management Module
"""
from models import Course, Student, Teacher
from utils import (load_json, save_json, get_input, get_int_input,
                   print_header, print_success, print_error,
                   print_info, print_divider, Colors, cprint)


COURSE_FILE  = "courses.json"
STUDENT_FILE = "students.json"
TEACHER_FILE = "teachers.json"

def _load_courses() -> list[Course]:
    return [Course.from_dict(d) for d in load_json(COURSE_FILE)]

def _save_courses(courses: list[Course]):
    save_json(COURSE_FILE, [c.to_dict() for c in courses])

def _find_course(courses, cid): return next((c for c in courses if c.course_id == cid), None)


class CourseManager:

    def add_course(self):
        print_header("ADD COURSE")
        courses = _load_courses()
        cid = get_input("Course ID (e.g. CS101)")
        if _find_course(courses, cid):
            print_error("Course ID already exists.")
            return
        name    = get_input("Course Name")
        credits = get_int_input("Credit Hours", 1, 6)
        dept    = get_input("Department")
        course  = Course(cid, name, credits, dept)
        courses.append(course)
        _save_courses(courses)
        print_success(f"Course '{name}' added.")

    def register_student(self):
        print_header("REGISTER STUDENT IN COURSE")
        courses  = _load_courses()
        students = [Student.from_dict(d) for d in load_json(STUDENT_FILE)]

        cid = get_input("Course ID")
        course = _find_course(courses, cid)
        if not course:
            print_error("Course not found.")
            return

        sid = get_input("Student ID")
        student = next((s for s in students if s.person_id == sid), None)
        if not student:
            print_error("Student not found.")
            return

        course.add_student(sid)
        student.enroll_course(cid)
        _save_courses(courses)
        save_json(STUDENT_FILE, [s.to_dict() for s in students])
        print_success(f"Student '{student.name}' enrolled in '{course.name}'.")

    def assign_teacher(self):
        print_header("ASSIGN TEACHER TO COURSE")
        courses  = _load_courses()
        teachers = [Teacher.from_dict(d) for d in load_json(TEACHER_FILE)]

        cid = get_input("Course ID")
        course = _find_course(courses, cid)
        if not course:
            print_error("Course not found.")
            return

        tid = get_input("Teacher ID")
        teacher = next((t for t in teachers if t.person_id == tid), None)
        if not teacher:
            print_error("Teacher not found.")
            return

        course.teacher_id = tid
        teacher.assign_subject(cid)
        _save_courses(courses)
        save_json(TEACHER_FILE, [t.to_dict() for t in teachers])
        print_success(f"Teacher '{teacher.name}' assigned to '{course.name}'.")

    def display_all_courses(self):
        print_header("ALL COURSES")
        courses = _load_courses()
        if not courses:
            print_info("No courses added.")
            return
        for c in courses:
            print_divider()
            cprint(str(c), Colors.CYAN)
        print_divider()
        print_info(f"Total: {len(courses)} course(s)")

    def view_course(self):
        print_header("COURSE DETAILS")
        courses = _load_courses()
        cid = get_input("Course ID")
        course = _find_course(courses, cid)
        if not course:
            print_error("Course not found.")
            return
        print_divider()
        cprint(str(course), Colors.CYAN)
        cprint(f"  Enrolled students: {', '.join(course.students) or 'None'}", Colors.YELLOW)

    def menu(self):
        while True:
            print_header("COURSE MANAGEMENT")
            for o in ["1. Add Course","2. Register Student in Course",
                      "3. Assign Teacher to Course","4. View Course Details",
                      "5. Display All Courses","0. Back"]:
                cprint(o, Colors.YELLOW)
            choice = input("\n  Select option: ").strip()
            if   choice == "1": self.add_course()
            elif choice == "2": self.register_student()
            elif choice == "3": self.assign_teacher()
            elif choice == "4": self.view_course()
            elif choice == "5": self.display_all_courses()
            elif choice == "0": break
            else: print_error("Invalid option.")
