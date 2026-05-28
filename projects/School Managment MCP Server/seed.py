#!/usr/bin/env python3
"""
seed.py — Populate the database with realistic demo data.
Run: python seed.py
"""

from datetime import date
from dateutil.relativedelta import relativedelta
from database import get_db

db = get_db()

print("🌱 Seeding database...")

# Clear existing data
db.executescript("""
    DELETE FROM attendance;
    DELETE FROM interactions;
    DELETE FROM reminders;
    DELETE FROM payments;
    DELETE FROM students;
""")
db.commit()

# ─── Students ─────────────────────────────────────────────────────────────────

students = [
    # Class 6
    ("Aarav Sharma",   "6", "A", "601",  "Rajesh Sharma",   "9876543210", 2500, 0,   None),
    ("Priya Verma",    "6", "A", "602",  "Sunil Verma",     "9876543211", 2500, 250, "Sibling discount"),
    ("Rohan Gupta",    "6", "B", "620",  "Amit Gupta",      "9876543212", 2500, 0,   None),
    ("Sneha Patel",    "6", "B", "621",  "Dinesh Patel",    "9876543213", 2500, 0,   None),
    # Class 7
    ("Karan Singh",    "7", "A", "701",  "Harpreet Singh",  "9876543214", 3000, 0,   None),
    ("Ananya Joshi",   "7", "A", "702",  "Prakash Joshi",   "9876543215", 3000, 300, "Merit discount"),
    ("Vikas Yadav",    "7", "B", "720",  "Ramesh Yadav",    "9876543216", 3000, 0,   None),
    ("Pooja Mehta",    "7", "B", "721",  "Vikram Mehta",    "9876543217", 3000, 0,   None),
    # Class 8
    ("Arjun Kumar",    "8", "A", "801",  "Sanjay Kumar",    "9876543218", 3500, 0,   None),
    ("Divya Nair",     "8", "A", "802",  "Krishnan Nair",   "9876543219", 3500, 350, "Scholarship"),
    ("Rahul Tiwari",   "8", "B", "820",  "Anil Tiwari",     "9876543220", 3500, 0,   None),
    ("Neha Agarwal",   "8", "B", "821",  "Suresh Agarwal",  "9876543221", 3500, 0,   None),
    # Class 10
    ("Akash Mishra",   "10","A", "1001", "Vinod Mishra",    "9876543222", 4500, 0,   None),
    ("Riya Pandey",    "10","A", "1002", "Deepak Pandey",   "9876543223", 4500, 450, "Single parent"),
    ("Mohit Saxena",   "10","B", "1020", "Rakesh Saxena",   "9876543224", 4500, 0,   None),
]

db.executemany("""
    INSERT INTO students (name, class, section, roll_no, parent_name, phone, monthly_fee, discount, notes)
    VALUES (?,?,?,?,?,?,?,?,?)
""", students)
db.commit()
print(f"✅ Inserted {len(students)} students")

# ─── Payments ─────────────────────────────────────────────────────────────────

all_students = db.execute("SELECT id, monthly_fee, discount FROM students").fetchall()
cm = date.today().strftime("%Y-%m")
lm = (date.today() - relativedelta(months=1)).strftime("%Y-%m")
tm = (date.today() - relativedelta(months=2)).strftime("%Y-%m")

payments = []
for i, s in enumerate(all_students):
    net = s[1] - s[2]
    method = ["cash", "upi", "online"][i % 3]

    # Everyone paid 2 months ago
    payments.append((s[0], net, tm, method, None))

    # All except last 3 paid last month
    if i < len(all_students) - 3:
        payments.append((s[0], net, lm, method, None))

    # First 8 paid current month
    if i < 8:
        payments.append((s[0], net, cm, "upi" if i % 2 == 0 else "cash", None))

db.executemany(
    "INSERT INTO payments (student_id, amount, month, method, notes) VALUES (?,?,?,?,?)",
    payments
)
db.commit()
print(f"✅ Inserted {len(payments)} payment records")

# ─── Interactions ─────────────────────────────────────────────────────────────

interactions = [
    (1,  "call",      "Called parent about pending fee. Will pay by 10th.",              "2026-05-02 10:30:00"),
    (3,  "whatsapp",  "Sent reminder on WhatsApp. No reply yet.",                        "2026-05-01 09:00:00"),
    (7,  "call",      "Parent requested 15-day extension due to financial issues.",       "2026-05-03 14:20:00"),
    (10, "meeting",   "Parent visited. Discussed scholarship. Fee reduced by ₹350.",     "2026-05-05 11:00:00"),
    (13, "whatsapp",  "Parent confirmed UPI payment done. Awaiting confirmation.",       "2026-05-02 16:45:00"),
    (4,  "note",      "Student often comes late — inform class teacher.",                "2026-05-04 08:00:00"),
    (9,  "call",      "No answer on first call. Will try again tomorrow.",               "2026-05-06 12:00:00"),
]

db.executemany(
    "INSERT INTO interactions (student_id, type, note, created_at) VALUES (?,?,?,?)",
    interactions
)
db.commit()
print(f"✅ Inserted {len(interactions)} interaction logs")

# ─── Attendance (last 5 school days) ──────────────────────────────────────────

attendance = []
today = date.today()
for day_offset in range(5):
    day = today - relativedelta(days=day_offset)
    day_str = day.isoformat()
    for i, s in enumerate(all_students):
        # Students 2 and 6 occasionally absent
        status = "absent" if (i == 2 and day_offset == 0) or (i == 6 and day_offset <= 1) else "present"
        attendance.append((s[0], day_str, status))

db.executemany(
    "INSERT OR IGNORE INTO attendance (student_id, date, status) VALUES (?,?,?)",
    attendance
)
db.commit()
print(f"✅ Inserted {len(attendance)} attendance records")

# ─── Summary ──────────────────────────────────────────────────────────────────

unpaid_count = len(all_students) - 8
print(f"""
🎉 Database seeded!

  Students           : {len(students)}
  Payment months     : {tm}, {lm}, {cm}
  Paid this month    : 8 / {len(students)}
  Unpaid this month  : {unpaid_count}
  Interaction logs   : {len(interactions)}

Run the server:
  python server.py
""")