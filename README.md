# IdeaForge

AI-Powered Idea Research Agent, built for NVIDIA Nemotron Dev Days Seoul 2026.

Give it an idea sketch (one line or a multi-paragraph Markdown file), and the agent will:
1. Ask follow-up questions to enrich context
2. Run Tavily web search across 5 categories (competitors, market, personas, real cases, pain points)
3. **Synthesize the full product**: overview/value prop, 3 user personas with scenarios, MVP roadmap (Must/Nice/Later), and risks & assumptions
4. Save everything as a single Markdown report

- Inference: NVIDIA NIM API — `nvidia/llama-3.3-nemotron-super-49b-v1`
- Agent: LangChain + LangGraph (`create_react_agent`)
- Web search: Tavily
- Runtime: Python 3.10+, no local model (NIM API only)

## Demo

```
$ python main.py examples/sample_sketch.md
============================================================
IdeaForge — AI-Powered Idea Research Agent
Powered by NVIDIA NIM (Nemotron) + LangGraph + Tavily
============================================================

[1/4] Generating follow-up questions...

[2/4] Please answer 3 questions to enrich the context.

Q1. ...
A: ...

[3/4] Running web research (5 categories, ~1-3 minutes)...

[4/4] Constructing product (overview / scenarios / roadmap / risks)...

Report saved: outputs/20260418_235501_냉장고-재료-기반-요리-추천-서비스.md
```

## Architecture

```
 sketch.md (or CLI input)
     │
     ▼
 interview (Nemotron) — 3 follow-up Qs
     │
     ▼
 enriched context
     │
     ▼
 research loop × 5 categories    [LangGraph ReAct + Tavily]
     ├─ competitors
     ├─ market_size
     ├─ target_persona
     ├─ real_cases
     └─ pain_points
     │
     ▼
 construct phase (Nemotron, no web search)
     ├─ generate_overview     — problem / solution / UVP
     ├─ generate_scenarios    — 3 personas with user journeys
     ├─ generate_roadmap      — Must / Nice / Later
     └─ generate_risks        — 6-10 assumptions + validation plan
     │
     ▼
 report.render  ──▶  outputs/{timestamp}_{slug}.md
```

## Quick Start

1. Clone and install dependencies
   ```bash
   git clone <this repo>
   cd IdeaForge
   python -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. Configure API keys (see "API Keys" below)
   ```bash
   cp .env.example .env
   # Open .env and fill in NVIDIA_API_KEY and TAVILY_API_KEY
   ```
3. Run
   ```bash
   # option A: pass a sketch file (recommended for real usage)
   python main.py examples/sample_sketch.md

   # option B: enter a one-line idea interactively
   python main.py
   ```

> **Mock mode**: if you want to verify the flow before obtaining API keys,
> run `IDEAFORGE_MOCK=1 python main.py`. It works without installing
> dependencies and replaces all LLM/search calls with sample data.

## API Keys

### NVIDIA NIM
1. Go to https://build.nvidia.com and sign in.
2. Open the `llama-3.3-nemotron-super-49b-v1` model page.
3. Click "Get API Key" on the right panel.
4. Put the issued key (starts with `nvapi-`) into `NVIDIA_API_KEY` in `.env`.

### Tavily
1. Sign up at https://tavily.com.
2. Copy the API key from the dashboard (free tier: 1,000 searches/month).
3. Put it into `TAVILY_API_KEY` in `.env`.

## File Structure

```
IdeaForge/
├── main.py                # CLI entrypoint (accepts sketch file path)
├── ideaforge/
│   ├── config.py          # .env loading, MODEL_ID
│   ├── llm.py             # ChatNVIDIA factory
│   ├── tools.py           # Tavily search tool
│   ├── prompts.py         # System prompts (interview / research / 4 synthesis)
│   ├── agent.py           # create_react_agent builder
│   ├── interview.py       # Follow-up generation and collection
│   ├── research.py        # 5-category research loop
│   ├── construct.py       # Product synthesis: overview / scenarios / roadmap / risks
│   └── report.py          # Markdown rendering and saving
├── examples/
│   └── sample_sketch.md   # Sample multi-paragraph sketch
├── outputs/               # Generated reports (gitignored)
├── requirements.txt
├── .env.example
└── README.md
```

## Configuration

You can tune the following variables in `.env`.

| Variable | Default | Description |
|---|---|---|
| `NVIDIA_API_KEY` | (required) | NVIDIA NIM API key |
| `TAVILY_API_KEY` | (required) | Tavily API key |
| `NEMOTRON_MODEL_ID` | `nvidia/llama-3.3-nemotron-super-49b-v1` | Nemotron model ID to use |
| `OUTPUT_DIR` | `outputs` | Report output directory |
| `IDEAFORGE_MOCK` | `0` | Set to `1` to run without API calls (demo/dev only) |

## Limitations

- Accuracy is currently higher for topics with rich English-language web coverage.
- Tavily free tier caps at 1,000 searches/month; each run uses 2-4 calls per category.
- Follow-up questions are fixed at exactly 3 (tunable via prompt).

## Future Work

- Result caching (re-running the same idea)
- Streamlit / Next.js web UI
- User-defined categories (e.g., regulation, revenue model)
- Multilingual output options

## Event

NVIDIA Nemotron Dev Days Seoul 2026 — https://nvevents.nvidia.com/nemotron-dev-days-seoul-2026
