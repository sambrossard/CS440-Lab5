# Vacuum Robot Environment

## Grid layout (row, col), row 0 at the top

```text
         col 0   col 1   col 2   col 3
row 0    START     0       0       0
row 1      0       X       0       0
row 2      0       0       0       0
row 3      0      -1       0      +10
```

## Cells

- Start state: (0,0)
- Wall: (1,1). The robot can never occupy this cell.
- Terminal states: (3,1) with reward -1, (3,3) with reward +10
- All other cells: reward 0
- 15 reachable states (16 cells minus the wall)

## Actions

- Up, Down, Left, Right (group assumption, following AIMA's grid world)
- Moving into the wall or off the grid leaves the robot where it is
  (group assumption).

## What the agent does NOT know

- T(s, a, s'): the probability of landing in s' after doing a in s
- R(s): the reward of each cell
- The agent only sees the state it lands in and the reward it receives,
  one step at a time. That is why this needs reinforcement learning
  (Q-learning) instead of value iteration.

## Related code

- aima-python mdp.py: GridMDP (the "known T and R" version, for comparison)
- aima-python reinforcement_learning.py: QLearningAgent, reused by vacuum/learning.py
