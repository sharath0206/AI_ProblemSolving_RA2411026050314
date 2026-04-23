# 🧩 Sudoku Solver — Constraint Satisfaction Problem (CSP)

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Algorithm](https://img.shields.io/badge/Algorithm-CSP%20Backtracking-1a1a2e?style=flat-square)](#algorithms-used)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

> An interactive Sudoku puzzle solver built with **pure Python** using a **Constraint Satisfaction Problem (CSP)** framework and a **Backtracking** search algorithm, served via a clean **Streamlit** web interface.

---

## 📸 Sample Outputs

| State | Screenshot |
|-------|-----------|
| **Unsolved Grid** — user enters starting clues | *(screenshot placeholder)* |
| **Solved Grid** — CSP fills remaining cells | *(screenshot placeholder)* |
| **Invalid Puzzle** — error shown for duplicates | *(screenshot placeholder)* |
| **Algorithm Info Panel** — expanded CSP explainer | *(screenshot placeholder)* |

---

## 📌 Problem Description

Sudoku is a classic **combinatorial puzzle** played on a 9×9 grid subdivided into nine 3×3 boxes. The objective is to fill every cell with a digit from **1 to 9** such that:

- Each **row** contains every digit exactly once.
- Each **column** contains every digit exactly once.
- Each **3×3 sub-grid** contains every digit exactly once.

Through the lens of **Artificial Intelligence**, Sudoku is a textbook **Constraint Satisfaction Problem (CSP)**. The puzzle's structure maps perfectly onto the CSP formalism — a finite set of variables, each with a domain of possible values, linked by constraints that restrict which combinations of assignments are legal. Solving Sudoku therefore becomes a systematic search through the assignment space, guided by constraint propagation to prune dead ends early.

---

## ⚙️ Algorithms Used

### CSP Component Mapping

| CSP Component | Sudoku Mapping |
|---------------|----------------|
| **Variables** | Each of the 81 cells, indexed by `(row, col)` |
| **Domain** | The set of integers `{1, 2, 3, 4, 5, 6, 7, 8, 9}` |
| **Constraints** | Row uniqueness · Column uniqueness · 3×3 Box uniqueness |

### Backtracking Search

The solver implements **Recursive Backtracking**, a depth-first search algorithm augmented with constraint checking at every step:

```
function BACKTRACK(board):
    cell ← find_empty(board)          # Select next unassigned variable
    if cell is None:
        return TRUE                   # All variables assigned → solution found

    for num in {1 … 9}:              # Iterate over domain
        if is_valid(board, cell, num):
            board[cell] ← num         # Tentative assignment
            if BACKTRACK(board):
                return TRUE
            board[cell] ← 0           # Undo assignment (backtrack)

    return FALSE                      # No value worked → propagate failure
```

**Key properties:**
- **Completeness**: Will always find a solution if one exists.
- **Optimality**: Finds the unique solution (Sudoku has at most one).
- **Complexity**: O(9^m) worst-case, where *m* is the number of empty cells — heavily pruned in practice by the constraint checks.
- **Space**: O(m) recursion depth.

The constraint function `is_valid(board, row, col, num)` checks all three constraint types in O(1) relative to the fixed board size, making each recursive call lightweight.

---

## 🚀 Execution Steps

### Prerequisites

- Python **3.10 or higher**
- `pip` package manager

### 1 — Clone the Repository

```bash
git clone https://github.com/your-username/sudoku-csp-solver.git
cd sudoku-csp-solver
```

### 2 — Install Dependencies

```bash
pip install streamlit pandas
```

Or using a requirements file:

```bash
pip install -r requirements.txt
```

**`requirements.txt`**
```
streamlit>=1.35.0
pandas>=2.0.0
```

### 3 — Run the Application

```bash
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`.

---

## 🗂️ Project Structure

```
sudoku-csp-solver/
│
├── app.py              # Main Streamlit application + CSP solver
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

---

## 🧠 Core Functions Reference

| Function | Description |
|----------|-------------|
| `is_valid(board, row, col, num)` | Checks all 3 Sudoku constraints for placing `num` at `(row, col)` |
| `find_empty(board)` | Returns coordinates of the next unassigned cell, or `None` |
| `solve(board)` | Recursive CSP backtracking solver — mutates board in-place |
| `is_board_valid(board)` | Pre-solve validation: detects duplicates in the initial puzzle |

---

## 🌐 Live Demo

> **Hosted on Streamlit Community Cloud:**
> 🔗 `https://your-app-name.streamlit.app` *(replace with your deployed URL)*

---

## 📄 License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for details.

---

## 👤 Author

**Your Name**
- GitHub: [@your-username](https://github.com/your-username)
- University: Your University Name
- Course: Artificial Intelligence / CSP Assignment

---

*Built with ❤️ using Python, Streamlit, and pure algorithmic thinking.*
