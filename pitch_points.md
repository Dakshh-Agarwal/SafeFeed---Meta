# Pitch Points — SafeFeed

## For Judges at Meta PyTorch Hackathon × Scaler

---

### 1. Why This Matters

- Teen mental health is a critical concern for social media platforms
- Current recommendation systems optimise for engagement without safety constraints
- There is no standardised way to **benchmark** feed ranking policies for safety
- SafeFeed provides that benchmark

---

### 2. Why It Is OpenEnv Aligned

- Implements the OpenEnv environment interface: `get_tasks()`, `reset()`, `step()`, `grade()`
- Defines **3 distinct tasks** with independent evaluation
- Every task produces a score strictly in **(0, 1)** — never exactly 0 or 1
- Designed for agent comparison, not just demonstration

---

### 3. Why It Is Benchmark-Like

- Two agents are compared under identical conditions
- Results are **reproducible** — deterministic agents, no randomness in action selection
- Grading formula is transparent and decomposable into subscores
- The environment is parameterisable via task configs (risk bias, repeat bias, diversity pressure)

---

### 4. Why the Grader Is Meaningful

- Combined score balances **engagement (40%)**, **safety (30%)**, and **diversity (30%)**
- Safety score inversely tracks spiral risk — rewards agents that keep risk low
- Diversity score rewards agents that introduce category variety
- Engagement score rewards agents that maintain user interest
- The grader creates a **real tradeoff** — you can't score perfectly on all three

---

### 5. Technical Highlights

- **FastAPI** backend with clean REST endpoints
- **React + Recharts** dashboard for live trajectory visualisation
- **72 synthetic posts** across 16 categories (healthy, neutral, and risk clusters)
- **Rule-based explainability** — every recommendation can be explained
- **No external ML dependencies** — runs entirely locally

---

### 6. What Could Be Extended

- Additional agents (RL-trained, LLM-based ranking)
- More tasks (e.g., seasonal variation, new user cold start)
- Real content pools from public datasets
- Multi-session longitudinal evaluation
- PyTorch-based agent training loop using the environment as a gym
