💰 Expense Tracker MCP Server
A local MCP (Model Context Protocol) server that connects Claude AI to a personal expense tracking system. Talk to Claude in plain English to manage all your expenses.
Built by: Aman Pratap Singh
Started: May 18, 2026
Type: Local MCP Server (Intermediate Project)

🎯 What it does
Ask Claude things like:

"Add ₹2000 for rent this month"
"How much did I spend on entertainment this week?"
"Show me all my expenses"
"Edit my grocery expense from ₹1500 to ₹1800"
"Remove the Netflix expense"
"Summarize my spending this month"

Claude handles everything through natural language. No forms. No manual entry.

📂 Expense Categories
CategoryExample🏠 RentMonthly rent, PG charges🛒 GroceryVegetables, milk, daily items🎬 EntertainmentNetflix, movies, games🚗 TransportUber, metro, petrol🍔 FoodRestaurants, Zomato, Swiggy💊 HealthMedicine, gym, doctor📚 EducationCourses, books, subscriptions💰 SavingsMonthly savings tracking🛍️ ShoppingClothes, electronics, misc

⚡ Features
Core Features

✅ Add expense — category, amount, date, description
✅ Edit expense — update any field of existing expense
✅ Remove expense — delete by ID or description
✅ List expenses — view all or filter by category/date
✅ Summarize — total spending per category + monthly overview

Smart Features

📊 Monthly spending breakdown
🔍 Filter by category, date range, amount
⚠️ Overspending alerts per category
💡 Claude gives saving suggestions based on your data


🛠️ Tech Stack

MCP Server — Local server built with Node.js
Claude Desktop — AI interface via MCP
JSON — Local data storage
JavaScript — Core logic


📁 Project Structure
expense-tracker-mcp/
├── server.js          ← MCP server (tools + handlers)
├── data/
│   └── expenses.json  ← Local expense storage
├── tools/
│   ├── addExpense.js
│   ├── editExpense.js
│   ├── removeExpense.js
│   ├── listExpenses.js
│   └── summarize.js
└── README.md

🚀 How to run
bash# Install dependencies
npm install

# Start MCP server
node server.js

# Connect to Claude Desktop via claude_desktop_config.json

📅 Development Log
DateWhat was builtMay 18, 2026Project started, structure defined, README created

💡 Why I built this
Managing expenses manually is boring. I wanted to just talk to Claude and have it track everything for me. MCP makes this possible — Claude becomes your personal finance assistant that actually remembers your data.

Part of my AI development journey — documenting everything publicly
GitHub: cloud-learning-journey repo
