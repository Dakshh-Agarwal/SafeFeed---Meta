# OpenEnv Submission Notes — SafeFeed

This document details exactly how SafeFeed meets OpenEnv validation requirements.

---

## Total Number of Tasks

**3 tasks** are defined in `backend/env/tasks.py`:

| ID | Name | Description |
|---|---|---|
| 0 | `balanced_feed` | Moderate risk, balanced diversity |
| 1 | `high_risk_feed` | Higher risk availability, easier to spiral |
| 2 | `low_diversity_feed` | Repetitive content loops more likely |

---

## How Graders Work

Each task is graded by the same grading function (`backend/env/grader.py`) which takes the full trajectory and task config as input.

The grader computes **3 subscores**:

1. **engagement_score** — Normalised average engagement across the trajectory (0–1)
2. **safety_score** — Inversely proportional to average spiral risk (0–1)
3. **diversity_score** — Average category diversity, slightly penalised by task's diversity pressure

The **combined score** is:

```
combined = 0.4 * engagement + 0.3 * safety + 0.3 * diversity
```

---

## How Scores Are Clamped

**All final scores** are clamped using:

```python
score = max(0.01, min(0.99, score))
```

This ensures:
- No score is ever exactly `0.0`
- No score is ever exactly `1.0`
- All scores satisfy `0 < score < 1`

The clamping function is defined as `_clamp()` in `grader.py` and is applied to every subscore and the combined score.

---

## How Each Task Is Evaluated

Each task can be evaluated independently:

```python
env = SafeFeedEnv(max_steps=20)

for task in env.get_tasks():
    env.reset(task_id=task["id"])
    
    # Run agent for full episode
    done = False
    while not done:
        action = agent.select_action(state, env.content_pool)
        state, reward, done, info = env.step(action)
    
    # Grade this task
    grade = env.grade()
    print(f"Task {task['id']}: {grade['score']}")
```

---

## How to Run the Benchmark

### Programmatic (Python)

```python
from env.safefeed_env import SafeFeedEnv
from agents.safety_agent import SafetyAgent

env = SafeFeedEnv(max_steps=20)
agent = SafetyAgent()

for task in env.get_tasks():
    state = env.reset(task_id=task["id"])
    done = False
    while not done:
        action = agent.select_action(state, env.content_pool)
        state, reward, done, info = env.step(action)
    print(env.grade())
```

### Via API

```bash
# Get all tasks
curl http://localhost:8000/tasks

# Run safety agent on task 1
curl -X POST http://localhost:8000/run-agent \
  -H "Content-Type: application/json" \
  -d '{"agent_type": "safety", "task_id": 1, "steps": 20}'

# Compare both agents across all tasks
curl http://localhost:8000/compare
```

### Via Dashboard

1. Start backend: `cd backend && uvicorn app:app --reload`
2. Start frontend: `cd frontend && npm run dev`
3. Open `http://localhost:5173`
4. Click **"Compare Both"** to run the full benchmark

---

## Validator Checklist

- [x] At least 3 tasks defined
- [x] Every task has a grader
- [x] Every score is strictly between 0 and 1
- [x] Scores are never exactly 0.0 or 1.0
- [x] `get_tasks()` returns all tasks
- [x] Each task is runnable and gradable independently
- [x] Clamp function uses `max(0.01, min(0.99, score))`
