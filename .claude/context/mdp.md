# MDP Notes (AIMA ch. 17, building on ch. 12 probability)

## Components of an MDP
- S: set of states (here: the 15 reachable grid cells)
- A(s): actions available in state s (Up, Down, Left, Right)
- T(s, a, s'): probability that action a in state s leads to s'
- R(s): reward for being in state s
- gamma: discount factor (0 to 1); how much future rewards count
- Policy pi(s): which action to take in each state

## Bellman equation (utility of a state)
U(s) = R(s) + gamma * max_a sum_s' T(s, a, s') * U(s')

## Solving an MDP when T and R ARE known
- Value iteration: repeat the Bellman update for every state until U converges
- Policy iteration: evaluate a policy, then improve it, until it stops changing
- aima-python: mdp.py has GridMDP, value_iteration, policy_iteration

## Why this does NOT work for our vacuum robot
- Both methods need T and R in advance. Our robot does not have them.
- Key question from lecture: "how can we do this update to V
  without knowing T and R?" -> learn from samples (see qlearning.md)
