"""
messages.py — Generate WhatsApp/SMS messages in English & Hindi.
No external APIs needed — uses Python string formatting.
"""

from datetime import datetime


def _month_name(ym: str, lang: str = "english") -> str:
    y, m = ym.split("-")
    dt = datetime(int(y), int(m), 1)
    if lang == "hindi":
        hindi_months = [
            "जनवरी", "फ़रवरी", "मार्च", "अप्रैल", "मई", "जून",
            "जुलाई", "अगस्त", "सितंबर", "अक्टूबर", "नवंबर", "दिसंबर"
        ]
        return f"{hindi_months[dt.month - 1]} {dt.year}"
    return dt.strftime("%B %Y")


def generate_reminder(
    student: dict,
    month: str,
    language: str = "english",
    tone: str = "polite",
) -> str:
    due = student["monthly_fee"] - student.get("discount", 0)
    mn = _month_name(month, language)
    name = student["name"]
    parent = student["parent_name"]
    cls = student["class"]

    templates = {
        "english": {
            "polite": (
                f"Dear {parent},\n\n"
                f"This is a gentle reminder that the fee of ₹{due:.0f}/- "
                f"for {name} (Class {cls}) for {mn} is due.\n\n"
                f"Kindly pay at your earliest convenience.\n\n"
                f"Payment modes accepted:\n"
                f"  • Cash at reception\n"
                f"  • UPI: school@upi (mention student name)\n\n"
                f"Thank you 🙏"
            ),
            "urgent": (
                f"Dear {parent},\n\n"
                f"⚠️ Fee Overdue Notice\n\n"
                f"Student : {name} | Class {cls}\n"
                f"Pending : ₹{due:.0f}/- for {mn}\n\n"
                f"Please clear the dues immediately to avoid inconvenience.\n"
                f"Contact us if you need any assistance.\n\n"
                f"Thank you."
            ),
            "friendly": (
                f"Hi {parent}! 😊\n\n"
                f"Hope all is well! Just a quick reminder — "
                f"{name}'s fees for {mn} (₹{due:.0f}/-) are still pending.\n\n"
                f"Please pay whenever convenient. Feel free to reach out if you have questions!"
            ),
        },
        "hindi": {
            "polite": (
                f"प्रिय {parent} जी,\n\n"
                f"यह सूचना है कि {name} (कक्षा {cls}) की "
                f"{mn} माह की फीस ₹{due:.0f}/- अभी बकाया है।\n\n"
                f"कृपया जल्द से जल्द भुगतान करें।\n\n"
                f"भुगतान के तरीके:\n"
                f"  • कार्यालय में नकद\n"
                f"  • UPI: school@upi (छात्र का नाम लिखें)\n\n"
                f"धन्यवाद 🙏"
            ),
            "urgent": (
                f"प्रिय {parent} जी,\n\n"
                f"⚠️ फीस बकाया सूचना\n\n"
                f"छात्र  : {name} | कक्षा {cls}\n"
                f"बकाया : ₹{due:.0f}/- ({mn})\n\n"
                f"कृपया तुरंत भुगतान करें। "
                f"किसी भी सहायता के लिए संपर्क करें।\n\n"
                f"धन्यवाद।"
            ),
            "friendly": (
                f"नमस्ते {parent} जी! 😊\n\n"
                f"उम्मीद है सब ठीक है। बस याद दिलाना था कि "
                f"{name} की {mn} की फीस ₹{due:.0f}/- बाकी है।\n\n"
                f"जब सुविधा हो, कृपया जमा करें। कोई सवाल हो तो बताएं!"
            ),
        },
    }

    lang_tpl = templates.get(language, templates["english"])
    return lang_tpl.get(tone, lang_tpl["polite"])


def generate_bulk_reminders(
    students: list[dict],
    month: str,
    language: str = "english",
    tone: str = "polite",
) -> list[dict]:
    return [
        {
            "student_id": s["id"],
            "student_name": s["name"],
            "parent_name": s["parent_name"],
            "phone": s["phone"],
            "class": s["class"],
            "due_amount": s["monthly_fee"] - s.get("discount", 0),
            "message": generate_reminder(s, month, language, tone),
        }
        for s in students
    ]


def generate_receipt(student: dict, payment: dict, language: str = "english") -> str:
    mn = _month_name(payment["month"], language)
    ref_line = f"\nRef    : {payment['reference']}" if payment.get("reference") else ""

    if language == "hindi":
        return (
            f"✅ रसीद / Receipt\n\n"
            f"छात्र  : {student['name']}\n"
            f"कक्षा  : {student['class']}\n"
            f"महीना  : {mn}\n"
            f"राशि   : ₹{payment['amount']:.0f}/-\n"
            f"विधि   : {payment['method'].upper()}"
            f"{ref_line}\n"
            f"दिनांक : {payment.get('paid_date', 'today')}\n\n"
            f"धन्यवाद! 🙏"
        )
    return (
        f"✅ Fee Receipt\n\n"
        f"Student : {student['name']}\n"
        f"Class   : {student['class']}\n"
        f"Month   : {mn}\n"
        f"Amount  : ₹{payment['amount']:.0f}/-\n"
        f"Mode    : {payment['method'].upper()}"
        f"{ref_line}\n"
        f"Date    : {payment.get('paid_date', 'today')}\n\n"
        f"Thank you! 🙏"
    )


def format_fee_summary(summary: dict) -> str:
    sep = "─" * 42

    method_lines = "\n".join(
        f"  • {m['method'].upper()}: {m['count']} payments = ₹{m['total']:.0f}"
        for m in summary["by_method"]
    ) or "  No payments recorded yet"

    class_lines = "\n".join(
        f"  • Class {c['class']}: {c['paid_students']}/{c['total_students']} paid"
        + (f"  (₹{c['collected']:.0f})" if c["collected"] else "")
        for c in summary["by_class"]
    )

    return (
        f"📊 Fee Collection Report — {summary['month_name']}\n{sep}\n"
        f"👥 Total Students  : {summary['total_students']}\n"
        f"✅ Paid            : {summary['paid_count']}\n"
        f"❌ Unpaid          : {summary['unpaid_count']}\n"
        f"📈 Collection Rate : {summary['collection_rate']}%\n"
        f"{sep}\n"
        f"💰 Expected Total  : ₹{summary['expected_total']:,}\n"
        f"✅ Collected       : ₹{summary['collected_total']:,}\n"
        f"⏳ Pending         : ₹{summary['pending_amount']:,}\n"
        f"{sep}\n"
        f"💳 By Payment Mode:\n{method_lines}\n"
        f"{sep}\n"
        f"🏫 By Class:\n{class_lines}"
    )