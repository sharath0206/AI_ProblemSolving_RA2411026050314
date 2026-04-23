# 🎮 Tic-Tac-Toe AI — Minimax Algorithm

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red?style=flat-square&logo=streamlit)
![Algorithm](https://img.shields.io/badge/Algorithm-Minimax-green?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

An interactive, browser-based Tic-Tac-Toe game where you play against an **unbeatable AI** powered by the **Minimax algorithm with Alpha-Beta Pruning**. Built with Python and Streamlit as a university assignment demonstrating adversarial search in artificial intelligence.

---

## 📋 Table of Contents

1. [Problem Description](#-problem-description)
2. [Algorithms Used](#-algorithms-used)
3. [Project Structure](#-project-structure)
4. [Execution Steps](#-execution-steps)
5. [Sample Outputs](#-sample-outputs)

---

## 🧩 Problem Description

Tic-Tac-Toe is a two-player, zero-sum game played on a 3×3 grid. Players alternate placing their mark (✕ for Human, ○ for AI) until one player achieves three-in-a-row — horizontally, vertically, or diagonally — or all nine cells are filled resulting in a draw.

Although simple in appearance, Tic-Tac-Toe is a canonical problem in **Artificial Intelligence** because:

- It has a **finite, fully observable** state space (~255,168 possible game sequences).
- It is a **perfect information** game — both players see the entire board at all times.
- It serves as an ideal testbed for **adversarial search algorithms**, where one agent's gain is the other's loss.

The core challenge is designing an AI agent that **never loses**. To do so, the agent must explore future game states and choose moves that maximise its own outcome while assuming the opponent plays optimally. This project solves that challenge using the Minimax algorithm.

---

## 🧠 Algorithms Used

### Minimax Algorithm

Minimax is a **recursive, depth-first adversarial search algorithm** used in two-player zero-sum games. It builds a **game tree** of all possible future board states and works backwards to determine the best move for the current player.

#### Roles: Maximizer vs. Minimizer

| Role | Player | Goal |
|------|--------|------|
| **Maximizer** | AI (○) | Choose moves that **maximise** the score |
| **Minimizer** | Human (✕) | Choose moves that **minimise** the score (from AI's perspective) |

#### Scoring (Terminal States)

| Outcome | Score |
|---------|-------|
| AI (○) wins | `+10 − depth` |
| Human (✕) wins | `depth − 10` |
| Draw | `0` |

Subtracting `depth` from the score means the AI **prefers faster wins and longer survivals**, making it play optimally in all scenarios.

#### Game Tree Evaluation

```
         [ Current Board ]
               |
     ┌─────────┴─────────┐
   [Move A]           [Move B]         ← AI's turn (Maximizer)
     |                   |
  [A1] [A2]          [B1] [B2]         ← Human's turn (Minimizer)
   -10   +8            +10   0
     ↑                   ↑
   max(-10, +8) = +8   max(+10, 0) = +10
                             ↑
                       AI picks Move B → score +10
```

At each level, the Maximizer picks the highest-scoring child and the Minimizer picks the lowest-scoring child. The root value propagates upward, and the AI selects the move leading to the highest guaranteed outcome.

#### Alpha-Beta Pruning (Optimisation)

To improve efficiency, this implementation adds **Alpha-Beta Pruning**:

- **Alpha** — the best score the Maximizer is guaranteed so far.
- **Beta** — the best score the Minimizer is guaranteed so far.
- If `beta ≤ alpha`, the remaining branches are **pruned** (skipped) because they cannot affect the final decision.

This reduces the number of nodes evaluated from O(b^d) to O(b^(d/2)) in the best case, where `b` is the branching factor and `d` is the depth — making the algorithm significantly faster without affecting correctness.

#### Why the AI Never Loses

Because Minimax explores **every possible future state** under the assumption that both players play optimally, it always finds the move that leads to the best guaranteed outcome. In Tic-Tac-Toe, optimal AI play results in either a **win (if the human errs)** or a **draw (if the human plays perfectly)** — never a loss.

---

## 📁 Project Structure

```
tic-tac-toe-ai/
│
├── app.py          # Main Streamlit application (UI + Minimax AI)
└── README.md       # Project documentation (this file)
```

---

## ⚙️ Execution Steps

### Prerequisites

- Python **3.9 or higher** installed ([python.org](https://www.python.org/downloads/))
- `pip` package manager

### Step 1 — Clone the Repository

```bash
git clone https://github.com/<your-username>/tic-tac-toe-ai.git
cd tic-tac-toe-ai
```

### Step 2 — (Optional) Create a Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate — macOS / Linux
source venv/bin/activate

# Activate — Windows
venv\Scripts\activate
```

### Step 3 — Install Dependencies

```bash
pip install streamlit
```

> No other third-party libraries are required. The Minimax algorithm uses only Python's built-in `math` module.

### Step 4 — Run the Application

```bash
streamlit run app.py
```

Streamlit will start a local server and automatically open the app in your default browser at:

```
http://localhost:8501
```

### Step 5 — Play!

- **You are ✕** — click any empty cell to make your move.
- **The AI is ○** — it responds instantly using Minimax.
- Click **↺ Play Again** to reset the board while keeping scores.

---

## 🖼️ Sample Outputs

Screenshots can be added below to demonstrate the application in action.

- **Initial Board State**
  > 📷 *(Screenshot placeholder — upload an image of the empty 3×3 grid when the app first loads)*

- **Mid-Game State (Human vs AI)**
  > 📷 *(Screenshot placeholder — upload an image showing several moves made by both players)*

- **AI Winning**
  > 📷 *(Screenshot placeholder — upload an image showing the "AI wins!" banner with three ○ marks in a row)*

- **Draw State**
  > 📷 *(Screenshot placeholder — upload an image showing the "It's a draw!" banner with a completely filled board)*

- **Score Tracker**
  > 📷 *(Screenshot placeholder — upload an image showing the score counters after multiple rounds)*

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

*Built as a university assignment · Python + Streamlit · Minimax with Alpha-Beta Pruning*
