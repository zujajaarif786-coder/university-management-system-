"""
utils.py - Utility functions for University Management System
"""
import json
import os
import hashlib
from datetime import datetime

# ─────────────────────────────────────────────
# Color codes for terminal UI (Bonus feature)
# ─────────────────────────────────────────────
class Colors:
    HEADER    = '\033[95m'
    BLUE      = '\033[94m'
    CYAN      = '\033[96m'
    GREEN     = '\033[92m'
    YELLOW    = '\033[93m'
    RED       = '\033[91m'
    BOLD      = '\033[1m'
    UNDERLINE = '\033[4m'
    RESET     = '\033[0m'

def cprint(text, color=Colors.RESET):
    print(f"{color}{text}{Colors.RESET}")

def print_header(title):
    width = 60
    cprint("=" * width, Colors.CYAN)
    cprint(f"{title.center(width)}", Colors.BOLD + Colors.CYAN)
    cprint("=" * width, Colors.CYAN)

def print_success(msg):
    cprint(f"  ✓  {msg}", Colors.GREEN)

def print_error(msg):
    cprint(f"  ✗  {msg}", Colors.RED)

def print_info(msg):
    cprint(f"  ℹ  {msg}", Colors.YELLOW)

def print_divider():
    cprint("-" * 60, Colors.BLUE)

# ─────────────────────────────────────────────
# JSON file handling
# ─────────────────────────────────────────────
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

def _file_path(filename):
    return os.path.join(DATA_DIR, filename)

def load_json(filename: str) -> list | dict:
    path = _file_path(filename)
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

def save_json(filename: str, data: list | dict) -> None:
    os.makedirs(DATA_DIR, exist_ok=True)
    path = _file_path(filename)
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

# ─────────────────────────────────────────────
# Password hashing
# ─────────────────────────────────────────────
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# ─────────────────────────────────────────────
# Input helpers
# ─────────────────────────────────────────────
def get_input(prompt: str, required=True) -> str:
    while True:
        value = input(f"  {prompt}: ").strip()
        if value or not required:
            return value
        print_error("This field is required.")

def get_int_input(prompt: str, min_val=None, max_val=None) -> int:
    while True:
        try:
            value = int(input(f"  {prompt}: ").strip())
            if min_val is not None and value < min_val:
                print_error(f"Value must be >= {min_val}")
                continue
            if max_val is not None and value > max_val:
                print_error(f"Value must be <= {max_val}")
                continue
            return value
        except ValueError:
            print_error("Please enter a valid integer.")

def get_float_input(prompt: str, min_val=0.0, max_val=100.0) -> float:
    while True:
        try:
            value = float(input(f"  {prompt}: ").strip())
            if value < min_val or value > max_val:
                print_error(f"Value must be between {min_val} and {max_val}")
                continue
            return value
        except ValueError:
            print_error("Please enter a valid number.")

def confirm(prompt="Are you sure?") -> bool:
    choice = input(f"  {prompt} (y/n): ").strip().lower()
    return choice == 'y'

# ─────────────────────────────────────────────
# Grade helpers
# ─────────────────────────────────────────────
def calculate_grade(marks: float) -> tuple[str, float]:
    """Returns (letter_grade, grade_points)."""
    if marks >= 90:
        return "A+", 4.0
    elif marks >= 85:
        return "A",  4.0
    elif marks >= 80:
        return "A-", 3.7
    elif marks >= 75:
        return "B+", 3.3
    elif marks >= 70:
        return "B",  3.0
    elif marks >= 65:
        return "B-", 2.7
    elif marks >= 60:
        return "C+", 2.3
    elif marks >= 55:
        return "C",  2.0
    elif marks >= 50:
        return "C-", 1.7
    elif marks >= 45:
        return "D",  1.0
    else:
        return "F",  0.0

def now_str() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def today_str() -> str:
    return datetime.now().strftime("%Y-%m-%d")
