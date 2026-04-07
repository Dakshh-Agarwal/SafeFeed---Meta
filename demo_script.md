# Demo Script — SafeFeed

Use this script to walk through the project in a hackathon demo (3-5 minutes).

---

## Setup (before demo)

1. Start the backend: `cd backend && uvicorn app:app --reload`
2. Start the frontend: `cd frontend && npm run dev`
3. Open `http://localhost:5173` in Chrome

---

## Step 1 — Introduce the Problem (30 sec)

> "When a teen scrolls through a feed, the algorithm typically optimises for engagement.
> But what happens when high engagement leads them into negative content spirals —
> appearance comparison, validation seeking, doomscrolling?
> SafeFeed is a benchmark environment that measures this tradeoff."

---

## Step 2 — Run the Engagement Agent (45 sec)

1. In the **Controls** panel, select **Task: Balanced Feed** and **Steps: 20**
2. Click **"Run Engagement Agent"**
3. Point out:
   - The trajectory feed showing the sequence of recommended posts
   - The spiral risk climbing (red line in the chart)
   - The engagement score staying high
   - The low diversity

> "The engagement agent always picks the most engaging post.
> It doesn't care about risk, repetition, or diversity.
> Watch the spiral risk climb."

---

## Step 3 — Run the Safety Agent (45 sec)

1. Click **Reset**, then click **"Run Safety Agent"** with the same settings
2. Point out:
   - Spiral risk staying much lower
   - More diverse categories
   - Slightly lower but still reasonable engagement

> "The safety agent balances engagement with risk awareness.
> It avoids content spirals while keeping the feed interesting."

---

## Step 4 — Compare Across All Tasks (60 sec)

1. Click **"Compare Both"**
2. Walk through each of the 3 tasks:
   - **Balanced Feed**: both agents perform similarly, safety agent slightly better on safety
   - **High Risk Feed**: safety agent significantly outperforms on safety scores
   - **Low Diversity Feed**: safety agent maintains diversity under pressure

> "Across all three scenarios, the safety agent consistently achieves higher combined scores
> because the grading function rewards the balance of engagement, safety, and diversity."

---

## Step 5 — Mention OpenEnv Compliance (30 sec)

> "SafeFeed is designed as an OpenEnv benchmark.
> It has 3 tasks, each with independent graders.
> All scores are clamped to (0, 1).
> The environment exposes get_tasks(), reset(), step(), and grade() —
> the standard benchmark interface."

---

## Step 6 — Wrap Up (15 sec)

> "This is SafeFeed: a benchmark that makes feed ranking safety measurable and comparable."
