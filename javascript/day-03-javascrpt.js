
// ============================================
// Day 03 - Arrays, Array Methods, Map/Filter/Reduce
// Playlist: CodeWithHarry JS Hindi
// Date: May 16, 2026
// ============================================

// ---- ARRAYS ----
console.log("--- Arrays ---");

let employees = ["Aman", "Rahul", "Priya", "Rohit", "Sneha"];
let leaveDays = [5, 3, 8, 2, 6];

console.log("Employees:", employees);
console.log("First employee:", employees[0]);
console.log("Total employees:", employees.length);

// Array methods
employees.push("Vikram");          // add at end
console.log("After push:", employees);

employees.pop();                    // remove from end
console.log("After pop:", employees);

employees.unshift("Deepak");       // add at start
console.log("After unshift:", employees);

employees.shift();                  // remove from start
console.log("After shift:", employees);

// indexOf
console.log("Aman's index:", employees.indexOf("Aman")); // 0

// includes
console.log("Has Priya?", employees.includes("Priya")); // true

// slice
let firstThree = employees.slice(0, 3);
console.log("First 3:", firstThree);

// splice
let removed = employees.splice(1, 1); // remove 1 item at index 1
console.log("Removed:", removed);
console.log("After splice:", employees);

// ---- LOOPS WITH ARRAYS ----
console.log("\n--- Loops with Arrays ---");

// forEach
console.log("All employees:");
employees.forEach((emp, index) => {
  console.log(`${index + 1}. ${emp}`);
});

// for of with array
console.log("\nLeave days:");
for (let days of leaveDays) {
  console.log(`${days} days`);
}

// ---- MAP ----
console.log("\n--- Map ---");
// map creates a NEW array by transforming each element

let leaveStatus = leaveDays.map(days => {
  if (days <= 3) return "Low";
  if (days <= 6) return "Medium";
  return "High";
});

console.log("Leave days:", leaveDays);
console.log("Leave status:", leaveStatus);

// Real example - add "Mr/Ms" to names
let formalNames = employees.map(name => "Mr/Ms " + name);
console.log("Formal names:", formalNames);

// ---- FILTER ----
console.log("\n--- Filter ---");
// filter creates a NEW array with only elements that pass the condition

let highLeave = leaveDays.filter(days => days > 5);
console.log("High leave days (>5):", highLeave);

// Filter employees who need approval (more than 3 days)
let leaveRequests = [
  { name: "Aman", days: 2, status: "pending" },
  { name: "Rahul", days: 5, status: "pending" },
  { name: "Priya", days: 1, status: "approved" },
  { name: "Rohit", days: 7, status: "pending" },
  { name: "Sneha", days: 3, status: "rejected" }
];

let pendingRequests = leaveRequests.filter(req => req.status === "pending");
console.log("Pending requests:", pendingRequests);

let longLeaves = leaveRequests.filter(req => req.days > 3);
console.log("Long leave requests (>3 days):", longLeaves);

// ---- REDUCE ----
console.log("\n--- Reduce ---");
// reduce takes all elements and reduces them to a single value

let totalLeaveDays = leaveDays.reduce((total, days) => total + days, 0);
console.log("Total leave days across all employees:", totalLeaveDays);

let totalPendingDays = pendingRequests.reduce((total, req) => total + req.days, 0);
console.log("Total pending leave days:", totalPendingDays);

// ---- TODAY'S SUMMARY ----
let day3Summary = {
  day: 3,
  date: "May 16, 2026",
  jsTopics: [
    "Arrays",
    "Array methods (push, pop, shift, unshift, slice, splice)",
    "Loops with arrays (forEach, for of)",
    "Map",
    "Filter",
    "Reduce"
  ],
  mcpProject: "Employee Leave Management System",
  githubCommit: true,
  linkedinPost: false
};

console.log(`\n🔥 Day ${day3Summary.day} Complete!`);
console.log(`JS Topics: ${day3Summary.jsTopics.length}`);
console.log(`MCP Project built: ${day3Summary.mcpProject}`);
