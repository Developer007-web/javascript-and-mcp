/**
 * Bridge server
 * - Spawns the Python MCP process
 * - Calls tools directly via JSON-RPC over stdio
 * - Exposes simple REST endpoints for the frontend
 */

const express = require("express");
const cors = require("cors");
const { spawn } = require("child_process");
const readline = require("readline");
const path = require("path");

const app = express();
app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, "public")));

// ── MCP process ───────────────────────────────────────────────────────────────

const mcpProcess = spawn("python", ["employee_leave_system.py"], {
  cwd: __dirname,
  stdio: ["pipe", "pipe", "inherit"],
});

let msgId = 1;
const pending = new Map(); // id → { resolve, reject }

const rl = readline.createInterface({ input: mcpProcess.stdout });
rl.on("line", (line) => {
  try {
    const msg = JSON.parse(line);
    const cb = pending.get(msg.id);
    if (cb) {
      pending.delete(msg.id);
      if (msg.error) cb.reject(new Error(msg.error.message));
      else cb.resolve(msg.result);
    }
  } catch (_) {}
});

function mcpCall(method, params) {
  return new Promise((resolve, reject) => {
    const id = msgId++;
    pending.set(id, { resolve, reject });
    const msg = JSON.stringify({ jsonrpc: "2.0", id, method, params });
    mcpProcess.stdin.write(msg + "\n");
    setTimeout(() => {
      if (pending.has(id)) {
        pending.delete(id);
        reject(new Error("MCP timeout"));
      }
    }, 5000);
  });
}

// Initialize MCP
mcpCall("initialize", {
  protocolVersion: "2024-11-05",
  capabilities: {},
  clientInfo: { name: "bridge", version: "1.0" },
}).catch(() => {});

// ── Helper: call a tool ───────────────────────────────────────────────────────

async function callTool(name, args) {
  const result = await mcpCall("tools/call", { name, arguments: args });
  // FastMCP returns content[0].text which is JSON string
  const raw = result?.content?.[0]?.text ?? "{}";
  return typeof raw === "string" ? JSON.parse(raw) : raw;
}

// ── REST endpoints ────────────────────────────────────────────────────────────

// GET /api/employees  – list all employees with their balances
app.get("/api/employees", async (_req, res) => {
  const names = ["Aman", "Rahul", "Priya"];
  try {
    const data = await Promise.all(
      names.map((n) => callTool("check_leave", { employee_name: n }))
    );
    res.json(data);
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

// GET /api/check/:name  – check one employee
app.get("/api/check/:name", async (req, res) => {
  try {
    const data = await callTool("check_leave", {
      employee_name: req.params.name,
    });
    res.json(data);
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

// POST /api/apply  – apply for leave  { employee_name, days }
app.post("/api/apply", async (req, res) => {
  const { employee_name, days } = req.body;
  if (!employee_name || !days)
    return res.status(400).json({ error: "Missing fields" });
  try {
    const data = await callTool("apply_leave", {
      employee_name,
      days: Number(days),
    });
    res.json(data);
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

// ── Start ─────────────────────────────────────────────────────────────────────

const PORT = process.env.PORT || 3000;
app.listen(PORT, () =>
  console.log(`Leave Management server → http://localhost:${PORT}`)
);
