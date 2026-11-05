# CS440 Lab 5 - Vacuum Robot with Q-Learning

A vacuum robot learns to reach the +10 cell of a 4x4 grid without knowing the
transition model or rewards in advance, using Q-learning (AIMA ch. 22).
This repository combines the Lab 4 configuration from our two strategy repos
(CS440-Lab4-Strat1 and CS440-Lab4-Strat4) and adds the implementation.

## Structure

```text
CLAUDE.md                     Claude Code entry point; imports AGENTS.md
AGENTS.md                     Project memory: grid, hyperparameters, standards, delegation
.claude/
    settings.json             HOOK: registers the UserPromptSubmit hook
    context/                  Notes the hook loads on demand
        environment.md        Grid layout, cells, actions, what the agent doesn't know
        mdp.md                AIMA ch. 17: MDPs, Bellman, why value iteration doesn't apply
        qlearning.md          AIMA ch. 22: Q-update, exploration, QLearningAgent
    skills/                   SKILLS
        hook-check/           Tests the hook from the shell (from Strat1)
        delegate/             Checklist for briefing a sub-agent (from Strat4)
    agents/                   SUB-AGENTS (from Strat4)
        rl-researcher.md      Read-only AIMA/RL research and hyperparameter reasoning
        env-builder.md        Builds the grid environment only
        code-reviewer.md      Read-only review of a supplied diff
scripts/context-switcher.sh   Hook script: prompt keywords -> context notes, once per session
aima/                         Vendored aima-python modules (mdp, reinforcement_learning, utils)
vacuum/                       Our code: environment.py, learning.py
tests/                        pytest tests
```

## Code features (3 of 4)

| Feature | Where | What it does |
| --- | --- | --- |
| Hooks | .claude/settings.json + scripts/context-switcher.sh | Loads the relevant note when a prompt mentions grid, MDP, or Q-learning topics |
| Skills | .claude/skills/ | hook-check tests the hook; delegate structures sub-agent briefs |
| Sub-agents | .claude/agents/ | Research, environment building, and review in separate contexts |

MCP is not used.

## Setup

```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
pytest
```

## Progress

- [x] Repo created; Lab 4 configuration merged from Strat1 and Strat4
- [ ] Grid environment (vacuum/environment.py) with tests
- [ ] Q-learning training (vacuum/learning.py) with tests
- [ ] Living reward, discount, learning rate, and epsilon selected and justified in AGENTS.md
- [ ] Results: learned policy grid, reward per episode, Q-values
