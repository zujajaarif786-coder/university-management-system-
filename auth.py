"""
auth.py - Authentication module for University Management System
Handles login for Admin, Teacher, and Student roles.
"""
import getpass
from models import Admin, Teacher, Student
from utils import (load_json, save_json, hash_password,
                   print_header, print_success, print_error,
                   print_info, get_input, Colors, cprint)


class AuthManager:
    """Manages user authentication across all roles."""

    ADMIN_FILE   = "admins.json"
    TEACHER_FILE = "teachers.json"
    STUDENT_FILE = "students.json"

    def __init__(self):
        self._ensure_default_admin()

    # ── Seed a default admin on first run ─────────────────────
    def _ensure_default_admin(self):
        admins = load_json(self.ADMIN_FILE)
        if not admins:
            default = Admin("ADM001", "Super Admin", "admin@university.edu", "admin123")
            save_json(self.ADMIN_FILE, [default.to_dict()])
            print_info("Default admin created → ID: ADM001 | Password: admin123")

    # ── Generic login helper ──────────────────────────────────
    def _masked_password(self, prompt="  Password: ") -> str:
        """Password masking (Bonus feature)."""
        try:
            return getpass.getpass(prompt)
        except Exception:
            return input(prompt)

    def _login(self, records: list[dict], id_field: str,
               model_cls, role: str):
        """Generic login: returns model instance or None."""
        print_header(f"{role.upper()} LOGIN")
        uid   = get_input(f"{role.capitalize()} ID")
        pwd   = self._masked_password()

        for rec in records:
            if rec[id_field] == uid:
                obj = model_cls.from_dict(rec)
                if obj.verify_password(pwd):
                    print_success(f"Welcome, {obj.name}!")
                    return obj
                else:
                    print_error("Incorrect password.")
                    return None
        print_error(f"{role.capitalize()} ID not found.")
        return None

    # ── Public login methods ──────────────────────────────────
    def login_admin(self) -> Admin | None:
        admins = load_json(self.ADMIN_FILE)
        return self._login(admins, "admin_id", Admin, "admin")

    def login_teacher(self) -> Teacher | None:
        teachers = load_json(self.TEACHER_FILE)
        return self._login(teachers, "teacher_id", Teacher, "teacher")

    def login_student(self) -> Student | None:
        students = load_json(self.STUDENT_FILE)
        return self._login(students, "student_id", Student, "student")

    # ── Registration (admin only) ─────────────────────────────
    def register_admin(self, admin_id: str, name: str, email: str, password: str) -> bool:
        admins = load_json(self.ADMIN_FILE)
        if any(a["admin_id"] == admin_id for a in admins):
            print_error("Admin ID already exists.")
            return False
        new_admin = Admin(admin_id, name, email, password)
        admins.append(new_admin.to_dict())
        save_json(self.ADMIN_FILE, admins)
        return True
