// ============================================
// Day 04 - Console, DOM, BOM, Window Object
// Playlist: CodeWithHarry JS Hindi
// Date: May 17, 2026
// ============================================

// ---- CONSOLE METHODS ----
console.log("--- Console Methods ---");

console.log("Normal log message");           // regular output
console.warn("This is a warning ⚠️");        // yellow warning
console.error("This is an error ❌");         // red error
console.info("This is info ℹ️");              // info message

// console.table - best for arrays of objects!
let employees = [
  { name: "Aman", role: "AI Developer", day: 4 },
  { name: "Rahul", role: "Cloud Engineer", day: 2 },
  { name: "Priya", role: "MCP Specialist", day: 1 }
];
console.table(employees); // shows data in a clean table format

// console.group - group related logs
console.group("My Learning Progress");
  console.log("Day 1 - JS Basics ✅");
  console.log("Day 2 - Loops & Functions ✅");
  console.log("Day 3 - Arrays & MCP Project ✅");
  console.log("Day 4 - DOM & BOM ✅");
console.groupEnd();

// console.time - measure execution time
console.time("loop timer");
for (let i = 0; i < 1000; i++) {}
console.timeEnd("loop timer");

// ---- ALERT, PROMPT, CONFIRM ----
console.log("\n--- Alert, Prompt, Confirm ---");

// alert - shows a message box (blocks code)
// alert("Welcome to my AI learning journey!");

// prompt - asks user for input, returns a string
// let userName = prompt("What is your name?");
// console.log("Hello " + userName);

// confirm - asks yes/no question, returns true/false
// let isReady = confirm("Are you ready to learn Claude API?");
// console.log("Ready:", isReady);

// Simulating without actually opening popups
let simulatedName = "Aman";           // what prompt would return
let simulatedConfirm = true;          // what confirm would return

console.log("Simulated prompt result:", simulatedName);
console.log("Simulated confirm result:", simulatedConfirm);

if (simulatedConfirm) {
  console.log(`Let's go ${simulatedName}! Time to learn Claude API 🚀`);
}

// ---- DOM - DOCUMENT OBJECT MODEL ----
console.log("\n--- DOM ---");

/*
DOM = Document Object Model
When browser loads HTML, it converts it into a tree of objects
JavaScript can then read, change, add or delete HTML elements

Structure:
Window
  └── Document
        └── html
              ├── head
              │     └── title
              └── body
                    ├── h1
                    ├── p
                    └── div

How to select elements:
*/

// getElementById - select by id
// let heading = document.getElementById("main-heading");

// querySelector - select by CSS selector (most common)
// let btn = document.querySelector("#submit-btn");
// let allCards = document.querySelectorAll(".card");

// getElementsByClassName
// let items = document.getElementsByClassName("item");

// Changing content
// heading.innerHTML = "New Heading";
// heading.textContent = "New Text";

// Changing styles
// heading.style.color = "blue";
// heading.style.fontSize = "32px";

// Changing attributes
// btn.setAttribute("disabled", true);
// let src = img.getAttribute("src");

// Creating new elements
// let newDiv = document.createElement("div");
// newDiv.textContent = "I was created with JS!";
// document.body.appendChild(newDiv);

console.log("DOM lets JS control every HTML element on the page ✅");

// ---- WALKING THE DOM ----
console.log("\n--- Walking the DOM ---");

/*
Walking the DOM = navigating between elements using relationships

From any element you can access:
  .parentElement     → go UP to parent
  .children          → go DOWN to all children
  .firstElementChild → first child
  .lastElementChild  → last child
  .nextElementSibling    → next sibling
  .previousElementSibling → previous sibling

Example:
  let parent = document.querySelector(".container");
  let firstChild = parent.firstElementChild;
  let nextSibling = firstChild.nextElementSibling;
*/

console.log("DOM Walking relationships:");
console.log("parentElement → go UP");
console.log("children → go DOWN");
console.log("firstElementChild → first child");
console.log("lastElementChild → last child");
console.log("nextElementSibling → go RIGHT");
console.log("previousElementSibling → go LEFT");

// ---- BOM - BROWSER OBJECT MODEL ----
console.log("\n--- BOM (Browser Object Model) ---");

/*
BOM = Browser Object Model
Lets JS interact with the browser itself (not just the page)
*/

// window object - top level object in browser
console.log("Window innerWidth:", window.innerWidth);   // browser width
console.log("Window innerHeight:", window.innerHeight); // browser height

// location object - current URL info
console.log("Current URL:", window.location.href);
console.log("Hostname:", window.location.hostname);

// navigator object - browser info
console.log("Browser language:", window.navigator.language);
console.log("Online status:", window.navigator.onLine);

// screen object
console.log("Screen width:", window.screen.width);
console.log("Screen height:", window.screen.height);

// ---- WINDOW OBJECT ----
console.log("\n--- Window Object ---");

/*
window is the GLOBAL object in browser JS
Everything runs inside window

window.alert()     = alert()
window.console.log = console.log
window.document    = document
window.location    = location

You don't need to write "window." — it's automatic
*/

// setTimeout - run code after a delay
setTimeout(() => {
  console.log("This runs after 2 seconds ⏰");
}, 2000);

// setInterval - run code repeatedly
let count = 0;
let interval = setInterval(() => {
  count++;
  console.log(`Interval running: ${count}`);
  if (count >= 3) clearInterval(interval); // stop after 3 times
}, 1000);

// ---- TODAY'S SUMMARY ----
let day4Summary = {
  day: 4,
  date: "May 17, 2026",
  topicsLearned: [
    "Console methods (log, warn, error, table, group, time)",
    "Alert, Prompt, Confirm",
    "DOM - Document Object Model",
    "Walking the DOM",
    "BOM - Browser Object Model",
    "Window Object"
  ],
  keyInsight: "DOM lets JS control HTML. BOM lets JS control the browser. Window is the boss of both.",
  githubCommit: true,
  linkedinPost: false
};

console.log(`\n🔥 Day ${day4Summary.day} Complete!`);
console.log(`Key insight: ${day4Summary.keyInsight}`);
console.log(`Topics: ${day4Summary.topicsLearned.length}`);
