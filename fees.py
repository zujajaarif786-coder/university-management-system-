"""
fees.py - Fee Management Module
"""
from models import FeeRecord, Student
from utils import (load_json, save_json, get_input, get_float_input, get_int_input,
                   print_header, print_success, print_error,
                   print_info, print_divider, Colors, cprint, now_str)


FEE_FILE     = "fees.json"
STUDENT_FILE = "students.json"


def _load_fees() -> list[FeeRecord]:
    return [FeeRecord.from_dict(d) for d in load_json(FEE_FILE)]

def _save_fees(fees: list[FeeRecord]):
    save_json(FEE_FILE, [f.to_dict() for f in fees])

def _find_fee(fees, sid, sem):
    return next((f for f in fees if f.student_id == sid and f.semester == sem), None)


class FeeManager:

    def create_fee_record(self):
        print_header("CREATE FEE RECORD")
        fees     = _load_fees()
        students = [Student.from_dict(d) for d in load_json(STUDENT_FILE)]
        sid = get_input("Student ID")
        if not any(s.person_id == sid for s in students):
            print_error("Student not found.")
            return
        sem       = get_int_input("Semester (1-8)", 1, 8)
        if _find_fee(fees, sid, sem):
            print_error("Fee record already exists for this student/semester.")
            return
        total = get_float_input("Total Fee Amount", 0, 1_000_000)
        record = FeeRecord(sid, total, 0.0, sem)
        fees.append(record)
        _save_fees(fees)
        print_success(f"Fee record created. Total: {total:.2f}")

    def submit_fee(self):
        print_header("SUBMIT FEE PAYMENT")
        fees = _load_fees()
        sid  = get_input("Student ID")
        sem  = get_int_input("Semester (1-8)", 1, 8)
        record = _find_fee(fees, sid, sem)
        if not record:
            print_error("No fee record found. Please create one first.")
            return
        cprint(f"  Total: {record.total_fee:.2f} | Paid: {record.paid:.2f} | "
               f"Due: {record.due:.2f}", Colors.CYAN)
        if record.due == 0:
            print_info("All fees are paid.")
            return
        amount = get_float_input(f"Amount to pay (max {record.due:.2f})", 0.01, record.due)
        note   = get_input("Payment note (optional)", required=False)
        try:
            record.add_payment(amount, note)
            _save_fees(fees)
            print_success(f"Payment of {amount:.2f} recorded. Remaining due: {record.due:.2f}")
            self._print_receipt(record, amount, note)
        except ValueError as e:
            print_error(str(e))

    def _print_receipt(self, record: FeeRecord, amount: float, note: str):
        print_divider()
        cprint("              FEE RECEIPT", Colors.BOLD + Colors.CYAN)
        print_divider()
        cprint(f"  Student ID : {record.student_id}", Colors.CYAN)
        cprint(f"  Semester   : {record.semester}", Colors.CYAN)
        cprint(f"  Amount Paid: {amount:.2f}", Colors.GREEN)
        cprint(f"  Remaining  : {record.due:.2f}", Colors.YELLOW)
        cprint(f"  Date/Time  : {now_str()}", Colors.CYAN)
        if note:
            cprint(f"  Note       : {note}", Colors.CYAN)
        print_divider()

    def view_dues(self):
        print_header("REMAINING DUES")
        fees = _load_fees()
        if not fees:
            print_info("No fee records found.")
            return
        print_divider()
        cprint(f"  {'Student':<12} {'Sem':>4} {'Total':>10} {'Paid':>10} {'Due':>10}", Colors.BOLD)
        print_divider()
        for f in fees:
            color = Colors.GREEN if f.due == 0 else Colors.RED
            cprint(f"  {f.student_id:<12} {f.semester:>4} {f.total_fee:>10.2f} "
                   f"{f.paid:>10.2f} {f.due:>10.2f}", color)
        print_divider()

    def generate_receipt(self):
        print_header("FEE RECEIPT — STUDENT")
        fees = _load_fees()
        sid  = get_input("Student ID")
        sem  = get_int_input("Semester", 1, 8)
        record = _find_fee(fees, sid, sem)
        if not record:
            print_error("No fee record found.")
            return
        print_divider()
        cprint(f"  Student ID : {record.student_id}", Colors.CYAN)
        cprint(f"  Semester   : {record.semester}", Colors.CYAN)
        cprint(f"  Total Fee  : {record.total_fee:.2f}", Colors.CYAN)
        cprint(f"  Amount Paid: {record.paid:.2f}", Colors.GREEN)
        cprint(f"  Balance Due: {record.due:.2f}",
               Colors.GREEN if record.due == 0 else Colors.RED)
        print_divider()
        cprint("  PAYMENT HISTORY:", Colors.BOLD)
        for p in record.payments:
            cprint(f"    {p['date']}  |  {p['amount']:.2f}  |  {p.get('note','')}", Colors.CYAN)
        print_divider()

    def menu(self):
        while True:
            print_header("FEE MANAGEMENT")
            for o in ["1. Create Fee Record","2. Submit Fee Payment",
                      "3. View Remaining Dues","4. Generate Fee Receipt","0. Back"]:
                cprint(o, Colors.YELLOW)
            choice = input("\n  Select option: ").strip()
            if   choice == "1": self.create_fee_record()
            elif choice == "2": self.submit_fee()
            elif choice == "3": self.view_dues()
            elif choice == "4": self.generate_receipt()
            elif choice == "0": break
            else: print_error("Invalid option.")
