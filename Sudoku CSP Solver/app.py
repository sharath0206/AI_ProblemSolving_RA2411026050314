import streamlit as st
import pandas as pd
import copy
import time

# ─────────────────────────────────────────────
#  CSP BACKTRACKING SOLVER (Pure Python, no libs)
# ─────────────────────────────────────────────

def is_valid(board: list[list[int]], row: int, col: int, num: int) -> bool:
    """
    Constraint checker — enforces all three Sudoku constraints:
      1. Row uniqueness
      2. Column uniqueness
      3. 3×3 sub-grid uniqueness
    """
    # Row constraint
    if num in board[row]:
        return False

    # Column constraint
    if num in [board[r][col] for r in range(9)]:
        return False

    # 3×3 sub-grid constraint
    box_row, box_col = 3 * (row // 3), 3 * (col // 3)
    for r in range(box_row, box_row + 3):
        for c in range(box_col, box_col + 3):
            if board[r][c] == num:
                return False

    return True


def find_empty(board: list[list[int]]) -> tuple[int, int] | None:
    """
    Finds the next unassigned variable (empty cell).
    Returns (row, col) or None if board is fully assigned.
    """
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                return (r, c)
    return None


def solve(board: list[list[int]]) -> bool:
    """
    CSP Backtracking Algorithm:
      - Variables  : each empty cell (r, c)
      - Domain     : digits 1–9
      - Constraints: row, column, and box uniqueness (checked via is_valid)
      - Strategy   : depth-first search with constraint propagation on assignment
    Returns True if solved in-place, False if unsolvable.
    """
    empty = find_empty(board)
    if not empty:
        return True          # All variables assigned → solution found

    row, col = empty

    for num in range(1, 10):   # Try each value in the domain
        if is_valid(board, row, col, num):
            board[row][col] = num          # Tentative assignment

            if solve(board):               # Recurse
                return True

            board[row][col] = 0            # Backtrack: undo assignment

    return False   # No value worked → trigger backtracking in caller


def is_board_valid(board: list[list[int]]) -> tuple[bool, str]:
    """
    Validates the initial puzzle for duplicate values before solving.
    """
    for r in range(9):
        row_vals = [v for v in board[r] if v != 0]
        if len(row_vals) != len(set(row_vals)):
            return False, f"Row {r + 1} contains duplicate values."

    for c in range(9):
        col_vals = [board[r][c] for r in range(9) if board[r][c] != 0]
        if len(col_vals) != len(set(col_vals)):
            return False, f"Column {c + 1} contains duplicate values."

    for br in range(3):
        for bc in range(3):
            box_vals = []
            for r in range(br * 3, br * 3 + 3):
                for c in range(bc * 3, bc * 3 + 3):
                    if board[r][c] != 0:
                        box_vals.append(board[r][c])
            if len(box_vals) != len(set(box_vals)):
                return False, f"3×3 box at ({br+1},{bc+1}) contains duplicate values."

    return True, ""


# ─────────────────────────────────────────────
#  STREAMLIT UI
# ─────────────────────────────────────────────

SAMPLE_PUZZLE = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9],
]

EMPTY_PUZZLE = [[0] * 9 for _ in range(9)]

st.set_page_config(
    page_title="Sudoku CSP Solver",
    page_icon="🧩",
    layout="centered",
)

# ── Custom CSS ──────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&display=swap');

  html, body, [class*="css"] {
      font-family: 'Space Mono', monospace;
  }
  .main-title {
      font-size: 2.4rem;
      font-weight: 700;
      letter-spacing: -1px;
      color: #fff;
      margin-bottom: 0;
  }
  .subtitle {
      color: #666;
      font-size: 0.85rem;
      margin-top: 2px;
      margin-bottom: 1.5rem;
  }
  .badge {
      display: inline-block;
      background: #1a1a2e;
      color: #e0e0ff;
      font-size: 0.7rem;
      padding: 3px 10px;
      border-radius: 4px;
      margin-right: 6px;
      letter-spacing: 1px;
      text-transform: uppercase;
  }
  .info-box {
      background: #f0f4ff;
      border-left: 4px solid #4a4aff;
      padding: 0.8rem 1rem;
      border-radius: 4px;
      font-size: 0.82rem;
      color: #333;
      margin-bottom: 1rem;
  }
  div[data-testid="stDataEditor"] table th {
      background: #1a1a2e !important;
      color: #e0e0ff !important;
  }
</style>
""", unsafe_allow_html=True)

# ── Header ──────────────────────────────────
st.markdown('<div class="main-title">🧩 Sudoku CSP Solver</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Constraint Satisfaction Problem · Backtracking Algorithm · Python + Streamlit</div>', unsafe_allow_html=True)

st.markdown("""
<span class="badge">Variables</span>
<span class="badge">Domains 1–9</span>
<span class="badge">Constraints</span>
<span class="badge">Backtracking</span>
""", unsafe_allow_html=True)

st.divider()

# ── Session State ────────────────────────────
if "grid" not in st.session_state:
    st.session_state.grid = copy.deepcopy(SAMPLE_PUZZLE)
if "solved_cells" not in st.session_state:
    st.session_state.solved_cells = set()

# ── Info Box ─────────────────────────────────
st.markdown("""
<div class="info-box">
  <b>How to use:</b> Enter digits 1–9 in the grid below (use <b>0</b> for empty cells).
  Click <b>Solve Sudoku</b> to watch the CSP algorithm fill the puzzle,
  or <b>Load Sample</b> to try a classic puzzle.
</div>
""", unsafe_allow_html=True)

# ── Grid Editor ──────────────────────────────
col_labels = [f"C{i+1}" for i in range(9)]
df = pd.DataFrame(
    st.session_state.grid,
    columns=col_labels,
    index=[f"R{i+1}" for i in range(9)],
)

column_config = {
    col: st.column_config.NumberColumn(
        label=col,
        min_value=0,
        max_value=9,
        step=1,
        default=0,
    )
    for col in col_labels
}

edited_df = st.data_editor(
    df,
    column_config=column_config,
    use_container_width=True,
    key="sudoku_editor",
    hide_index=False,
)

# ── Action Buttons ───────────────────────────
btn_col1, btn_col2, btn_col3 = st.columns([2, 1.5, 1.5])

with btn_col1:
    solve_clicked = st.button("🚀 Solve Sudoku", type="primary", use_container_width=True)
with btn_col2:
    sample_clicked = st.button("📋 Load Sample", use_container_width=True)
with btn_col3:
    clear_clicked = st.button("🗑️ Clear Grid", use_container_width=True)

# ── Button Logic ─────────────────────────────

if sample_clicked:
    st.session_state.grid = copy.deepcopy(SAMPLE_PUZZLE)
    st.session_state.solved_cells = set()
    st.rerun()

if clear_clicked:
    st.session_state.grid = copy.deepcopy(EMPTY_PUZZLE)
    st.session_state.solved_cells = set()
    st.rerun()

if solve_clicked:
    # Parse grid from editor
    raw = edited_df.fillna(0).astype(int).values.tolist()

    # Validate input range
    valid_range = all(0 <= raw[r][c] <= 9 for r in range(9) for c in range(9))
    if not valid_range:
        st.error("⚠️ All cell values must be between 0 and 9.")
    else:
        ok, msg = is_board_valid(raw)
        if not ok:
            st.error(f"❌ Invalid puzzle: {msg}")
        else:
            board_copy = copy.deepcopy(raw)
            start = time.perf_counter()
            solvable = solve(board_copy)
            elapsed = time.perf_counter() - start

            if solvable:
                # Track which cells were filled by the solver
                filled = {
                    (r, c)
                    for r in range(9)
                    for c in range(9)
                    if raw[r][c] == 0
                }
                st.session_state.grid = board_copy
                st.session_state.solved_cells = filled
                st.success(f"✅ Puzzle solved in **{elapsed*1000:.2f} ms** using CSP Backtracking!")
                st.balloons()
                st.rerun()
            else:
                st.error("❌ This puzzle has no solution. Please check your input.")

# ── CSP Explanation ──────────────────────────
st.divider()
with st.expander("📖 How the CSP Algorithm Works", expanded=False):
    st.markdown("""
**Constraint Satisfaction Problem (CSP) Framework:**

| Component | Sudoku Mapping |
|-----------|---------------|
| **Variables** | Each of the 81 cells `(row, col)` |
| **Domain** | Integers `{1, 2, 3, 4, 5, 6, 7, 8, 9}` |
| **Constraints** | Each digit appears exactly once per row, column, and 3×3 box |

**Backtracking Algorithm (DFS + Constraint Checking):**
1. **Select** the next unassigned variable (empty cell)
2. **Iterate** over domain values `1–9`
3. **Check** constraints — if `is_valid(board, row, col, num)` passes, assign tentatively
4. **Recurse** — call `solve()` on the updated board
5. **Backtrack** — if recursion fails, reset cell to `0` and try the next value
6. **Terminate** — return `True` when no empty cells remain (solution found)

The algorithm explores the search space in O(9^m) worst-case where `m` is the number of empty cells,
pruned heavily by constraint checking at every step.
    """)

# ── Footer ────────────────────────────────────
st.caption("Built with Python + Streamlit · CSP / Backtracking · University AI Assignment")
