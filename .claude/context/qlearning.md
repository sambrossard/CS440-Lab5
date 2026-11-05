# Q-Learning Notes (AIMA ch. 22)

## Reinforcement learning basics

- The agent learns by acting: it observes (state, action, reward, next state).
- Model-based RL: learn T and R first, then solve the MDP.
- Model-free RL: skip T and R and learn action values directly (Q-learning).

## Q-values

- Q(s, a): expected total discounted reward of doing a in s, then acting optimally
- Best action in s = the a with the highest Q(s, a)

## Q-learning update (after each step s, a -> s' with reward r)

```text
Q(s, a) <- Q(s, a) + alpha * (r + gamma * max_a' Q(s', a') - Q(s, a))
```

- alpha: learning rate (how much each new sample changes Q)
- gamma: discount factor
- The term in parentheses is the temporal-difference (TD) error.

## Exploration vs exploitation

- The agent must sometimes try actions that look worse, or it never finds
  better paths.
- AIMA uses an exploration function f(u, n) with parameters Ne and Rplus:
  try each action at least Ne times, treating unexplored actions as worth Rplus.
- A common alternative is epsilon-greedy.

## In aima-python

- reinforcement_learning.py: QLearningAgent(mdp, Ne, Rplus, alpha)
- Hyperparameters (alpha, gamma, Ne, Rplus, episodes) will be chosen in the
  implementation; see the Hyperparameters section of AGENTS.md.
