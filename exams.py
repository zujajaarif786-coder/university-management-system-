"""
exams.py - Examination & Result System
"""
from models import Student
from utils import (load_json, save_json, get_input, get_float_input,
                   print_header, print_success, print_error,
                   print_info, print_divider, calculate_grade, Colors, cprint, now_str)


STUDENT_FILE = "students.json"


def _load_students() -> list[Student]:
    return [Student.from_dict(d) for d in load_json(STUDENT_FILE)]

def _save_students(students: list[Student]):
    save_json(STUDENT_FILE, [s.to_dict() for s in students])


class ExamManager:

    def add_marks(self):
        print_header("ADD / UPDATE MARKS")
        students = _load_students()
        sid = get_input("Student ID")
        student = next((s for s in students if s.person_id == sid), None)
        if not student:
            print_error("Student not found.")
            return

        if not student.courses:
            print_info("Student is not enrolled in any course.")
            return

        cprint(f"  Enrolled courses: {', '.join(student.courses)}", Colors.CYAN)
        cid = get_input("Course ID")
        if cid not in student.courses:
            print_error("Student is not enrolled in this course.")
            return

        marks = get_float_input("Marks obtained (0-100)", 0, 100)
        student.add_result(cid, marks)
        _save_students(students)
        grade, _ = calculate_grade(marks)
        print_success(f"Marks recorded. Grade: {grade}")

    def view_results(self):
        print_header("VIEW STUDENT RESULTS")
        students = _load_students()
        sid = get_input("Student ID")
        student = next((s for s in students if s.person_id == sid), None)
        if not student:
            print_error("Student not found.")
            return
        self._print_result_card(student)

    def _print_result_card(self, student: Student):
        print_divider()
        cprint(f"  RESULT CARD — {student.name} ({student.person_id})", Colors.BOLD + Colors.CYAN)
        cprint(f"  Department: {student.department} | Semester: {student.semester}", Colors.CYAN)
        print_divider()
        if not student.results:
            print_info("  No results available.")
            return
        cprint(f"  {'Course':<15} {'Marks':>8} {'Grade':>8} {'GP':>6}", Colors.BOLD)
        print_divider()
        for cid, res in student.results.items():
            grade_color = Colors.GREEN if res["grade"] not in ("D","F") else Colors.RED
            cprint(f"  {cid:<15} {res['marks']:>8.2f} {res['grade']:>8} "
                   f"{res['grade_points']:>6.1f}", grade_color)
        print_divider()
        gpa = student.calculate_gpa()
        gpa_color = Colors.GREEN if gpa >= 2.0 else Colors.RED
        cprint(f"  {'GPA':>33}  {gpa:>5.2f}", gpa_color + Colors.BOLD)
        print_divider()

    def generate_result_cards(self):
        """Generate result cards for all students in a course."""
        print_header("RESULT CARDS — COURSE")
        students = _load_students()
        cid = get_input("Course ID")
        enrolled = [s for s in students if cid in s.courses]
        if not enrolled:
            print_info("No students enrolled in this course.")
            return
        for student in enrolled:
            self._print_result_card(student)

    def toppers_list(self):
        """Bonus: Topper list."""
        print_header("TOPPERS LIST (by GPA)")
        students = _load_students()
        ranked = sorted(students, key=lambda s: s.calculate_gpa(), reverse=True)
        print_divider()
        cprint(f"  {'Rank':<6} {'Name':<20} {'ID':<10} {'GPA':>6}", Colors.BOLD)
        print_divider()
        for i, s in enumerate(ranked[:10], 1):
            gpa = s.calculate_gpa()
            color = Colors.GREEN if i == 1 else (Colors.CYAN if i <= 3 else Colors.RESET)
            cprint(f"  {i:<6} {s.name:<20} {s.person_id:<10} {gpa:>6.2f}", color)
        print_divider()

    def menu(self):
        while True:
            print_header("EXAMINATION & RESULT SYSTEM")
            for o in ["1. Add / Update Marks","2. View Student Result",
                      "3. Generate Course Result Cards","4. Toppers List","0. Back"]:
                cprint(o, Colors.YELLOW)
            choice = input("\n  Select option: ").strip()
            if   choice == "1": self.add_marks()
            elif choice == "2": self.view_results()
            elif choice == "3": self.generate_result_cards()
            elif choice == "4": self.toppers_list()
            elif choice == "0": break
            else: print_error("Invalid option.")
