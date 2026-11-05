# Lab 5 - Vacuum Robot with Q-Learning (CS 440)

## Project overview
A vacuum-robot agent learns to navigate a 4x4 grid with Q-learning (AIMA ch. 22).
This lab implements the environment and the learning agent, and selects values
for the living reward, discount factor, learning rate, and epsilon.

## Environment
- 4x4 grid, cells as (row, col); (0,0) top-left is the start
- Wall "X" at (1,1): cannot be entered
- Terminal cells: -1 at (3,1), +10 at (3,3); every other cell gives the living reward
- Actions: Up, Down, Left, Right (our assumption, following AIMA's grid world)
- Moving into the wall or off the grid leaves the robot in place (our assumption)
- There are 15 reachable states
- The transition model T and reward function R are UNKNOWN to the agent,
  so value/policy iteration (AIMA ch. 17) cannot be used directly; the agent
  must learn from experience (Q-learning, AIMA ch. 22)

## Hyperparameters
Chosen with experiments/sweep.py (one value varied at a time, 20 seeds each);
do not change them without rerunning the sweep and updating this section.
- Living reward: -0.04. Value iteration's optimal policy is the same for -0.04,
  -0.4 and -1, so a bigger penalty only lowers rewards; matches Lab 3.
- Discount factor (gamma): 0.9. Fewest steps (7.7); 0.5 is too short-sighted
  (9.0 steps) and 0.99 learns slower in 500 episodes (8.6 steps).
- Learning rate (alpha): 0.3. Best goal rate (99.6%, 7.8 steps vs 7.4 optimal);
  0.1 converges slower, 0.5+ is noisy under the 80/10/10 slippery moves.
- Epsilon (exploration): 0.1. 0 locks onto a longer route; 0.2+ wastes reward exploring.
- Episodes: 2000.

## Layout and coding standards
- aima/ is a vendored copy of the aima-python modules we need (mdp.py,
  reinforcement_learning.py, utils.py). Reuse its classes; do not edit it.
- vacuum/ holds our code: environment.py (the grid) and learning.py (training).
  experiments/ holds the hyperparameter sweep.
- aima quirks we work around in vacuum/, not by editing aima/: GridMDP treats a
  0 reward as a wall (so the living reward must be nonzero), and QLearningAgent
  wastes every other episode after a terminal (EpsilonGreedyQAgent resets instead).
- tests/ holds pytest tests; seed all randomness so results are reproducible.
- Python 3; docstrings and type hints on every function and class.
- Read only the notes and source definitions needed for the assigned task.

## Code features used (3 of 4)
- Hooks: .claude/settings.json runs scripts/context-switcher.sh on every prompt,
  loading the matching .claude/context/ note once per session.
- Skills: .claude/skills/ (hook-check, delegate), loaded when a task matches.
- Sub-agents: .claude/agents/ (rl-researcher, env-builder, code-reviewer).

## Delegation
- Use rl-researcher for focused AIMA/RL questions (including hyperparameter
  reasoning), env-builder for the grid environment, and code-reviewer for a
  supplied diff. Follow the delegate skill when briefing them.
- The parent supplies the goal, relevant paths, acceptance criteria, and
  boundaries; for edits, an explicit list of allowed paths. Never assign
  overlapping edit ownership; review only after edits are complete.
- Do not forward the whole conversation or all context notes.
- Specialists stop and report missing inputs or out-of-scope requests. They do
  not delegate further, commit, push, or change permissions.
- The parent integrates results, runs validation, and makes final decisions.
  A specialist's summary is not evidence that tests passed.
