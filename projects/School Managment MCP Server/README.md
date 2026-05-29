# 🏫 School Fee Manager MCP Server

An advanced **Model Context Protocol (MCP) Server** for managing school fees, student records, attendance, parent communication, payment tracking, and automated reminders.

Built using:

* Python
* SQLite
* MCP SDK
* AsyncIO

This project demonstrates a complete school administration backend that can be integrated with AI assistants through the MCP protocol.

---

## ✨ Features

### 👨‍🎓 Student Management

* Add new students
* Update student profiles
* Search students by name or class
* Deactivate students
* Manage parent contact details

### 💰 Fee Management

* Record fee payments
* Track unpaid students
* Detect overdue payments
* Generate fee summaries
* Support multiple payment methods:

  * Cash
  * UPI
  * Online Transfer
  * Cheque

### 📨 Smart Reminder System

Generate automated reminders for pending fees:

* English reminders
* Hindi reminders
* Friendly tone
* Polite tone
* Urgent tone

### 📊 Analytics & Reporting

Generate insightful reports:

* Monthly fee collection reports
* Collection rate analysis
* Payment method statistics
* Class-wise payment summaries

### 📞 Parent Interaction Tracking

Maintain communication history:

* Phone calls
* WhatsApp messages
* Parent meetings
* Administrative notes

### 📅 Attendance Management

* Mark daily attendance
* Track absentees
* Generate daily absentee reports

### ⚡ MCP Capabilities

The server exposes:

* **13 MCP Tools**
* **4 MCP Resources**
* **3 MCP Prompts**

---

# 🏗️ Project Structure

```text
school-fee-manager/
│
├── server.py          # MCP Server
├── database.py        # SQLite setup and schema
├── queries.py         # Database query layer
├── messages.py        # Reminder and receipt generation
├── seed.py            # Demo data generator
│
├── data/
│   └── school.db
│
└── README.md
```

---

# ⚙️ Tech Stack

| Technology | Purpose              |
| ---------- | -------------------- |
| Python     | Backend Development  |
| SQLite     | Database             |
| MCP SDK    | MCP Server Framework |
| AsyncIO    | Async Runtime        |

---

# 🗄️ Database Schema

The project uses SQLite with the following core tables:

* students
* payments
* reminders
* interactions
* attendance

### Features

* Foreign key relationships
* Indexed queries
* WAL mode enabled
* Normalized schema design
* Fast local storage

---

# 🚀 Installation

## 1. Clone the Repository

```bash
git clone https://github.com/your-username/school-fee-manager.git

cd school-fee-manager
```

## 2. Create Virtual Environment

```bash
python -m venv venv
```

## 3. Activate Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

## 4. Install Dependencies

```bash
pip install mcp python-dateutil
```

---

# 🌱 Seed Demo Data

Generate sample records:

```bash
python seed.py
```

This creates:

* Demo students
* Payment records
* Attendance data
* Parent interactions

---

# ▶️ Run the MCP Server

```bash
python server.py
```

The server will start and expose MCP tools, resources, and prompts.

---

# 🛠 MCP Tools

| Tool                 | Description                |
| -------------------- | -------------------------- |
| add_student          | Add a new student          |
| mark_fee_paid        | Record fee payment         |
| get_overdue_students | List overdue students      |
| generate_reminders   | Generate payment reminders |
| get_fee_summary      | Monthly analytics          |
| search_student       | Search student records     |
| mark_attendance      | Record attendance          |
| apply_discount       | Apply fee discounts        |

---

# 📡 MCP Resources

| Resource                     | Purpose               |
| ---------------------------- | --------------------- |
| students://all               | Active student roster |
| fees://unpaid                | Unpaid students       |
| interactions://recent        | Recent communications |
| attendance://absentees/today | Daily absentee report |

---

# 🧠 MCP Prompts

| Prompt             | Purpose                           |
| ------------------ | --------------------------------- |
| monthly_fee_report | Principal-level fee report        |
| draft_reminder     | Context-aware reminder generation |
| weekly_digest      | Weekly fee activity summary       |

---

# 📨 Reminder Example

### English Reminder

```text
Dear Parent,

This is a gentle reminder that the fee for May 2026 is pending.

Kindly make the payment at your earliest convenience.

Thank you.
```

### Hindi Reminder

```text
प्रिय अभिभावक,

मई 2026 की फीस अभी लंबित है।

कृपया शीघ्र भुगतान करने का कष्ट करें।

धन्यवाद।
```

---

# 📊 Fee Analytics

The system can generate:

* Collection Rate Reports
* Pending Dues Analysis
* Class-wise Fee Summary
* Payment Method Statistics
* Monthly Revenue Reports

---

# 🔥 Example Use Cases

### School Administration

* Student management
* Fee collection tracking
* Attendance monitoring
* Parent communication

### AI School Assistant

* Automated reminders
* Smart fee analysis
* AI-generated reports
* Attendance insights

### MCP Learning Project

* MCP Tools implementation
* MCP Resources
* MCP Prompts
* Async Server Architecture
* SQLite Integration

---

# 🚀 Future Improvements

* Web Dashboard
* QR-based Payments
* SMS API Integration
* PDF Receipt Generation
* AI Voice Calling
* Student Portal
* Admin Authentication
* Multi-School Support
* Cloud Deployment
* Advanced Analytics

---

# 🧑‍💻 Author

**Aman Pratap Singh**
