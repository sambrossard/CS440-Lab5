"""The 4x4 vacuum grid as an aima GridMDP; cells are (row, col), GridMDP states (x, y)."""

from aima.mdp import GridMDP

ROWS = 4
COLS = 4
START = (0, 0)
WALL = (1, 1)
TERMINAL_REWARDS = {(3, 1): -1.0, (3, 3): 10.0}

ARROWS = {(1, 0): ">", (0, 1): "^", (-1, 0): "<", (0, -1): "v"}


def to_xy(cell: tuple[int, int]) -> tuple[int, int]:
    """Convert a (row, col) cell to GridMDP's (x, y) state."""
    row, col = cell
    return (col, ROWS - 1 - row)


def to_cell(state: tuple[int, int]) -> tuple[int, int]:
    """Convert a GridMDP (x, y) state to a (row, col) cell."""
    x, y = state
    return (ROWS - 1 - y, x)


def make_vacuum_mdp(living_reward: float = -0.04, gamma: float = 0.9) -> GridMDP:
    """Build the grid; living_reward must be nonzero since GridMDP treats 0 as a wall."""
    if living_reward == 0:
        raise ValueError("living_reward must be nonzero: GridMDP drops 0-reward cells")
    grid = []
    for row in range(ROWS):
        grid_row = []
        for col in range(COLS):
            if (row, col) == WALL:
                grid_row.append(None)
            else:
                grid_row.append(TERMINAL_REWARDS.get((row, col), living_reward))
        grid.append(grid_row)
    terminals = [to_xy(cell) for cell in TERMINAL_REWARDS]
    return GridMDP(grid, terminals=terminals, init=to_xy(START), gamma=gamma)


def policy_grid(mdp: GridMDP, policy: dict) -> str:
    """Draw a policy as text: arrows, X for the wall, rewards on terminals."""
    lines = []
    for row in range(ROWS):
        cells = []
        for col in range(COLS):
            state = to_xy((row, col))
            if (row, col) == WALL:
                cells.append("X")
            elif state in mdp.terminals:
                cells.append(f"{mdp.R(state):+g}")
            else:
                cells.append(ARROWS[policy[state]])
        lines.append(" ".join(f"{c:>3}" for c in cells))
    return "\n".join(lines)
