---
name: delegate
description: Parent-side procedure for one Strategy 4 delegation - pick the specialist, assemble a complete brief, snapshot the worktree, then check the handoff and confirm no unauthorized files changed. Use before invoking rl-researcher, env-builder, or code-reviewer, or when running the README's smoke tests.
---

# Delegate one bounded task

Delegation rules live in AGENTS.md and each specialist's limits live in
.claude/agents/. This skill does not restate them; it is the parent's checklist
for applying them to a single task. Skip it for small lookups you can do locally.

## 1. Pick one specialist
- Question about AIMA/RL theory or why something works -> rl-researcher
- Environment plan (or, after a scope update, authorized environment edits) -> env-builder
- Findings on a change that already exists -> code-reviewer
- A task that spans two of these is two delegations. Split it; do not widen one.

## 2. Gather inputs before writing the brief
Specialists have no shell and stop on missing inputs, so collect these first:

| Specialist | Must supply |
| --- | --- |
| rl-researcher | The question; aima/ paths if definitions are needed; which .claude/context/ note applies, if any |
| env-builder | aima/ paths (aima/mdp.py, etc.); acceptance criteria; "planning only" or the exact allowed edit paths |
| code-reviewer | The diff text, its comparison base, and the changed paths |

For a review, produce the diff yourself and paste it into the brief:

```sh
git diff <base> -- <paths>          # tracked changes
git status --porcelain --untracked-files=all   # list new files; include their contents too
```

The AIMA code this lab needs is vendored in aima/ (mdp.py, reinforcement_learning.py, utils.py).

## 3. Write the brief
Use these five headings and nothing else. Do not paste the conversation or
whole context notes; point to the one note that matters.

```text
Goal: <one sentence>
Inputs: <paths, source references, or the pasted diff + base>
Acceptance: <what a complete answer contains>
Boundaries: <read-only | planning only, no files | edit only: <paths>>
Return: <the handoff shape from the agent's ## Handoff section>
```

## 4. Snapshot, delegate, compare
Take a snapshot before any delegation, including read-only ones. `git diff`
alone misses untracked files.

```sh
snap=$(mktemp); git ls-files -co --exclude-standard -z | xargs -0 shasum > "$snap"
# ... run the specialist ...
git ls-files -co --exclude-standard -z | xargs -0 shasum | diff "$snap" -
```

- rl-researcher / code-reviewer / planning-only env-builder: diff must be empty.
- Authorized env-builder: every changed line must fall within the assigned paths.
- Run independent read-only delegations in parallel, then compare once. Never
  run two delegations that edit at the same time.

## 5. Accept or reject the handoff
Accept only if:
- It matches the Return shape in the brief and stays inside the Goal.
- Claims cite source paths/lines (research) or changed file/line (review).
- A blocker report names the specific missing input. If so, fix that input and
  re-delegate; do not do the specialist's work for it.
- Nothing claims tests passed. If validation is needed, run it yourself (pytest
  in tests/) and report the real output.

Then integrate the result and make the decision yourself. When findings from two
specialists conflict, check the cited sources instead of picking one.
