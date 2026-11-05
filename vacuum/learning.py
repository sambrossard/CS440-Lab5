"""Epsilon-greedy Q-learning for the vacuum grid, built on aima's QLearningAgent."""

from __future__ import annotations

import random

from aima.mdp import MDP
from aima.reinforcement_learning import QLearningAgent


class EpsilonGreedyQAgent(QLearningAgent):
    """aima's QLearningAgent with epsilon-greedy exploration and a constant learning rate."""

    def __init__(self, mdp: MDP, alpha: float, epsilon: float) -> None:
        """Ne=0 makes aima's own action choice greedy."""
        super().__init__(mdp, Ne=0, Rplus=0, alpha=lambda n: alpha)
        self.epsilon = epsilon

    def __call__(self, percept: tuple) -> tuple | None:
        """Update Q from the last step and return the next action (None at a terminal)."""
        state, reward = self.update_state(percept)
        if state in self.terminals:
            # A terminal's Q is its reward; set it before aima's update uses it.
            self.Q[state, None] = reward
        action = super().__call__(percept)
        if state in self.terminals:
            # Reset now; aima would reset on the next call and waste that episode.
            self.reset_episode()
            return None
        if random.random() < self.epsilon:
            action = random.choice(self.all_act)
            self.a = action
        return action

    def reset_episode(self) -> None:
        """Forget the previous step so the next percept starts a new episode."""
        self.s = self.a = self.r = None

    def greedy_policy(self, mdp: MDP) -> dict:
        """Return the best learned action for every non-terminal state."""
        return {
            state: max(self.all_act, key=lambda action: self.Q[state, action])
            for state in mdp.states
            if state not in mdp.terminals
        }


def sample_next_state(mdp: MDP, state: tuple, action: tuple) -> tuple:
    """Sample the next state from the environment's T (hidden from the agent)."""
    outcomes = mdp.T(state, action)
    return random.choices([s for _, s in outcomes], weights=[p for p, _ in outcomes])[0]


def run_episode(agent: EpsilonGreedyQAgent, mdp: MDP, max_steps: int = 200) -> tuple[float, int]:
    """Run one capped episode from mdp.init; return (total reward, moves made)."""
    state = mdp.init
    total_reward = 0.0
    for steps in range(max_steps + 1):
        reward = mdp.R(state)
        total_reward += reward
        action = agent((state, reward))
        if action is None:
            return total_reward, steps
        state = sample_next_state(mdp, state, action)
    agent.reset_episode()
    return total_reward, max_steps


def train(
    mdp: MDP, episodes: int, alpha: float, epsilon: float, seed: int = 0
) -> tuple[EpsilonGreedyQAgent, list[float]]:
    """Train a new agent for ``episodes`` episodes; return it and the reward of each episode."""
    random.seed(seed)
    agent = EpsilonGreedyQAgent(mdp, alpha=alpha, epsilon=epsilon)
    rewards = [run_episode(agent, mdp)[0] for _ in range(episodes)]
    return agent, rewards
