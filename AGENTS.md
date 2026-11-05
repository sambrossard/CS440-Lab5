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
Chosen values and the reasoning for each are recorded here once experiments
justify them; do not change them without updating this section.
- Living reward: TBD
- Discount factor (gamma): TBD
- Learning rate (alpha): TBD
- Epsilon (exploration): TBD

## Layout and coding standards
- aima/ is a vendored copy of the aima-python modules we need (mdp.py,
  reinforcement_learning.py, utils.py). Reuse its classes; do not edit it.
- vacuum/ holds our code: environment.py (the grid) and learning.py (training).
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
