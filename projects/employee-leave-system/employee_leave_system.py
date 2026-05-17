"""
FastMCP Employee Leave Management System

Run from the repository root:
    uv run employee_leave_system.py
"""

from mcp.server.fastmcp import FastMCP

# Create MCP server
mcp = FastMCP("Employee Leave System", json_response=True)

# Total allowed leaves
TOTAL_LEAVES = 20

# Employee database
employees = {
    "Aman": 2,
    "Rahul": 5,
    "Priya": 0
}


# Tool to check leave balance
@mcp.tool()
def check_leave(employee_name: str) -> dict:
    """Check employee leave details"""

    if employee_name not in employees:
        return {"error": "Employee not found"}

    taken = employees[employee_name]
    remaining = TOTAL_LEAVES - taken

    return {
        "employee": employee_name,
        "total_leaves": TOTAL_LEAVES,
        "leaves_taken": taken,
        "remaining_leaves": remaining
    }


# Tool to apply for leave
@mcp.tool()
def apply_leave(employee_name: str, days: int) -> dict:
    """Apply leave for an employee"""

    if employee_name not in employees:
        return {"error": "Employee not found"}

    current_taken = employees[employee_name]

    if current_taken + days > TOTAL_LEAVES:
        return {
            "status": "Rejected",
            "message": "Leave limit exceeded"
        }

    employees[employee_name] += days

    return {
        "status": "Approved",
        "employee": employee_name,
        "new_leaves_taken": employees[employee_name],
        "remaining_leaves": TOTAL_LEAVES - employees[employee_name]
    }


# Resource to get employee summary
@mcp.resource("employee://{employee_name}")
def employee_summary(employee_name: str) -> str:
    """Get employee leave summary"""

    if employee_name not in employees:
        return "Employee not found"

    taken = employees[employee_name]
    remaining = TOTAL_LEAVES - taken

    return (
        f"Employee: {employee_name}\n"
        f"Total Leaves: {TOTAL_LEAVES}\n"
        f"Leaves Taken: {taken}\n"
        f"Remaining Leaves: {remaining}"
    )


# Prompt for HR leave message
@mcp.prompt()
def leave_report(employee_name: str) -> str:
    """Generate HR leave report prompt"""

    if employee_name not in employees:
        return "Employee not found"

    taken = employees[employee_name]
    remaining = TOTAL_LEAVES - taken

    return (
        f"Generate a professional HR leave report for employee "
        f"{employee_name}. The employee has taken {taken} leaves "
        f"out of {TOTAL_LEAVES} and has {remaining} leaves remaining."
    )


# Run MCP server
if __name__ == "__main__":
    mcp.run(transport="stdio")
