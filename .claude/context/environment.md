# Vacuum Robot Environment

## Grid layout (row, col), row 0 at the top

```text
         col 0   col 1   col 2   col 3
row 0    START     r       r       r
row 1      r       X       r       r
row 2      r       r       r       r
row 3      r      -1       r      +10
```

r = living reward (-0.04; see AGENTS.md).

## Cells

- Start state: (0,0)
- Wall: (1,1). The robot can never occupy this cell.
- Terminal states: (3,1) with reward -1, (3,3) with reward +10
- All other cells: the living reward, -0.04. It must be nonzero because
  GridMDP treats a 0-reward cell as a wall.
- 15 reachable states (16 cells minus the wall)

## Actions

- Up, Down, Left, Right (group assumption, following AIMA's grid world)
- Moving into the wall or off the grid leaves the robot where it is
  (group assumption).
- Moves are slippery (GridMDP's model): 80% as intended, 10% each to the
  left or right of the intended direction.

## What the agent does NOT know

- T(s, a, s'): the probability of landing in s' after doing a in s
- R(s): the reward of each cell
- The agent only sees the state it lands in and the reward it receives,
  one step at a time. That is why this needs reinforcement learning
  (Q-learning) instead of value iteration.

## Related code

- vacuum/environment.py: make_vacuum_mdp builds the grid as an aima GridMDP;
  to_xy/to_cell convert (row, col) to GridMDP's (x, y), where y = 0 is the bottom row
- aima/mdp.py: GridMDP, value_iteration (known T and R; used only to check results)
