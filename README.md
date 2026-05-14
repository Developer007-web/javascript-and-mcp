// ============================================
// Day 01 - JavaScript Basics
// Date: May 14, 2026
// ============================================

// ---- PRIMITIVE DATA TYPES ----
let name = "Aman Pratap Singh";   // String
let age = 21;                      // Number
let isLearning = true;             // Boolean
let nothing = null;                // Null
let notDefined;                    // Undefined

console.log("Name:", name);
console.log("Age:", age);
console.log("Is Learning:", isLearning);

// ---- NON-PRIMITIVE DATA TYPES ----
let skills = ["Cloud", "MCP", "Claude API", "JavaScript"]; // Array
let profile = {                                              // Object
  name: "Aman Pratap Singh",
  goal: "Get a job using Claude API and MCP",
  day: 1
};

console.log("Skills:", skills);
console.log("Profile:", profile);

// ---- OPERATORS ----
let a = 10;
let b = 3;

console.log("Addition:", a + b);       // 13
console.log("Subtraction:", a - b);    // 7
console.log("Multiplication:", a * b); // 30
console.log("Division:", a / b);       // 3.33
console.log("Modulus:", a % b);        // 1
console.log("Is Equal:", a == b);      // false
console.log("Greater than:", a > b);   // true

// ---- CONDITIONAL STATEMENTS ----
let myScore = 85;

if (myScore >= 90) {
  console.log("Grade: A");
} else if (myScore >= 75) {
  console.log("Grade: B");  // this will print
} else {
  console.log("Grade: C");
}

// Real example - am I ready to learn Claude API?
let jsVideosWatched = 10;

if (jsVideosWatched >= 30) {
  console.log("Ready to build with Claude API!");
} else {
  console.log("Keep going! " + (30 - jsVideosWatched) + " more videos to go.");
}

// ---- EXPRESSIONS ----
let total = (5 + 3) * 2;        // arithmetic expression
let isAdult = age >= 18;         // logical expression
let greeting = "Hello " + name; // string expression

console.log("Total:", total);
console.log("Is Adult:", isAdult);
console.log("Greeting:", greeting);

// ---- FOR LOOP ----
console.log("--- My Learning Journey ---");
for (let day = 1; day <= 5; day++) {
  console.log("Day " + day + " of JavaScript done ✅");
}

// Loop through skills array
console.log("--- Skills I'm building ---");
for (let i = 0; i < skills.length; i++) {
  console.log("Skill " + (i + 1) + ": " + skills[i]);
}

// ---- WHILE LOOP ----
console.log("--- Counting commits ---");
let commits = 1;
while (commits <= 5) {
  console.log("GitHub Commit #" + commits + " pushed ✅");
  commits++;
}

// ---- TODAY'S GOAL TRACKER ----
let todayGoals = {
  watchedVideos: 10,
  githubCommit: true,
  linkedinPost: false, // do this after commit!
  topicsLearned: [
    "Primitive data types",
    "Non-primitive data types",
    "Operators",
    "Conditional statements",
    "Expressions",
    "For loop",
    "While loop"
  ]
};

console.log("=== Day 1 Summary ===");
console.log("Videos watched:", todayGoals.watchedVideos);
console.log("GitHub commit:", todayGoals.githubCommit);
console.log("Topics learned:", todayGoals.topicsLearned.length);
todayGoals.topicsLearned.forEach((topic, index) => {
  console.log((index + 1) + ". " + topic);
});
