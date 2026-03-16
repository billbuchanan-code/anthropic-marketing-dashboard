# Workflow Map — Anthropic → Level Agency

## How to Read This

Each row maps one of Austin Lau's documented automations to the Level equivalent,
identifies our readiness, and names the next action.

---

## Workflow Comparison Table

| #   | Anthropic Workflow                                                     | Time Saved (Anthropic) | Level Equivalent                                         | Our Readiness            | Next Action                       |
| --- | ---------------------------------------------------------------------- | ---------------------- | -------------------------------------------------------- | ------------------------ | --------------------------------- |
| 1   | Google Ads CSV → sub-agents (headlines + descriptions) → compliant CSV | 30 min → 30 sec per ad | Multi-client Google Ads copy refresh across 150 accounts | Not started              | Build POC (see file 04)           |
| 2   | Figma plugin → 100+ ad variation generation                            | Hours → minutes        | Creative brief → variation matrix for client decks       | Not started              | Explore Figma MCP                 |
| 3   | Meta Ads MCP server → campaign analytics in Claude Desktop             | Manual pulls → instant | Meta reporting for client status calls                   | Partial (manual exports) | Connect Meta MCP server           |
| 4   | Hypothesis memory system → self-improving A/B test tracker             | No equivalent before   | Level test-and-learn documentation                       | Not started              | Design log schema first           |
| 5   | SEO + email + ASO managed solo with Claude Code                        | 1 person, 10 months    | Single strategist managing multiple channels per client  | In progress              | Identify highest-leverage channel |

---

## Priority Order for Level

### Phase 1 — High Impact, Achievable Now

1. **Google Ads copy sub-agent** — directly maps to client deliverables, API exists, POC in file 04
2. **Meta MCP server connection** — replaces manual CSV exports for status calls

### Phase 2 — Medium Effort

3. **A/B hypothesis memory system** — build a JSONL log per client, feed prior tests into context
4. **Multi-channel orchestration** — one agent per channel (paid search, paid social, email), coordinator agent above

### Phase 3 — Longer Horizon

5. **Figma plugin for creative variations** — requires Figma API access and design system alignment

---

## Key Architecture Principles from Austin's Setup

- **Sub-agents over monoliths** — split tasks by constraint (character limits, platform rules) not just by topic
- **CSV as universal interface** — input and output in CSV so non-engineers can run and read results
- **Memory as a log, not a database** — append-only hypothesis file pulled into context each run
- **Brainstorm in Claude.ai first** — fully spec the workflow in chat before writing a single line of Claude Code
