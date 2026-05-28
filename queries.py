"""
queries.py — All database query functions for the School Fee Manager.
"""

from datetime import date, datetime, timedelta
from database import get_db, rows_to_list, row_to_dict


# ═══════════════════════════════════════════════════════════
#  STUDENTS
# ═══════════════════════════════════════════════════════════

def get_all_students() -> list[dict]:
    db = get_db()
    rows = db.execute(
        "SELECT * FROM students WHERE is_active = 1 ORDER BY class, section, name"
    ).fetchall()
    return rows_to_list(rows)


def get_student_by_id(student_id: int) -> dict:
    db = get_db()
    row = db.execute(
        "SELECT * FROM students WHERE id = ?", (student_id,)
    ).fetchone()
    return row_to_dict(row)


def search_students_by_name(name: str) -> list[dict]:
    db = get_db()
    rows = db.execute(
        "SELECT * FROM students WHERE name LIKE ? AND is_active = 1 ORDER BY name",
        (f"%{name}%",)
    ).fetchall()
    return rows_to_list(rows)


def get_students_by_class(cls: str) -> list[dict]:
    db = get_db()
    rows = db.execute(
        "SELECT * FROM students WHERE class = ? AND is_active = 1 ORDER BY section, name",
        (cls,)
    ).fetchall()
    return rows_to_list(rows)


def get_all_classes() -> list[str]:
    db = get_db()
    rows = db.execute(
        "SELECT DISTINCT class FROM students WHERE is_active = 1 ORDER BY class"
    ).fetchall()
    return [r["class"] for r in rows]


def add_student(data: dict) -> dict:
    db = get_db()
    cursor = db.execute("""
        INSERT INTO students
            (name, class, section, roll_no, parent_name, phone, alt_phone,
             email, monthly_fee, discount, address, notes)
        VALUES
            (:name, :class, :section, :roll_no, :parent_name, :phone, :alt_phone,
             :email, :monthly_fee, :discount, :address, :notes)
    """, {
        "name":        data["name"],
        "class":       data["class"],
        "section":     data.get("section", "A"),
        "roll_no":     data.get("roll_no"),
        "parent_name": data["parent_name"],
        "phone":       data["phone"],
        "alt_phone":   data.get("alt_phone"),
        "email":       data.get("email"),
        "monthly_fee": data["monthly_fee"],
        "discount":    data.get("discount", 0),
        "address":     data.get("address"),
        "notes":       data.get("notes"),
    })
    db.commit()
    return get_student_by_id(cursor.lastrowid)


def update_student(student_id: int, data: dict) -> dict:
    db = get_db()
    fields = ", ".join(f"{k} = :{k}" for k in data)
    data["id"] = student_id
    db.execute(f"UPDATE students SET {fields} WHERE id = :id", data)
    db.commit()
    return get_student_by_id(student_id)


def deactivate_student(student_id: int) -> dict:
    db = get_db()
    db.execute("UPDATE students SET is_active = 0 WHERE id = ?", (student_id,))
    db.commit()
    return {"message": f"Student ID {student_id} deactivated."}


# ═══════════════════════════════════════════════════════════
#  PAYMENTS
# ═══════════════════════════════════════════════════════════

def mark_fee_paid(student_id: int, amount: float, month: str,
                  method: str = "cash", reference: str = None,
                  notes: str = None, recorded_by: str = "admin") -> dict:
    db = get_db()
    cursor = db.execute("""
        INSERT INTO payments (student_id, amount, month, method, reference, notes, recorded_by)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (student_id, amount, month, method, reference, notes, recorded_by))
    db.commit()
    row = db.execute("SELECT * FROM payments WHERE id = ?", (cursor.lastrowid,)).fetchone()
    return row_to_dict(row)


def get_payment_history(student_id: int, limit: int = 12) -> list[dict]:
    db = get_db()
    rows = db.execute(
        "SELECT * FROM payments WHERE student_id = ? ORDER BY month DESC LIMIT ?",
        (student_id, limit)
    ).fetchall()
    return rows_to_list(rows)


def get_unpaid_students(month: str, cls: str = None) -> list[dict]:
    db = get_db()
    if cls:
        rows = db.execute("""
            SELECT s.* FROM students s
            WHERE s.is_active = 1 AND s.class = ?
              AND s.id NOT IN (
                  SELECT student_id FROM payments WHERE month = ?
              )
            ORDER BY s.class, s.name
        """, (cls, month)).fetchall()
    else:
        rows = db.execute("""
            SELECT s.* FROM students s
            WHERE s.is_active = 1
              AND s.id NOT IN (
                  SELECT student_id FROM payments WHERE month = ?
              )
            ORDER BY s.class, s.name
        """, (month,)).fetchall()
    return rows_to_list(rows)


def get_overdue_students() -> list[dict]:
    db = get_db()
    today = date.today()
    cm = today.strftime("%Y-%m")
    lm = (today.replace(day=1) - timedelta(days=1)).strftime("%Y-%m")

    rows = db.execute("""
        SELECT s.*, 
               MAX(CASE WHEN p.month = ? THEN 1 ELSE 0 END) AS paid_current,
               MAX(CASE WHEN p.month = ? THEN 1 ELSE 0 END) AS paid_last
        FROM students s
        LEFT JOIN payments p ON s.id = p.student_id AND p.month IN (?, ?)
        WHERE s.is_active = 1
        GROUP BY s.id
        HAVING paid_current = 0 OR paid_last = 0
        ORDER BY s.class, s.name
    """, (cm, lm, cm, lm)).fetchall()
    return rows_to_list(rows)


def get_fee_summary(month: str) -> dict:
    db = get_db()

    students = db.execute(
        "SELECT id, monthly_fee, discount, class FROM students WHERE is_active = 1"
    ).fetchall()
    total_students = len(students)
    expected_total = sum(s["monthly_fee"] - s["discount"] for s in students)

    paid_rows = db.execute("""
        SELECT student_id, SUM(amount) as total
        FROM payments WHERE month = ?
        GROUP BY student_id
    """, (month,)).fetchall()
    paid_ids = {r["student_id"] for r in paid_rows}
    collected_total = sum(r["total"] for r in paid_rows)
    paid_count = len(paid_ids)
    unpaid_count = total_students - paid_count
    pending_amount = expected_total - collected_total
    collection_rate = round(paid_count / total_students * 100, 1) if total_students else 0

    by_method = db.execute("""
        SELECT method, COUNT(*) as count, SUM(amount) as total
        FROM payments WHERE month = ?
        GROUP BY method
    """, (month,)).fetchall()

    by_class_rows = db.execute("""
        SELECT s.class,
               COUNT(DISTINCT s.id) as total_students,
               COUNT(DISTINCT p.student_id) as paid_students,
               COALESCE(SUM(p.amount), 0) as collected
        FROM students s
        LEFT JOIN payments p ON s.id = p.student_id AND p.month = ?
        WHERE s.is_active = 1
        GROUP BY s.class
        ORDER BY s.class
    """, (month,)).fetchall()

    y, m = month.split("-")
    month_name = datetime(int(y), int(m), 1).strftime("%B %Y")

    return {
        "month": month,
        "month_name": month_name,
        "total_students": total_students,
        "paid_count": paid_count,
        "unpaid_count": unpaid_count,
        "collection_rate": collection_rate,
        "expected_total": round(expected_total),
        "collected_total": round(collected_total),
        "pending_amount": round(pending_amount),
        "by_method": rows_to_list(by_method),
        "by_class": rows_to_list(by_class_rows),
    }


# ═══════════════════════════════════════════════════════════
#  REMINDERS & INTERACTIONS
# ═══════════════════════════════════════════════════════════

def log_reminder(student_id: int, message: str, month: str,
                 channel: str = "whatsapp") -> dict:
    db = get_db()
    cursor = db.execute("""
        INSERT INTO reminders (student_id, message, channel, month)
        VALUES (?, ?, ?, ?)
    """, (student_id, message, channel, month))
    db.commit()
    return {"id": cursor.lastrowid, "message": "Reminder logged."}


def log_interaction(student_id: int, interaction_type: str,
                    note: str, created_by: str = "admin") -> dict:
    db = get_db()
    cursor = db.execute("""
        INSERT INTO interactions (student_id, type, note, created_by)
        VALUES (?, ?, ?, ?)
    """, (student_id, interaction_type, note, created_by))
    db.commit()
    return {"id": cursor.lastrowid, "message": "Interaction logged."}


def get_interactions(student_id: int, limit: int = 20) -> list[dict]:
    db = get_db()
    rows = db.execute("""
        SELECT * FROM interactions
        WHERE student_id = ?
        ORDER BY created_at DESC
        LIMIT ?
    """, (student_id, limit)).fetchall()
    return rows_to_list(rows)


def get_recent_interactions_all(days: int = 7) -> list[dict]:
    db = get_db()
    since = (date.today() - timedelta(days=days)).isoformat()
    rows = db.execute("""
        SELECT i.*, s.name as student_name, s.class
        FROM interactions i
        JOIN students s ON s.id = i.student_id
        WHERE i.created_at >= ?
        ORDER BY i.created_at DESC
    """, (since,)).fetchall()
    return rows_to_list(rows)


# ═══════════════════════════════════════════════════════════
#  ATTENDANCE
# ═══════════════════════════════════════════════════════════

def mark_attendance(student_id: int, att_date: str, status: str = "present") -> dict:
    db = get_db()
    db.execute("""
        INSERT INTO attendance (student_id, date, status)
        VALUES (?, ?, ?)
        ON CONFLICT(student_id, date) DO UPDATE SET status = excluded.status
    """, (student_id, att_date, status))
    db.commit()
    return {"message": f"Attendance marked: {status} for student {student_id} on {att_date}."}


def get_today_absentees() -> list[dict]:
    db = get_db()
    today = date.today().isoformat()
    rows = db.execute("""
        SELECT s.id, s.name, s.class, s.section, s.phone, s.parent_name
        FROM students s
        JOIN attendance a ON a.student_id = s.id
        WHERE a.date = ? AND a.status = 'absent' AND s.is_active = 1
        ORDER BY s.class, s.name
    """, (today,)).fetchall()
    return rows_to_list(rows)


# ═══════════════════════════════════════════════════════════
#  FULL PROFILE
# ═══════════════════════════════════════════════════════════

def get_student_full_profile(student_id: int) -> dict:
    student = get_student_by_id(student_id)
    if not student:
        return {}
    payments = get_payment_history(student_id)
    interactions = get_interactions(student_id)
    return {
        "student": student,
        "payments": payments,
        "interactions": interactions,
    }