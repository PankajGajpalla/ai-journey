# Research Note

Created: 2026-05-17 11:13:56

# AI Agent Framework Comparison

| Framework | What it is | Key Strengths | Best Use Cases |
|-----------|------------|---------------|----------------|
| **LangChain** | Open‑source library (Python/JavaScript) that provides pre‑built agent architectures, tools, and chains for LLMs. It is backed by *LangGraph* for durable runtimes and integrates with *LangSmith* for observability. | • Rapid prototyping with templates for common patterns (ReAct, Tool calling).  <br>• 1,000+ model and tool integrations, no vendor lock‑in.  <br>• Middleware hooks for human‑in‑the‑loop, data‑privacy, and compression.  <br>• Durable runtime: persistence, rewind, checkpoints.  <br>• Strong community, frequent updates. | • Building chatbots that need memory and external knowledge.  <br>• Document‑centric Q&A or summarisation tools.  <br>• Workflow automation that stitches LLM calls with API tools.  <br>• Rapid experimentation in research labs or prototypes. |
| **CrewAI** | Enterprise‑grade multi‑agent platform. Offers a visual editor + AI copilot for no‑code creation, plus a programmable API for developers. Designed to orchestrate AI “crews” that can interact with SaaS and internal systems. | • No‑code visual workflow editor + AI copilot.  <br>• Built‑in connectors for Gmail, Slack, Salesforce, Notion, HubSpot, Teams, etc.  <br>• Role‑based access, guardrails, and monitoring for compliance.  <br>• Serverless containers and scalable deployment.  <br>• Centralised training and task guardrails. | • Automating repetitive enterprise tasks (email triage, data entry).  <br>• Customer support and sales workflows.  <br>• Internal knowledge‑management bots that pull from org tools.  <br>• Teams that want to prototype agentic workflows without coding. |
| **AutoGen** | Microsoft Research’s event‑driven multi‑agent framework. Consists of *Core* (runtime), *AgentChat* (conversational API), and *Studio* (UI). Supports extensions for external services and distributed execution. | • Event‑driven architecture supports deterministic & dynamic workflows.  <br>• Built‑in code execution (Docker, CLI).  <br>• Distributed agents via gRPC/worker runtimes.  <br>• Extensible with custom extensions for tools or protocols.  <br>• Designed for research and large‑scale production use. | • Complex, multi‑step business processes that require collaboration among specialized agents.  <br>• Research into agentic collaboration and coordination.  <br>• Distributed systems where agents run across machines or languages.  <br>• Tasks that involve running code (data processing pipelines). |

## Quick Decision Guide
| Question | LangChain | CrewAI | AutoGen |
|----------|-----------|--------|----------|
| Need a quick, low‑code prototype? | ✔ (templates, LangSmith) | ✔ (visual editor & copilot) | ✘ (code‑centric) |
| Want deep customisation and control over runtime? | ✔ (middleware, LangGraph) | ✘ | ✔ (event‑driven core) |
| Must integrate with enterprise SaaS tools? | ✘ (requires custom tools) | ✔ (pre‑built connectors) | ✘ (requires extensions) |
| Requires distributed, multi‑language agents? | ✘ | ✘ | ✔ |
| Focus on research / experiment with new agentic models? | ✔ (active community) | ✘ | ✔ |

---

**Takeaway**: LangChain is ideal for rapid LLM‑centric prototyping, CrewAI excels at enterprise‑scale, low‑code agent orchestration, and AutoGen shines in research‑grade, distributed multi‑agent systems.
