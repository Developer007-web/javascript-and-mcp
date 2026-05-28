#!/usr/bin/env python3
"""
server.py — School Fee & Communication Manager MCP Server

Tools    : 13 actions (add student, mark paid, reminders, etc.)
Resources: 4 live data feeds
Prompts  : 3 pre-built workflows

Run:  python server.py
"""

import json
import sys
from datetime import date
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types

from queries import (
    get_all_students, get_student_by_id, search_students_by_name,
    get_students_by_class, add_student, update_student, deactivate_student,
    get_all_classes, mark_fee_paid, get_payment_history, get_unpaid_students,
    get_overdue_students, get_fee_summary, log_reminder, log_interaction,
    get_interactions, get_recent_interactions_all, mark_attendance,
    get_today_absentees, get_student_full_profile,
)
from messages import (
    generate_reminder, generate_bulk_reminders,
    generate_receipt, format_fee_summary,
)

app = Server("school-fee-manager")

def _cm() -> str:
    return date.today().strftime("%Y-%m")

def _today() -> str:
    return date.today().isoformat()

def _txt(text: str) -> list[types.TextContent]:
    return [types.TextContent(type="text", text=text)]


# ═══════════════════════════════════════════════════════════
#  TOOLS
# ═══════════════════════════════════════════════════════════

@app.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="add_student",
            description="Add a new student to the school database",
            inputSchema={
                "type": "object",
                "required": ["name", "class", "parent_name", "phone", "monthly_fee"],
                "properties": {
                    "name":         {"type": "string",  "description": "Full name of student"},
                    "class":        {"type": "string",  "description": "Class e.g. '6', '7', '10', 'LKG'"},
                    "section":      {"type": "string",  "description": "Section A/B/C", "default": "A"},
                    "roll_no":      {"type": "string",  "description": "Roll number"},
                    "parent_name":  {"type": "string",  "description": "Parent/guardian full name"},
                    "phone":        {"type": "string",  "description": "Parent mobile number"},
                    "alt_phone":    {"type": "string",  "description": "Alternate phone"},
                    "email":        {"type": "string",  "description": "Parent email"},
                    "monthly_fee":  {"type": "number",  "description": "Monthly fee in rupees"},
                    "discount":     {"type": "number",  "description": "Discount amount", "default": 0},
                    "address":      {"type": "string",  "description": "Home address"},
                    "notes":        {"type": "string",  "description": "Any special notes"},
                },
            },
        ),
        types.Tool(
            name="mark_fee_paid",
            description="Record a fee payment for a student",
            inputSchema={
                "type": "object",
                "required": ["student_id", "amount"],
                "properties": {
                    "student_id": {"type": "integer", "description": "Student ID"},
                    "amount":     {"type": "number",  "description": "Amount paid in ₹"},
                    "month":      {"type": "string",  "description": "YYYY-MM (default: current month)"},
                    "method":     {"type": "string",  "enum": ["cash","upi","cheque","online"], "default": "cash"},
                    "reference":  {"type": "string",  "description": "UPI txn ID or cheque number"},
                    "notes":      {"type": "string"},
                },
            },
        ),
        types.Tool(
            name="get_overdue_students",
            description="List students with fees overdue for current or last month",
            inputSchema={"type": "object", "properties": {}},
        ),
        types.Tool(
            name="get_unpaid_students",
            description="List students who haven't paid for a specific month",
            inputSchema={
                "type": "object",
                "properties": {
                    "month": {"type": "string", "description": "YYYY-MM (default: current month)"},
                    "class": {"type": "string", "description": "Filter by class"},
                },
            },
        ),
        types.Tool(
            name="generate_reminders",
            description="Generate WhatsApp/SMS fee reminder messages for unpaid students",
            inputSchema={
                "type": "object",
                "properties": {
                    "month":    {"type": "string", "description": "YYYY-MM (default: current month)"},
                    "class":    {"type": "string", "description": "Filter by class"},
                    "language": {"type": "string", "enum": ["english","hindi"], "default": "english"},
                    "tone":     {"type": "string", "enum": ["polite","urgent","friendly"], "default": "polite"},
                    "save_log": {"type": "boolean", "default": True},
                },
            },
        ),
        types.Tool(
            name="get_fee_summary",
            description="Get fee collection summary for a month",
            inputSchema={
                "type": "object",
                "properties": {
                    "month": {"type": "string", "description": "YYYY-MM (default: current month)"},
                },
            },
        ),
        types.Tool(
            name="get_student_profile",
            description="Get full profile: details, payment history, interaction log",
            inputSchema={
                "type": "object",
                "properties": {
                    "student_id": {"type": "integer", "description": "Student ID"},
                    "name":       {"type": "string",  "description": "Search by partial name"},
                },
            },
        ),
        types.Tool(
            name="search_student",
            description="Search students by name or class",
            inputSchema={
                "type": "object",
                "properties": {
                    "name":  {"type": "string", "description": "Partial name"},
                    "class": {"type": "string", "description": "Filter by class"},
                },
            },
        ),
        types.Tool(
            name="log_interaction",
            description="Log a parent call, WhatsApp message, meeting, or note",
            inputSchema={
                "type": "object",
                "required": ["student_id", "type", "note"],
                "properties": {
                    "student_id":  {"type": "integer"},
                    "type":        {"type": "string", "enum": ["call","whatsapp","meeting","note"]},
                    "note":        {"type": "string", "description": "Details of interaction"},
                    "created_by":  {"type": "string", "default": "admin"},
                },
            },
        ),
        types.Tool(
            name="mark_attendance",
            description="Mark attendance for a student",
            inputSchema={
                "type": "object",
                "required": ["student_id"],
                "properties": {
                    "student_id": {"type": "integer"},
                    "status":     {"type": "string", "enum": ["present","absent","late"], "default": "present"},
                    "date":       {"type": "string", "description": "YYYY-MM-DD (default: today)"},
                },
            },
        ),
        types.Tool(
            name="get_todays_absentees",
            description="Get list of students absent today",
            inputSchema={"type": "object", "properties": {}},
        ),
        types.Tool(
            name="apply_discount",
            description="Apply or update a fee discount for a student",
            inputSchema={
                "type": "object",
                "required": ["student_id", "discount"],
                "properties": {
                    "student_id": {"type": "integer"},
                    "discount":   {"type": "number", "description": "Discount in ₹"},
                    "reason":     {"type": "string", "description": "sibling / merit / scholarship"},
                },
            },
        ),
        types.Tool(
            name="list_classes",
            description="List all classes in the school",
            inputSchema={"type": "object", "properties": {}},
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:

    # ── add_student ──────────────────────────────────────────
    if name == "add_student":
        student = add_student(arguments)
        return _txt(
            f"✅ Student added!\n\n"
            f"ID      : {student['id']}\n"
            f"Name    : {student['name']}\n"
            f"Class   : {student['class']}-{student['section']}\n"
            f"Fee     : ₹{student['monthly_fee']}/month\n"
            f"Discount: ₹{student['discount']}\n"
            f"Parent  : {student['parent_name']} ({student['phone']})"
        )

    # ── mark_fee_paid ────────────────────────────────────────
    if name == "mark_fee_paid":
        sid    = arguments["student_id"]
        amount = arguments["amount"]
        month  = arguments.get("month") or _cm()
        method = arguments.get("method", "cash")
        ref    = arguments.get("reference")
        notes  = arguments.get("notes")

        student = get_student_by_id(sid)
        if not student:
            return _txt(f"❌ Student ID {sid} not found.")

        result = mark_fee_paid(sid, amount, month, method, ref, notes)
        if result["success"]:
            receipt = generate_receipt(
                student,
                {"amount": amount, "month": month, "method": method,
                 "reference": ref, "paid_date": _today()}
            )
            return _txt(f"{result['message']}\n\n{receipt}")
        return _txt(result["message"])

    # ── get_overdue_students ─────────────────────────────────
    if name == "get_overdue_students":
        students = get_overdue_students()
        if not students:
            return _txt("🎉 No overdue students! All fees are up to date.")
        lines = [
            f"{i+1}. {s['name']} (Class {s['class']}) — ID: {s['id']}\n"
            f"   Parent: {s['parent_name']} | 📞 {s['phone']}\n"
            f"   Overdue: {s['overdue_months']} | Total due: ₹{s['due_amount'] * s['overdue_count']:.0f}"
            for i, s in enumerate(students)
        ]
        return _txt(f"⚠️ {len(students)} students with overdue fees:\n\n" + "\n\n".join(lines))

    # ── get_unpaid_students ──────────────────────────────────
    if name == "get_unpaid_students":
        month = arguments.get("month") or _cm()
        cls   = arguments.get("class")
        students = get_unpaid_students(month, cls)
        if not students:
            return _txt(f"✅ All students have paid for {month}!")
        lines = [
            f"{i+1}. {s['name']} (Class {s['class']}) — ID: {s['id']} | ₹{s['due_amount']:.0f} | 📞 {s['phone']}"
            for i, s in enumerate(students)
        ]
        return _txt(f"📋 {len(students)} unpaid students for {month}:\n\n" + "\n".join(lines))

    # ── generate_reminders ───────────────────────────────────
    if name == "generate_reminders":
        month    = arguments.get("month") or _cm()
        cls      = arguments.get("class")
        language = arguments.get("language", "english")
        tone     = arguments.get("tone", "polite")
        save_log = arguments.get("save_log", True)

        students = get_unpaid_students(month, cls)
        if not students:
            return _txt(f"✅ No unpaid students for {month}. Nothing to remind!")

        reminders = generate_bulk_reminders(students, month, language, tone)
        if save_log:
            for r in reminders:
                log_reminder(r["student_id"], r["message"], "whatsapp", month)

        blocks = [
            f"{'━'*50}\n{i+1}. {r['student_name']} (Class {r['class']}) | 📞 {r['phone']}\n{'━'*50}\n{r['message']}"
            for i, r in enumerate(reminders)
        ]
        return _txt(f"📨 {len(reminders)} reminder(s) for {month}:\n\n" + "\n\n".join(blocks))

    # ── get_fee_summary ──────────────────────────────────────
    if name == "get_fee_summary":
        month = arguments.get("month") or _cm()
        summary = get_fee_summary(month)
        return _txt(format_fee_summary(summary))

    # ── get_student_profile ──────────────────────────────────
    if name == "get_student_profile":
        sid  = arguments.get("student_id")
        name_q = arguments.get("name")
        if sid:
            profile = get_student_full_profile(int(sid))
        elif name_q:
            found = search_students_by_name(name_q)
            if not found:
                return _txt(f"❌ No student found matching '{name_q}'")
            if len(found) > 1:
                lst = "\n".join(f"  • ID {s['id']}: {s['name']} (Class {s['class']})" for s in found)
                return _txt(f"Multiple matches:\n{lst}\n\nUse student_id to be specific.")
            profile = get_student_full_profile(found[0]["id"])
        else:
            return _txt("❌ Provide student_id or name.")

        if not profile:
            return _txt("❌ Student not found.")

        payments_str = "\n  ".join(
            f"{p['month']} — ₹{p['amount']:.0f} via {p['method']}"
            for p in profile["recent_payments"]
        ) or "None"

        interactions_str = "\n  ".join(
            f"[{i['created_at'][:10]}] {i['type']}: {i['note']}"
            for i in profile["recent_interactions"]
        ) or "None"

        sep = "─" * 42
        return _txt(
            f"👤 Student Profile\n{sep}\n"
            f"Name      : {profile['name']}\n"
            f"ID        : {profile['id']}\n"
            f"Class     : {profile['class']}-{profile['section']}\n"
            f"Roll No   : {profile.get('roll_no') or 'N/A'}\n"
            f"{sep}\n"
            f"Parent    : {profile['parent_name']}\n"
            f"Phone     : {profile['phone']}\n"
            f"Alt Phone : {profile.get('alt_phone') or 'N/A'}\n"
            f"Email     : {profile.get('email') or 'N/A'}\n"
            f"{sep}\n"
            f"Monthly Fee    : ₹{profile['monthly_fee']}\n"
            f"Discount       : ₹{profile['discount']}\n"
            f"Net Fee        : ₹{profile['net_fee']}\n"
            f"This Month Paid: {'✅ Yes' if profile['current_month_paid'] else '❌ No'}\n"
            f"{sep}\n"
            f"Recent Payments:\n  {payments_str}\n"
            f"{sep}\n"
            f"Recent Interactions:\n  {interactions_str}"
        )

    # ── search_student ───────────────────────────────────────
    if name == "search_student":
        name_q = arguments.get("name")
        cls    = arguments.get("class")
        if name_q:
            students = search_students_by_name(name_q)
        elif cls:
            students = get_students_by_class(cls)
        else:
            students = get_all_students()
        if not students:
            return _txt("❌ No students found.")
        lines = [
            f"• [ID:{s['id']}] {s['name']} — Class {s['class']}{s['section']} | {s['parent_name']} | 📞 {s['phone']}"
            for s in students
        ]
        return _txt(f"Found {len(students)} student(s):\n\n" + "\n".join(lines))

    # ── log_interaction ──────────────────────────────────────
    if name == "log_interaction":
        sid  = arguments["student_id"]
        student = get_student_by_id(sid)
        if not student:
            return _txt(f"❌ Student ID {sid} not found.")
        result = log_interaction(sid, arguments["type"], arguments["note"], arguments.get("created_by","admin"))
        return _txt(
            f"✅ {result['message']}\n\n"
            f"Student : {student['name']} (Class {student['class']})\n"
            f"Type    : {arguments['type']}\n"
            f"Note    : {arguments['note']}"
        )

    # ── mark_attendance ──────────────────────────────────────
    if name == "mark_attendance":
        result = mark_attendance(
            arguments["student_id"],
            arguments.get("date") or _today(),
            arguments.get("status", "present"),
        )
        return _txt(result["message"])

    # ── get_todays_absentees ─────────────────────────────────
    if name == "get_todays_absentees":
        absentees = get_today_absentees()
        if not absentees:
            return _txt("✅ All students are present today!")
        lines = [f"• {s['name']} (Class {s['class']}) — 📞 {s['phone']}" for s in absentees]
        return _txt(f"📋 {len(absentees)} absent today:\n\n" + "\n".join(lines))

    # ── apply_discount ───────────────────────────────────────
    if name == "apply_discount":
        sid      = arguments["student_id"]
        discount = arguments["discount"]
        reason   = arguments.get("reason", "")
        student  = get_student_by_id(sid)
        if not student:
            return _txt(f"❌ Student ID {sid} not found.")
        old_discount = student["discount"]
        update_student(sid, {"discount": discount})
        if reason:
            log_interaction(sid, "note", f"Discount updated: ₹{discount} ({reason})")
        net = student["monthly_fee"] - discount
        return _txt(
            f"✅ Discount updated for {student['name']}\n"
            f"Previous : ₹{old_discount}\n"
            f"New      : ₹{discount}\n"
            f"Net Fee  : ₹{net}/month"
            + (f"\nReason   : {reason}" if reason else "")
        )

    # ── list_classes ─────────────────────────────────────────
    if name == "list_classes":
        classes = get_all_classes()
        lines   = "\n".join(f"  • Class {c}" for c in classes)
        return _txt(f"📚 Classes in school:\n\n{lines}")

    return _txt(f"❌ Unknown tool: {name}")


# ═══════════════════════════════════════════════════════════
#  RESOURCES
# ═══════════════════════════════════════════════════════════

@app.list_resources()
async def list_resources() -> list[types.Resource]:
    return [
        types.Resource(uri="students://all",                  name="All Students",        description="Full active student roster", mimeType="application/json"),
        types.Resource(uri="fees://unpaid",                   name="Unpaid This Month",   description="Students who haven't paid current month", mimeType="application/json"),
        types.Resource(uri="interactions://recent",           name="Recent Interactions", description="Parent communications in last 7 days", mimeType="application/json"),
        types.Resource(uri="attendance://absentees/today",    name="Today's Absentees",   description="Students absent today", mimeType="application/json"),
    ]


@app.read_resource()
async def read_resource(uri: types.AnyUrl) -> str:
    uri_str = str(uri)

    if uri_str == "students://all":
        return json.dumps(get_all_students(), indent=2, default=str)

    if uri_str == "fees://unpaid":
        return json.dumps(get_unpaid_students(_cm()), indent=2, default=str)

    if uri_str == "interactions://recent":
        return json.dumps(get_recent_interactions_all(7), indent=2, default=str)

    if uri_str == "attendance://absentees/today":
        return json.dumps(get_today_absentees(), indent=2, default=str)

    raise ValueError(f"Unknown resource: {uri_str}")


# ═══════════════════════════════════════════════════════════
#  PROMPTS
# ═══════════════════════════════════════════════════════════

@app.list_prompts()
async def list_prompts() -> list[types.Prompt]:
    return [
        types.Prompt(
            name="monthly_fee_report",
            description="Generate a complete monthly fee collection report for the principal",
            arguments=[types.PromptArgument(name="month", description="YYYY-MM (default: current)", required=False)],
        ),
        types.Prompt(
            name="draft_reminder",
            description="Draft a context-aware reminder based on student's payment history",
            arguments=[
                types.PromptArgument(name="student_id", description="Student ID", required=True),
                types.PromptArgument(name="language",   description="english or hindi",  required=False),
            ],
        ),
        types.Prompt(
            name="weekly_digest",
            description="Weekly summary of fee activity and top priority actions",
            arguments=[],
        ),
    ]


@app.get_prompt()
async def get_prompt(name: str, arguments: dict | None) -> types.GetPromptResult:
    args = arguments or {}

    if name == "monthly_fee_report":
        month = args.get("month") or _cm()
        return types.GetPromptResult(
            description="Monthly fee collection report",
            messages=[types.PromptMessage(
                role="user",
                content=types.TextContent(type="text", text=(
                    f"Generate a complete fee collection report for {month}.\n"
                    f"1. Use get_fee_summary to get overall numbers.\n"
                    f"2. Use get_unpaid_students to list who hasn't paid.\n"
                    f"3. Use get_overdue_students to flag critical cases.\n"
                    f"Format it as a professional report suitable to share with the principal."
                )),
            )],
        )

    if name == "draft_reminder":
        sid  = args.get("student_id", "")
        lang = args.get("language", "english")
        return types.GetPromptResult(
            description="Context-aware fee reminder",
            messages=[types.PromptMessage(
                role="user",
                content=types.TextContent(type="text", text=(
                    f"Draft a fee reminder for student ID {sid} in {lang}.\n"
                    f"First call get_student_profile to understand their payment history.\n"
                    f"If they have ignored reminders before, use urgent tone.\n"
                    f"If this is the first reminder, use polite tone.\n"
                    f"Then call generate_reminders with the appropriate tone."
                )),
            )],
        )

    if name == "weekly_digest":
        return types.GetPromptResult(
            description="Weekly digest of fee activity",
            messages=[types.PromptMessage(
                role="user",
                content=types.TextContent(type="text", text=(
                    "Give me a weekly digest:\n"
                    "1. Call get_fee_summary for this month's collection progress.\n"
                    "2. Call get_overdue_students to flag critical cases.\n"
                    "3. Read interactions://recent resource for recent parent conversations.\n"
                    "4. Suggest the top 3 priority actions I should take today."
                )),
            )],
        )

    raise ValueError(f"Unknown prompt: {name}")


# ═══════════════════════════════════════════════════════════
#  ENTRY POINT
# ═══════════════════════════════════════════════════════════

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

if __name__ == "__main__":
    import asyncio
    print("🏫 School Fee Manager MCP Server starting...", file=sys.stderr)
    asyncio.run(main())