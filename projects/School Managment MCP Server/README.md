
🏫 School Fee Manager MCP Server

An advanced Model Context Protocol (MCP) server for managing school fees, student records, attendance, payment tracking, parent communication, and automated reminders.

Built with:

Python
SQLite
MCP SDK
Async MCP Server Architecture

This project provides a complete backend system for schools to:

manage students
track fee payments
generate reminders
log interactions
monitor attendance
expose live MCP tools/resources/prompts
✨ Features
👨‍🎓 Student Management
Add new students
Update student profiles
Search students by name/class
Deactivate students
Track parent details
💰 Fee Management
Record fee payments
Track unpaid students
Detect overdue payments
Generate fee summaries
Support:
Cash
UPI
Online
Cheque
📨 Smart Reminder System
Generate WhatsApp/SMS reminders
English + Hindi support
Multiple tones:
polite
urgent
friendly
📊 Analytics & Reporting
Monthly collection reports
Collection rate analysis
Payment method statistics
Class-wise payment summaries
📞 Parent Interaction Tracking
Log:
Calls
WhatsApp messages
Meetings
Notes
📅 Attendance System
Mark attendance
Track absentees
Daily absentee reports
⚡ MCP Features
13 MCP Tools
4 Live Resources
3 Smart Prompts
🏗️ Project Structure
school-fee-manager/
│
├── server.py          # MCP server
├── database.py        # SQLite setup & schema
├── queries.py         # Database query layer
├── messages.py        # Reminder/receipt generation
├── seed.py            # Demo data generator
│
├── data/
│   └── school.db
│
└── README.md
⚙️ Tech Stack
Technology	Purpose
Python	Backend
SQLite	Database
MCP SDK	MCP server framework
AsyncIO	Async server runtime
🗄️ Database Schema

The project uses SQLite with the following tables:

students
payments
reminders
interactions
attendance

The schema includes:

foreign keys
indexes
WAL mode
normalized structure

Defined in:

🚀 Installation
1. Clone Repository
git clone https://github.com/your-username/school-fee-manager.git
cd school-fee-manager
2. Create Virtual Environment
python -m venv venv

Activate environment:

Windows
venv\Scripts\activate
Linux / Mac
source venv/bin/activate
3. Install Dependencies
pip install mcp python-dateutil
🌱 Seed Demo Data
python seed.py

This creates:

demo students
payments
attendance records
interactions

Seed file:

▶️ Run MCP Server
python server.py

Server implementation:

🛠 MCP Tools

The server exposes powerful MCP tools including:

Tool	Description
add_student	Add student
mark_fee_paid	Record fee payment
get_overdue_students	View overdue fees
generate_reminders	Create WhatsApp reminders
get_fee_summary	Monthly analytics
search_student	Search student records
mark_attendance	Attendance tracking
apply_discount	Add fee discounts

Defined in:

📡 MCP Resources
Resource	Purpose
students://all	Active student roster
fees://unpaid	Unpaid students
interactions://recent	Recent communications
attendance://absentees/today	Daily absentees
🧠 MCP Prompts

The server includes built-in intelligent workflows:

Prompt	Purpose
monthly_fee_report	Principal-level report
draft_reminder	Context-aware reminders
weekly_digest	Weekly fee activity summary
📨 Reminder System

Supports:

English reminders
Hindi reminders
Friendly/urgent/polite tone generation

Example:

Dear Parent,

This is a gentle reminder that the fee for May 2026 is pending.

Kindly pay at your earliest convenience.

Reminder generation logic:

📊 Fee Analytics

The project can generate:

Collection rate
Pending dues
Class-wise summaries
Payment method analysis
Monthly fee reports

Analytics logic:

🔥 Example Use Cases
School Administration
Fee management
Attendance tracking
Parent communication
AI School Assistant
AI-powered reminders
Automated fee analysis
Smart reporting
MCP Learning Project
Learn MCP tools/resources/prompts
Async server design
SQLite integration
📸 Future Improvements
Web dashboard
QR-based payments
AI voice calling
SMS API integration
PDF receipt generation
Student portal
Admin authentication
Multi-school support
🧑‍💻 Author

Aman Pratap Singh
