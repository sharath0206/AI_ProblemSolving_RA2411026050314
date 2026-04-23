import streamlit as st
import math

# ─────────────────────────────────────────────
#  Page configuration
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Tic-Tac-Toe AI",
    page_icon="🎮",
    layout="centered",
)

# ─────────────────────────────────────────────
#  Custom CSS – clean, modern look
# ─────────────────────────────────────────────
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Space Mono', monospace;
        background-color: #0f0f0f;
        color: #f0f0f0;
    }

    /* Main container */
    .block-container {
        max-width: 520px !important;
        padding-top: 2rem !important;
    }

    /* Title */
    .game-title {
        font-family: 'Syne', sans-serif;
        font-size: 2.6rem;
        font-weight: 800;
        letter-spacing: -1px;
        text-align: center;
        background: linear-gradient(135deg, #e0e0e0 30%, #888 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.25rem;
    }
    .game-subtitle {
        text-align: center;
        font-size: 0.75rem;
        color: #555;
        letter-spacing: 3px;
        text-transform: uppercase;
        margin-bottom: 2rem;
    }

    /* Status banner */
    .status-banner {
        text-align: center;
        font-family: 'Syne', sans-serif;
        font-size: 1.15rem;
        font-weight: 700;
        padding: 0.65rem 1.2rem;
        border-radius: 8px;
        margin-bottom: 1.4rem;
        letter-spacing: 0.5px;
    }
    .status-playing  { background: #1a1a2e; border: 1px solid #2a2a4a; color: #9090cc; }
    .status-human-win{ background: #1a2e1a; border: 1px solid #2a4a2a; color: #70cc70; }
    .status-ai-win   { background: #2e1a1a; border: 1px solid #4a2a2a; color: #cc7070; }
    .status-draw     { background: #2a2a1a; border: 1px solid #4a4a2a; color: #cccc70; }

    /* Grid cell buttons */
    div[data-testid="column"] button {
        width: 100% !important;
        height: 110px !important;
        font-family: 'Syne', sans-serif !important;
        font-size: 2.6rem !important;
        font-weight: 800 !important;
        border-radius: 10px !important;
        border: 2px solid #2a2a2a !important;
        background-color: #1a1a1a !important;
        color: #f0f0f0 !important;
        transition: background 0.15s, border-color 0.15s, transform 0.1s !important;
        cursor: pointer !important;
    }
    div[data-testid="column"] button:hover:not(:disabled) {
        background-color: #242424 !important;
        border-color: #444 !important;
        transform: scale(1.04) !important;
    }
    div[data-testid="column"] button:disabled {
        opacity: 1 !important;
        cursor: default !important;
    }

    /* Play Again button */
    div[data-testid="stButton"] > button[kind="primary"] {
        background: linear-gradient(135deg, #303030, #1a1a1a) !important;
        color: #e0e0e0 !important;
        border: 1px solid #404040 !important;
        border-radius: 8px !important;
        font-family: 'Space Mono', monospace !important;
        font-size: 0.85rem !important;
        letter-spacing: 2px !important;
        text-transform: uppercase !important;
        padding: 0.6rem 2rem !important;
        transition: all 0.2s !important;
    }
    div[data-testid="stButton"] > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #404040, #252525) !important;
        border-color: #606060 !important;
        transform: translateY(-1px) !important;
    }

    /* Score box */
    .score-box {
        display: flex;
        justify-content: center;
        gap: 1.5rem;
        margin: 1rem 0 1.5rem 0;
    }
    .score-item {
        text-align: center;
        padding: 0.5rem 1.2rem;
        border-radius: 8px;
        border: 1px solid #222;
        background: #141414;
        min-width: 80px;
    }
    .score-label { font-size: 0.62rem; color: #555; letter-spacing: 2px; text-transform: uppercase; }
    .score-value { font-family: 'Syne', sans-serif; font-size: 1.6rem; font-weight: 800; margin-top: 0.1rem; }
    .score-human { color: #70aaff; }
    .score-ai    { color: #ff7070; }
    .score-draw  { color: #aaa; }

    /* Turn indicator dots */
    .turn-dot {
        display: inline-block;
        width: 8px; height: 8px;
        border-radius: 50%;
        margin-right: 6px;
        vertical-align: middle;
    }
    .dot-human { background: #70aaff; }
    .dot-ai    { background: #ff7070; }

    /* Divider */
    hr { border-color: #222 !important; margin: 1.5rem 0 !important; }

    /* Footer */
    .footer {
        text-align: center;
        font-size: 0.65rem;
        color: #333;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-top: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────
#  Session state initialisation
# ─────────────────────────────────────────────
def init_state():
    """Initialise all session-state keys for a fresh game."""
    st.session_state.board = [" "] * 9   # indices 0-8, row-major
    st.session_state.current_player = "X"  # human is X, AI is O
    st.session_state.game_over = False
    st.session_state.winner = None         # "X", "O", or "Draw"
    st.session_state.winning_line = []     # cell indices of the winning trio

if "board" not in st.session_state:
    # First run: also initialise score counters
    init_state()
    st.session_state.score_human = 0
    st.session_state.score_ai = 0
    st.session_state.score_draw = 0

# ─────────────────────────────────────────────
#  Core game logic
# ─────────────────────────────────────────────
WINNING_LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # cols
    (0, 4, 8), (2, 4, 6),             # diagonals
]


def check_winner(board):
    """Return 'X', 'O', 'Draw', or None."""
    for a, b, c in WINNING_LINES:
        if board[a] == board[b] == board[c] != " ":
            return board[a]
    if " " not in board:
        return "Draw"
    return None


def get_winning_line(board):
    """Return the winning triple of indices, or []."""
    for a, b, c in WINNING_LINES:
        if board[a] == board[b] == board[c] != " ":
            return [a, b, c]
    return []


def available_moves(board):
    return [i for i, v in enumerate(board) if v == " "]


# ─────────────────────────────────────────────
#  Minimax algorithm
# ─────────────────────────────────────────────
def minimax(board, depth, is_maximizing, alpha=-math.inf, beta=math.inf):
    """
    Minimax with alpha-beta pruning.
    AI  = 'O' = Maximizer  (+10 for AI win)
    Human = 'X' = Minimizer (-10 for human win)
    Depth subtracted from score so shallower wins are preferred.
    """
    result = check_winner(board)
    if result == "O":
        return 10 - depth
    if result == "X":
        return depth - 10
    if result == "Draw":
        return 0

    moves = available_moves(board)

    if is_maximizing:                     # AI's turn (O)
        best = -math.inf
        for i in moves:
            board[i] = "O"
            score = minimax(board, depth + 1, False, alpha, beta)
            board[i] = " "
            best = max(best, score)
            alpha = max(alpha, best)
            if beta <= alpha:
                break
        return best
    else:                                 # Human's turn (X)
        best = math.inf
        for i in moves:
            board[i] = "X"
            score = minimax(board, depth + 1, True, alpha, beta)
            board[i] = " "
            best = min(best, score)
            beta = min(beta, best)
            if beta <= alpha:
                break
        return best


def best_ai_move(board):
    """Return the board index of the optimal move for AI ('O')."""
    best_score = -math.inf
    best_idx = None
    for i in available_moves(board):
        board[i] = "O"
        score = minimax(board, 0, False)
        board[i] = " "
        if score > best_score:
            best_score = score
            best_idx = i
    return best_idx


# ─────────────────────────────────────────────
#  Move handler
# ─────────────────────────────────────────────
def handle_click(cell_index):
    """Called when a human clicks a cell."""
    board = st.session_state.board
    if st.session_state.game_over or board[cell_index] != " ":
        return

    # Human move
    board[cell_index] = "X"
    winner = check_winner(board)

    if winner:
        _finish_game(winner, board)
        return

    # AI move
    ai_idx = best_ai_move(board)
    if ai_idx is not None:
        board[ai_idx] = "O"
        winner = check_winner(board)
        if winner:
            _finish_game(winner, board)


def _finish_game(winner, board):
    st.session_state.game_over = True
    st.session_state.winner = winner
    st.session_state.winning_line = get_winning_line(board)
    if winner == "X":
        st.session_state.score_human += 1
    elif winner == "O":
        st.session_state.score_ai += 1
    else:
        st.session_state.score_draw += 1


# ─────────────────────────────────────────────
#  Cell label helper
# ─────────────────────────────────────────────
CELL_SYMBOLS = {"X": "✕", "O": "○", " ": ""}


def cell_label(val):
    return CELL_SYMBOLS.get(val, "")


# ─────────────────────────────────────────────
#  UI rendering
# ─────────────────────────────────────────────
st.markdown('<div class="game-title">Tic-Tac-Toe</div>', unsafe_allow_html=True)
st.markdown('<div class="game-subtitle">Minimax AI · Unbeatable</div>', unsafe_allow_html=True)

# Score board
st.markdown(
    f"""
    <div class="score-box">
        <div class="score-item">
            <div class="score-label">You (✕)</div>
            <div class="score-value score-human">{st.session_state.score_human}</div>
        </div>
        <div class="score-item">
            <div class="score-label">Draws</div>
            <div class="score-value score-draw">{st.session_state.score_draw}</div>
        </div>
        <div class="score-item">
            <div class="score-label">AI (○)</div>
            <div class="score-value score-ai">{st.session_state.score_ai}</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Status banner
winner = st.session_state.winner
game_over = st.session_state.game_over

if not game_over:
    st.markdown(
        '<div class="status-banner status-playing">'
        '<span class="turn-dot dot-human"></span>Your turn — play as ✕</div>',
        unsafe_allow_html=True,
    )
elif winner == "X":
    st.markdown(
        '<div class="status-banner status-human-win">🎉 You won! Congratulations!</div>',
        unsafe_allow_html=True,
    )
elif winner == "O":
    st.markdown(
        '<div class="status-banner status-ai-win">🤖 AI wins! Better luck next time.</div>',
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        '<div class="status-banner status-draw">🤝 It\'s a draw — perfect play!</div>',
        unsafe_allow_html=True,
    )

# 3×3 grid
board = st.session_state.board
winning_line = st.session_state.winning_line

for row in range(3):
    cols = st.columns(3, gap="small")
    for col in range(3):
        idx = row * 3 + col
        val = board[idx]
        is_winner_cell = idx in winning_line

        with cols[col]:
            # Highlight winning cells with inline style trick via markdown
            if is_winner_cell:
                st.markdown(
                    f"<style>div[data-testid='column']:nth-child({col + 1}) button "
                    f"{{ border-color: #555 !important; background-color: #2a2a1a !important; }}</style>",
                    unsafe_allow_html=True,
                )

            disabled = game_over or val != " "
            label = cell_label(val) if val != " " else " "
            st.button(
                label,
                key=f"cell_{idx}",
                disabled=disabled,
                on_click=handle_click,
                args=(idx,),
                use_container_width=True,
            )

st.markdown("<hr>", unsafe_allow_html=True)

# Play Again button
col_left, col_mid, col_right = st.columns([1, 2, 1])
with col_mid:
    if st.button("↺  Play Again", type="primary", use_container_width=True):
        init_state()
        st.rerun()

st.markdown(
    '<div class="footer">Powered by Minimax · Built with Streamlit</div>',
    unsafe_allow_html=True,
)
