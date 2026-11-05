"""Hyperparameter sweep used to choose the values recorded in AGENTS.md.

Changes one value at a time from the chosen baseline and averages over seeds.
Run from the repository root: python -m experiments.sweep
"""

from __future__ import annotations

import random
import statistics

from aima.mdp import GridMDP, best_policy, value_iteration
from vacuum.environment import make_vacuum_mdp, to_xy
from vacuum.learning import sample_next_state, train

BASELINE = {"living_reward": -0.04, "gamma": 0.9, "alpha": 0.3, "epsilon": 0.1}
SWEEP = {
    "living_reward": [-0.01, -0.04, -0.1, -0.4, -1.0],
    "gamma": [0.5, 0.8, 0.9, 0.99],
    "alpha": [0.01, 0.05, 0.1, 0.3, 0.5, 0.9],
    "epsilon": [0.0, 0.05, 0.1, 0.2, 0.3, 0.5],
}


def evaluate(mdp: GridMDP, policy: dict, runs: int = 200, max_steps: int = 100) -> tuple[float, float]:
    """Follow ``policy`` greedily; return the fraction of runs reaching +10 and the mean steps."""
    goal = to_xy((3, 3))
    wins, steps = 0, []
    for _ in range(runs):
        state, count = mdp.init, 0
        while state not in mdp.terminals and count < max_steps:
            state = sample_next_state(mdp, state, policy[state])
            count += 1
        wins += state == goal
        steps.append(count)
    return wins / runs, statistics.mean(steps)


def score(living_reward: float, gamma: float, alpha: float, epsilon: float,
          episodes: int = 500, seeds: int = 20) -> dict:
    """Train with one setting over several seeds and average the results."""
    mdp = make_vacuum_mdp(living_reward, gamma)
    optimal = best_policy(mdp, value_iteration(mdp))
    results = {"goal": [], "steps": [], "matches_vi": [], "train_reward": []}
    for seed in range(seeds):
        agent, rewards = train(mdp, episodes, alpha=alpha, epsilon=epsilon, seed=seed)
        policy = agent.greedy_policy(mdp)
        random.seed(1000 + seed)
        goal, steps = evaluate(mdp, policy)
        results["goal"].append(goal)
        results["steps"].append(steps)
        results["matches_vi"].append(sum(policy[s] == optimal[s] for s in policy) / len(policy))
        results["train_reward"].append(statistics.mean(rewards[-100:]))
    return {key: statistics.mean(values) for key, values in results.items()}


def main() -> None:
    """Print one table row per setting."""
    print(f"{'setting':<22}{'goal%':>7}{'steps':>7}{'=VI%':>7}{'train R':>9}")
    for name, values in SWEEP.items():
        for value in values:
            result = score(**{**BASELINE, name: value})
            print(f"{name + '=' + str(value):<22}{result['goal'] * 100:>6.1f}%{result['steps']:>7.1f}"
                  f"{result['matches_vi'] * 100:>6.1f}%{result['train_reward']:>9.2f}")
        print()


if __name__ == "__main__":
    main()
