# SafeFeed

## An OpenEnv-Compatible Benchmark for Evaluating Safety-Aware Feed Ranking Agents

**Meta PyTorch Hackathon × Scaler School of Technology**

---

## What Is SafeFeed?

SafeFeed is a benchmark simulation environment where:

- A **simulated teen user session** evolves over time
- An **agent chooses the next content item to recommend** from a pool of 72 synthetic posts
- The environment tracks **engagement, spiral risk, repetition, and diversity**
- Two agents are compared:
  1. **Engagement-only baseline** — always picks the highest-engagement post
  2. **Safety-aware agent** — balances engagement with risk, repetition, and diversity

The core question:

> **Can a ranking agent maintain engagement while preventing the user from spiralling into harmful content loops?**

---

## Why OpenEnv?

SafeFeed is designed to meet the OpenEnv benchmark specification:

| Requirement | Implementation |
|---|---|
| ≥ 3 tasks | 3 distinct scenarios: `balanced_feed`, `high_risk_feed`, `low_diversity_feed` |
| Per-task graders | `grader.py` grades each task independently |
| Scores in (0, 1) | All scores clamped to `max(0.01, min(0.99, score))` |
| `get_tasks()` | Exposed in `SafeFeedEnv.get_tasks()` and `GET /tasks` |
| Independent task runs | Each task can be `reset()` → `step()` → `grade()` independently |

---

## Architecture

```
safe-feed/
├── backend/
│   ├── app.py                   # FastAPI server
│   ├── requirements.txt
│   ├── env/
│   │   ├── safefeed_env.py      # Core environment class
│   │   ├── state.py             # Session state model
│   │   ├── reward.py            # Reward function
│   │   ├── grader.py            # Task grader (clamped 0-1)
│   │   ├── logger.py            # Trajectory logger
│   │   ├── content_pool.py      # 72 synthetic posts
│   │   └── tasks.py             # 3 benchmark tasks
│   ├── agents/
│   │   ├── engagement_agent.py  # Greedy baseline
│   │   └── safety_agent.py      # Safety-aware agent
│   └── utils/
│       ├── helpers.py           # Utility functions
│       └── explain.py           # Rule-based explainability
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── pages/Dashboard.jsx
│   │   └── components/
│   │       ├── Controls.jsx
│   │       ├── FeedCard.jsx
│   │       ├── StatePanel.jsx
│   │       ├── MetricsChart.jsx
│   │       └── ComparisonView.jsx
│   └── ...config files
│
├── README.md
├── demo_script.md
├── pitch_points.md
└── openenv_submission_notes.md
```

---

## Setup & Run

### Backend

```bash
cd safe-feed/backend
pip install -r requirements.txt
uvicorn app:app --reload
```

The API is available at `http://localhost:8000`.

### Frontend

```bash
cd safe-feed/frontend
npm install
npm run dev
```

The dashboard is available at `http://localhost:5173`.

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Health check |
| `GET` | `/tasks` | List all benchmark tasks |
| `POST` | `/reset` | Reset environment to a task |
| `POST` | `/step` | Advance by one step |
| `POST` | `/run-agent` | Run a full episode with an agent |
| `GET` | `/compare` | Compare both agents across all tasks |
| `GET` | `/grade` | Grade current trajectory |

---

## Key Design Decisions

1. **No external ML** — Both agents are rule-based for reproducibility and debuggability
2. **Deterministic** — Agents produce the same output given the same state
3. **Modular** — Each component (state, reward, grader, logger) is independently testable
4. **Validator-safe** — All scores clamped to `(0.01, 0.99)`, never exactly 0 or 1
5. **Content is synthetic** — No real harmful content; risk scores are abstract numerical signals

---

## License

MIT — Built for the Meta PyTorch Hackathon × Scaler School of Technology.
