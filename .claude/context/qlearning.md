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
- This lab uses epsilon-greedy instead: with probability epsilon take a
  random action, otherwise the action with the highest Q.

## In this repo

- vacuum/learning.py: EpsilonGreedyQAgent subclasses aima's QLearningAgent,
  keeping its Q-update but with Ne=0 (greedy), a constant alpha, and
  epsilon-greedy action choice. It also resets at each terminal, because
  aima's agent wastes the episode after one.
- train(mdp, episodes, alpha, epsilon, seed) trains a seeded agent;
  greedy_policy() returns the learned policy.
- Chosen values: alpha 0.3, gamma 0.9, epsilon 0.1, 2000 episodes
  (see the Hyperparameters section of AGENTS.md; set by experiments/sweep.py).
