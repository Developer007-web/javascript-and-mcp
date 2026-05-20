# MCP Day 02 - Research Assistant + Tavily Search
**Date:** May 19, 2026

---

## What I built today

1. ✅ Connected Tavily Search to Claude Desktop via MCP
2. ✅ Built AI Research Assistant project in Claude Desktop
3. ✅ Generated full career research report automatically
4. ✅ Report saved to Excel + Google Drive automatically
5. ✅ Tested multiple research prompts

---

## Tavily MCP Setup

### What is Tavily?
Tavily is a search API built specifically for AI agents.
Unlike Google, it returns clean structured data perfect for Claude to analyze.
Free tier: 1000 searches/month

### Config added to claude_desktop_config.json:
```json
"tavily-search": {
  "command": "npx",
  "args": ["-y", "tavily-mcp"],
  "env": {
    "TAVILY_API_KEY": "tvly-your-key-here"
  }
}
```

### Steps followed:
1. Signed up at tavily.com
2. Got free API key
3. Added config to claude_desktop_config.json
4. Restarted Claude Desktop
5. Verified Tavily appears in 🔨 tools list ✅

---

## Research Assistant Setup

### System prompt used:
```
You are an advanced AI Research Assistant with access to
web search, Google Drive and file system via MCP tools.

When I give you a research topic:
1. SEARCH — Use Tavily web search (minimum 5 sources)
2. ORGANIZE — Structure findings with clear headings
3. ANALYZE — Key insights, patterns, contradictions
4. SAVE — Save full report as .md file

Output format:
# Research Report: [Topic]
## 🎯 Key Findings (top 5)
## 📊 Detailed Analysis
## 🔍 Latest Developments (2025-2026)
## ⚠️ Things to Verify
## 💡 Recommendations
## 📚 Sources
```

---

## Research Report Generated Today

**Topic:** Claude API and MCP Developer Jobs in India 2026

### Key findings from the report:

#### Salary Ranges
| Experience | Base | Top Companies |
|------------|------|---------------|
| Fresher (0–1 yr) | ₹8–15 LPA | ₹15–20 LPA |
| Mid-level (2–4 yr) | ₹18–30 LPA | ₹30–50 LPA |
| Senior (5+ yr) | ₹35–55 LPA | ₹50–80 LPA |

#### Best Cities for MCP/AI Jobs
| City | Salary vs Baseline | Growth | Best For |
|------|-------------------|--------|----------|
| Bangalore | Highest | Very High | Product companies |
| Hyderabad | 10–15% below Bangalore | Fastest | Cost of living |
| Delhi NCR | 15–20% below Bangalore | High | IT services entry |
| Remote | Variable ₹20–50 LPA | Growing | Global startups |

#### Fresher Positioning Roadmap (from report)
| Priority | Action | Timeline | Impact |
|----------|--------|----------|--------|
| 1 | Build MCP server | Month 1–2 | Very High |
| 2 | Build multi-agent system | Month 2–3 | Very High |
| 3 | Get IBM RAG + Agentic AI cert | Month 1–3 | High |
| 4 | Optimise LinkedIn | Month 1 | High |
| 5 | Contribute to open source | Month 2–4 | High |

#### Sources cited by Claude (11 total)
- Naukri — Infosys AI Jobs
- BeBee — Fresher Agentic AI listings
- Synopsys Careers
- Build Fast with AI — Salary Guide
- BeInCareer — AI Engineer Roadmap
- JobPulse.in
- The New Stack
- NextAgile.ai
- Wipro Careers
- YouTube — MCP Creator video
- IBM RAG and Agentic AI Coursera

---

## MCP Tools Connected (full list)

| Tool | Status | Purpose |
|------|--------|---------|
| Tavily Search | ✅ Connected | Live web search |
| Filesystem | ✅ Connected | Save files locally |
| Google Drive | ✅ Connected | Save to cloud |
| AccuWeather | ✅ Connected | Weather data |

---

## Key Insight Today

> Claude + Tavily + Google Drive = Personal AI Researcher
> One prompt → web search → structured report → saved to Excel
> No manual work. No opening websites. No copy-pasting.
> This is what MCP makes possible.

---

## Prompts that worked well today

```
Research "[topic]" for me.
Search the web for latest info.
Save the report as [topic]-research.md
```

```
What are the best cities in India for MCP developer jobs?
Compare salary, growth and cost of living.
Save comparison to my Research folder.
```

---

*MCP Day 02 complete — Research Assistant fully operational ✅*
