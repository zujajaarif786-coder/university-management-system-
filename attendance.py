"""
attendance.py - Attendance Management Module
"""
from models import Student
from utils import (load_json, save_json, get_input,
                   print_header, print_success, print_error,
                   print_info, print_divider, Colors, cprint, today_str)


STUDENT_FILE = "students.json"


def _load_students() -> list[Student]:
    return [Student.from_dict(d) for d in load_json(STUDENT_FILE)]

def _save_students(students: list[Student]):
    save_json(STUDENT_FILE, [s.to_dict() for s in students])


class AttendanceManager:

    def mark_attendance(self):
        print_header("MARK ATTENDANCE")
        students = _load_students()
        cid = get_input("Course ID")

        # Filter students enrolled in this course
        enrolled = [s for s in students if cid in s.courses]
        if not enrolled:
            print_info("No students enrolled in this course.")
            return

        print_info(f"Marking attendance for {today_str()} — Course: {cid}")
        for student in enrolled:
            cprint(f"\n  Student: {student.name} ({student.person_id})", Colors.CYAN)
            status = input("  Present? (y/n): ").strip().lower()
            student.mark_attendance(cid, status == 'y')

        _save_students(students)
        print_success("Attendance marked successfully.")

    def generate_report(self):
        print_header("ATTENDANCE REPORT")
        students = _load_students()
        cid = get_input("Course ID (leave blank for all courses)", required=False)

        enrolled = [s for s in students if (cid in s.courses if cid else True)]
        if not enrolled:
            print_info("No data found.")
            return

        for student in enrolled:
            print_divider()
            cprint(f"  {student.name} ({student.person_id})", Colors.BOLD + Colors.CYAN)
            if cid:
                pct = student.get_attendance_percentage(cid)
                att = student.attendance.get(cid, {"present": 0, "total": 0})
                status_color = Colors.GREEN if pct >= 75 else Colors.RED
                cprint(f"    Course {cid}: {att['present']}/{att['total']} "
                       f"= {pct}%", status_color)
            else:
                for course_id in student.courses:
                    pct = student.get_attendance_percentage(course_id)
                    att = student.attendance.get(course_id, {"present": 0, "total": 0})
                    status_color = Colors.GREEN if pct >= 75 else Colors.RED
                    cprint(f"    Course {course_id}: {att['present']}/{att['total']} "
                           f"= {pct}%", status_color)
        print_divider()
        print_info("Students with < 75% attendance are shown in red.")

    def view_student_attendance(self):
        """For student self-view."""
        print_header("MY ATTENDANCE")
        students = _load_students()
        sid = get_input("Your Student ID")
        student = next((s for s in students if s.person_id == sid), None)
        if not student:
            print_error("Student not found.")
            return
        if not student.courses:
            print_info("You are not enrolled in any courses.")
            return
        print_divider()
        cprint(f"  Attendance for {student.name}", Colors.BOLD + Colors.CYAN)
        for cid in student.courses:
            pct = student.get_attendance_percentage(cid)
            att = student.attendance.get(cid, {"present": 0, "total": 0})
            color = Colors.GREEN if pct >= 75 else Colors.RED
            cprint(f"  {cid}: {att['present']}/{att['total']} classes = {pct}%", color)

    def menu(self):
        while True:
            print_header("ATTENDANCE SYSTEM")
            for o in ["1. Mark Attendance","2. Generate Attendance Report",
                      "3. View My Attendance (Student)","0. Back"]:
                cprint(o, Colors.YELLOW)
            choice = input("\n  Select option: ").strip()
            if   choice == "1": self.mark_attendance()
            elif choice == "2": self.generate_report()
            elif choice == "3": self.view_student_attendance()
            elif choice == "0": break
            else: print_error("Invalid option.")
