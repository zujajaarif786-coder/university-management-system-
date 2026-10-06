"""
models.py - OOP class hierarchy for University Management System

Demonstrates:
  • Abstraction  - Abstract base class 'Person' with abstract methods
  • Inheritance  - Student, Teacher, Admin extend Person
  • Encapsulation- Private attributes with getters/setters
  • Polymorphism - display_info() overridden in every subclass
"""

from abc import ABC, abstractmethod
from utils import hash_password, calculate_grade, now_str


# ══════════════════════════════════════════════════════════════
#  ABSTRACTION  –  Abstract base class
# ══════════════════════════════════════════════════════════════
class Person(ABC):
    """Abstract base class for all university members."""

    def __init__(self, person_id: str, name: str, email: str, password: str):
        # ENCAPSULATION: private attributes
        self.__person_id: str = person_id
        self.__name: str      = name
        self.__email: str     = email
        self.__password: str  = hash_password(password) if len(password) != 64 else password
        self._role: str       = "person"   # protected, overridden by child classes

    # ── Getters ────────────────────────────────────────────────
    @property
    def person_id(self) -> str:
        return self.__person_id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def email(self) -> str:
        return self.__email

    @property
    def password(self) -> str:
        return self.__password

    @property
    def role(self) -> str:
        return self._role

    # ── Setters ────────────────────────────────────────────────
    @name.setter
    def name(self, value: str):
        if not value.strip():
            raise ValueError("Name cannot be empty.")
        self.__name = value.strip()

    @email.setter
    def email(self, value: str):
        if "@" not in value:
            raise ValueError("Invalid email address.")
        self.__email = value.strip()

    def set_password(self, raw_password: str):
        if len(raw_password) < 6:
            raise ValueError("Password must be at least 6 characters.")
        self.__password = hash_password(raw_password)

    # ── Abstract methods (Abstraction) ────────────────────────
    @abstractmethod
    def display_info(self) -> str:
        """Every subclass must implement its own display."""
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        """Serialize to dictionary for JSON storage."""
        pass

    # ── Common ───────────────────────────────────────────────
    def verify_password(self, raw_password: str) -> bool:
        return self.__password == hash_password(raw_password)

    def __str__(self) -> str:
        return self.display_info()


# ══════════════════════════════════════════════════════════════
#  INHERITANCE  –  Student
# ══════════════════════════════════════════════════════════════
class Student(Person):
    """Student inherits from Person and adds academic details."""

    def __init__(self, student_id: str, name: str, email: str, password: str,
                 department: str = "", semester: int = 1, phone: str = ""):
        super().__init__(student_id, name, email, password)
        self._role        = "student"
        self.__department = department
        self.__semester   = semester
        self.__phone      = phone
        self.__courses: list[str]     = []   # list of course_ids
        self.__attendance: dict       = {}   # {course_id: {"present": int, "total": int}}
        self.__results: dict          = {}   # {course_id: {"marks": float, "grade": str}}

    # ── Getters / Setters ─────────────────────────────────────
    @property
    def department(self): return self.__department
    @department.setter
    def department(self, v): self.__department = v

    @property
    def semester(self): return self.__semester
    @semester.setter
    def semester(self, v):
        if not (1 <= v <= 8):
            raise ValueError("Semester must be between 1 and 8.")
        self.__semester = v

    @property
    def phone(self): return self.__phone
    @phone.setter
    def phone(self, v): self.__phone = v

    @property
    def courses(self): return list(self.__courses)

    @property
    def attendance(self): return dict(self.__attendance)

    @property
    def results(self): return dict(self.__results)

    # ── Business logic ────────────────────────────────────────
    def enroll_course(self, course_id: str):
        if course_id not in self.__courses:
            self.__courses.append(course_id)
            self.__attendance[course_id] = {"present": 0, "total": 0}

    def drop_course(self, course_id: str):
        if course_id in self.__courses:
            self.__courses.remove(course_id)

    def mark_attendance(self, course_id: str, present: bool):
        if course_id not in self.__attendance:
            self.__attendance[course_id] = {"present": 0, "total": 0}
        self.__attendance[course_id]["total"]  += 1
        if present:
            self.__attendance[course_id]["present"] += 1

    def add_result(self, course_id: str, marks: float):
        grade, gp = calculate_grade(marks)
        self.__results[course_id] = {"marks": marks, "grade": grade, "grade_points": gp}

    def calculate_gpa(self) -> float:
        if not self.__results:
            return 0.0
        total_gp = sum(v["grade_points"] for v in self.__results.values())
        return round(total_gp / len(self.__results), 2)

    def get_attendance_percentage(self, course_id: str) -> float:
        att = self.__attendance.get(course_id, {"present": 0, "total": 0})
        if att["total"] == 0:
            return 0.0
        return round((att["present"] / att["total"]) * 100, 2)

    # ── POLYMORPHISM: override display_info ───────────────────
    def display_info(self) -> str:
        return (f"[STUDENT] ID: {self.person_id} | Name: {self.name} | "
                f"Dept: {self.__department} | Sem: {self.__semester} | "
                f"Email: {self.email} | GPA: {self.calculate_gpa()}")

    def to_dict(self) -> dict:
        return {
            "student_id":  self.person_id,
            "name":        self.name,
            "email":       self.email,
            "password":    self.password,
            "department":  self.__department,
            "semester":    self.__semester,
            "phone":       self.__phone,
            "courses":     self.__courses,
            "attendance":  self.__attendance,
            "results":     self.__results,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Student":
        s = cls(d["student_id"], d["name"], d["email"], d["password"],
                d.get("department",""), d.get("semester",1), d.get("phone",""))
        s._Student__courses    = d.get("courses", [])
        s._Student__attendance = d.get("attendance", {})
        s._Student__results    = d.get("results", {})
        return s


# ══════════════════════════════════════════════════════════════
#  INHERITANCE  –  Teacher
# ══════════════════════════════════════════════════════════════
class Teacher(Person):
    """Teacher inherits from Person and adds professional details."""

    def __init__(self, teacher_id: str, name: str, email: str, password: str,
                 department: str = "", designation: str = "", phone: str = ""):
        super().__init__(teacher_id, name, email, password)
        self._role           = "teacher"
        self.__department    = department
        self.__designation   = designation
        self.__phone         = phone
        self.__subjects: list[str]  = []   # list of course_ids assigned
        self.__courses: list[str]   = []   # alias

    @property
    def department(self): return self.__department
    @department.setter
    def department(self, v): self.__department = v

    @property
    def designation(self): return self.__designation
    @designation.setter
    def designation(self, v): self.__designation = v

    @property
    def phone(self): return self.__phone
    @phone.setter
    def phone(self, v): self.__phone = v

    @property
    def subjects(self): return list(self.__subjects)

    def assign_subject(self, course_id: str):
        if course_id not in self.__subjects:
            self.__subjects.append(course_id)

    def remove_subject(self, course_id: str):
        if course_id in self.__subjects:
            self.__subjects.remove(course_id)

    # ── POLYMORPHISM: override display_info ───────────────────
    def display_info(self) -> str:
        return (f"[TEACHER] ID: {self.person_id} | Name: {self.name} | "
                f"Dept: {self.__department} | Designation: {self.__designation} | "
                f"Email: {self.email} | Subjects: {len(self.__subjects)}")

    def to_dict(self) -> dict:
        return {
            "teacher_id":   self.person_id,
            "name":         self.name,
            "email":        self.email,
            "password":     self.password,
            "department":   self.__department,
            "designation":  self.__designation,
            "phone":        self.__phone,
            "subjects":     self.__subjects,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Teacher":
        t = cls(d["teacher_id"], d["name"], d["email"], d["password"],
                d.get("department",""), d.get("designation",""), d.get("phone",""))
        t._Teacher__subjects = d.get("subjects", [])
        return t


# ══════════════════════════════════════════════════════════════
#  INHERITANCE  –  Admin
# ══════════════════════════════════════════════════════════════
class Admin(Person):
    """Admin inherits from Person with elevated privileges."""

    def __init__(self, admin_id: str, name: str, email: str, password: str):
        super().__init__(admin_id, name, email, password)
        self._role = "admin"

    # ── POLYMORPHISM: override display_info ───────────────────
    def display_info(self) -> str:
        return (f"[ADMIN] ID: {self.person_id} | Name: {self.name} | "
                f"Email: {self.email}")

    def to_dict(self) -> dict:
        return {
            "admin_id": self.person_id,
            "name":     self.name,
            "email":    self.email,
            "password": self.password,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Admin":
        return cls(d["admin_id"], d["name"], d["email"], d["password"])


# ══════════════════════════════════════════════════════════════
#  Course model  (plain class, not a Person)
# ══════════════════════════════════════════════════════════════
class Course:
    def __init__(self, course_id: str, name: str, credits: int,
                 department: str = "", teacher_id: str = ""):
        self.__course_id   = course_id
        self.__name        = name
        self.__credits     = credits
        self.__department  = department
        self.__teacher_id  = teacher_id
        self.__students: list[str] = []

    @property
    def course_id(self): return self.__course_id
    @property
    def name(self): return self.__name
    @name.setter
    def name(self, v): self.__name = v
    @property
    def credits(self): return self.__credits
    @property
    def department(self): return self.__department
    @property
    def teacher_id(self): return self.__teacher_id
    @teacher_id.setter
    def teacher_id(self, v): self.__teacher_id = v
    @property
    def students(self): return list(self.__students)

    def add_student(self, sid: str):
        if sid not in self.__students:
            self.__students.append(sid)

    def remove_student(self, sid: str):
        if sid in self.__students:
            self.__students.remove(sid)

    def __str__(self):
        return (f"[COURSE] {self.__course_id} | {self.__name} | "
                f"Credits: {self.__credits} | Dept: {self.__department} | "
                f"Teacher: {self.__teacher_id or 'Unassigned'} | "
                f"Students: {len(self.__students)}")

    def to_dict(self) -> dict:
        return {
            "course_id":  self.__course_id,
            "name":       self.__name,
            "credits":    self.__credits,
            "department": self.__department,
            "teacher_id": self.__teacher_id,
            "students":   self.__students,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Course":
        c = cls(d["course_id"], d["name"], d["credits"],
                d.get("department",""), d.get("teacher_id",""))
        c._Course__students = d.get("students", [])
        return c


# ══════════════════════════════════════════════════════════════
#  Fee Record model
# ══════════════════════════════════════════════════════════════
class FeeRecord:
    def __init__(self, student_id: str, total_fee: float,
                 paid: float = 0.0, semester: int = 1):
        self.__student_id = student_id
        self.__total_fee  = total_fee
        self.__paid       = paid
        self.__semester   = semester
        self.__payments: list[dict] = []

    @property
    def student_id(self): return self.__student_id
    @property
    def total_fee(self): return self.__total_fee
    @property
    def paid(self): return self.__paid
    @property
    def due(self): return round(self.__total_fee - self.__paid, 2)
    @property
    def semester(self): return self.__semester
    @property
    def payments(self): return list(self.__payments)

    def add_payment(self, amount: float, note: str = ""):
        if amount <= 0:
            raise ValueError("Payment amount must be positive.")
        if amount > self.due:
            raise ValueError(f"Payment exceeds due amount ({self.due}).")
        self.__paid += amount
        self.__payments.append({
            "amount": amount,
            "date": now_str(),
            "note": note
        })

    def to_dict(self) -> dict:
        return {
            "student_id": self.__student_id,
            "semester":   self.__semester,
            "total_fee":  self.__total_fee,
            "paid":       self.__paid,
            "payments":   self.__payments,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "FeeRecord":
        fr = cls(d["student_id"], d["total_fee"], d["paid"], d.get("semester",1))
        fr._FeeRecord__payments = d.get("payments", [])
        return fr
