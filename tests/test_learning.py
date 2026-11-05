"""Tests for the epsilon-greedy Q-learning agent."""

import pytest

from vacuum.environment import make_vacuum_mdp, to_xy
from vacuum.learning import EpsilonGreedyQAgent, run_episode, train


@pytest.fixture
def mdp():
    """The default vacuum grid."""
    return make_vacuum_mdp(living_reward=-0.04, gamma=0.9)


def test_q_update_matches_formula(mdp):
    agent = EpsilonGreedyQAgent(mdp, alpha=0.5, epsilon=0.0)
    s, s1 = to_xy((2, 3)), to_xy((3, 3))
    agent((s, -0.04))
    a = agent.a
    agent((s1, 10.0))
    # Q(s,a) = 0 + 0.5 * (r + gamma * max Q(s1) - 0), with Q(terminal) = its reward
    assert agent.Q[s, a] == pytest.approx(0.5 * (-0.04 + 0.9 * 10.0))


def test_terminal_ends_episode_and_resets(mdp):
    agent = EpsilonGreedyQAgent(mdp, alpha=0.5, epsilon=0.0)
    agent((to_xy((2, 3)), -0.04))
    assert agent((to_xy((3, 3)), 10.0)) is None
    assert agent.s is None and agent.a is None


def test_every_episode_takes_steps(mdp):
    # aima's agent alone would end every other episode after zero moves.
    agent = EpsilonGreedyQAgent(mdp, alpha=0.1, epsilon=0.1)
    steps = [run_episode(agent, mdp)[1] for _ in range(50)]
    assert all(n > 0 for n in steps)


def test_training_is_reproducible(mdp):
    _, first = train(mdp, 50, alpha=0.1, epsilon=0.1, seed=3)
    _, second = train(mdp, 50, alpha=0.1, epsilon=0.1, seed=3)
    assert first == second


def test_learned_policy_heads_to_goal(mdp):
    agent, rewards = train(mdp, 2000, alpha=0.1, epsilon=0.1, seed=0)
    policy = agent.greedy_policy(mdp)
    down, right = (0, -1), (1, 0)
    assert policy[to_xy((2, 3))] == down
    assert policy[to_xy((3, 2))] == right
    assert sum(rewards[-100:]) / 100 > 8
