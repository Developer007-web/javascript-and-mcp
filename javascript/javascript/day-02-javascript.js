
// ============================================
// Day 02 - JavaScript Loops, Functions, Strings
// Playlist: CodeWithHarry JS Hindi
// Date: May 15, 2026
// ============================================

// ---- FOR LOOP ----
console.log("--- For Loop ---");
for (let i = 1; i <= 5; i++) {
  console.log("Day " + i + " of JavaScript ✅");
}

// ---- FOR IN LOOP ---- (loops over object keys)
console.log("--- For In Loop ---");
let profile = {
  name: "Aman Pratap Singh",
  goal: "AI Developer",
  skills: "JavaScript",
  day: 2
};

for (let key in profile) {
  console.log(key + " : " + profile[key]);
}

// ---- FOR OF LOOP ---- (loops over arrays)
console.log("--- For Of Loop ---");
let topics = ["Loops", "Functions", "Strings", "Template Literals"];

for (let topic of topics) {
  console.log("Learned: " + topic);
}

// ---- WHILE LOOP ----
console.log("--- While Loop ---");
let day = 1;
while (day <= 3) {
  console.log("Commit #" + day + " pushed to GitHub ✅");
  day++;
}

// ---- DO WHILE LOOP ----
console.log("--- Do While Loop ---");
let count = 1;
do {
  console.log("LinkedIn post #" + count + " done ✅");
  count++;
} while (count <= 3);
// do-while always runs at least once even if condition is false

// ---- FUNCTIONS ----
console.log("--- Functions ---");

// Basic function
function greet(name) {
  return "Hello " + name + ", keep coding! 💪";
}
console.log(greet("Aman"));

// Function with multiple params
function addDays(current, added) {
  return current + added;
}
console.log("Total days learned:", addDays(1, 1));

// Arrow function
const myGoal = (weeks) => {
  return "In " + weeks + " weeks I will be building with Claude API!";
};
console.log(myGoal(4));

// Function to track daily progress
function dailySummary(day, videos, topics) {
  return `Day ${day} — Watched ${videos} videos — Learned: ${topics.join(", ")}`;
}
console.log(dailySummary(2, 10, ["Loops", "Functions", "Strings"]));

// ---- STRINGS ----
console.log("--- Strings ---");

let firstName = "Aman";
let lastName = "Pratap Singh";

// String methods
console.log(firstName.length);              // 4
console.log(firstName.toUpperCase());       // AMAN
console.log(lastName.toLowerCase());        // pratap singh
console.log(firstName.includes("man"));     // true
console.log(firstName + " " + lastName);   // Aman Pratap Singh

// Slice
let techStack = "JavaScript, Claude API, MCP";
console.log(techStack.slice(0, 10));        // JavaScript

// Replace
let old = "I know HTML";
let updated = old.replace("HTML", "JavaScript");
console.log(updated);                       // I know JavaScript

// ---- TEMPLATE LITERALS ----
console.log("--- Template Literals ---");

let name = "Aman";
let currentDay = 2;
let target = "Claude API";

// Old way
console.log("My name is " + name + " and I am on day " + currentDay);

// New way with template literals (much cleaner!)
console.log(`My name is ${name} and I am on day ${currentDay}`);
console.log(`In week 2, I will start building with ${target} 🚀`);

// Multi-line template literal
let summary = `
=== Day ${currentDay} Summary ===
Name     : ${name}
Target   : ${target}
Topics   : Loops, Functions, Strings, Template Literals
Commit   : ✅ Done
LinkedIn : ✅ Done
`;
console.log(summary);

// ---- TODAY'S PROGRESS ----
let todayProgress = {
  day: 2,
  date: "May 15, 2026",
  videosWatched: 10,
  topicsLearned: [
    "For loop",
    "For in loop",
    "For of loop",
    "While loop",
    "Do while loop",
    "Functions",
    "Strings",
    "Template literals"
  ],
  githubCommit: true,
  linkedinPost: false
};

console.log(`\n🔥 Day ${todayProgress.day} Complete!`);
console.log(`Topics covered: ${todayProgress.topicsLearned.length}`);
todayProgress.topicsLearned.forEach((t, i) => console.log(`  ${i + 1}. ${t}`));
