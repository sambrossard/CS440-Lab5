"""Q-learning for the vacuum grid, reusing aima-python's QLearningAgent.

aima's agent explores with an exploration function (Ne, Rplus). The lab asks
for epsilon, so EpsilonGreedyQAgent keeps aima's Q-update and replaces the
action choice with epsilon-greedy.
"""

from __future__ import annotations

import random

from aima.mdp import MDP
from aima.reinforcement_learning import QLearningAgent


class EpsilonGreedyQAgent(QLearningAgent):
    """aima's QLearningAgent with epsilon-greedy exploration and a constant learning rate."""

    def __init__(self, mdp: MDP, alpha: float, epsilon: float) -> None:
        """Ne=0 makes aima's exploration function return Q itself, so its choice is greedy."""
        super().__init__(mdp, Ne=0, Rplus=0, alpha=lambda n: alpha)
        self.epsilon = epsilon

    def __call__(self, percept: tuple) -> tuple | None:
        """Update Q from the last step and return the next action (None at a terminal)."""
        state, reward = self.update_state(percept)
        if state in self.terminals:
            # A terminal's utility is its reward. Set it before aima's update so
            # the step into the terminal learns from it right away.
            self.Q[state, None] = reward
        action = super().__call__(percept)
        if state in self.terminals:
            # aima resets on the *next* call, which ends that episode at once;
            # resetting here keeps every episode.
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
    """Run one episode from mdp.init, like aima's run_single_trial but with a step cap.

    Returns the total reward collected and the number of moves made.
    """
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
