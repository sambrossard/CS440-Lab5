---
name: hook-check
description: Test the context-switcher hook from the shell by feeding it fake prompts and checking which topic notes it loads. Use after editing scripts/context-switcher.sh or adding a note to .claude/context/, or when a note doesn't load (or loads twice) as expected.
---

# Hook check

Tests `scripts/context-switcher.sh` without starting a Claude Code session.
Claude Code sends the hook a JSON object on stdin, so these checks send the
same kind of object and look at which notes the script prints.

## Setup

Run from the repo root:

```sh
export CLAUDE_PROJECT_DIR="$PWD"
run() { printf '{"session_id":"%s","prompt":"%s"}' "$1" "$2" \
  | bash scripts/context-switcher.sh | grep '^--- context:'; }
S=hookcheck-$$
```

## Checks

| # | Command | Expected |
| --- | --- | --- |
| 1 | `run $S "Explain Q-learning"` | `qlearning.md` |
| 2 | `run $S "Explain Q-learning"` | nothing (already loaded this session) |
| 3 | `run $S "Describe the grid"` | `environment.md` |
| 4 | `run $S "Explain Bellman"` | `mdp.md` |
| 5 | `run $S-b "bellman update on the grid with epsilon"` | all three notes, in a new session |
| 6 | `run $S-c "hello"` | nothing |

If you added a topic, add a row with one of its keywords. Also check that a
prompt with a different topic's keyword doesn't load your note.

## Clean up

```sh
rm -f /tmp/lab5-context-$S*.txt
```

## What to watch for

- **Too many matches:** keywords are substrings, so `cell` also matches
  "excellent". The script also searches the whole JSON object, not just the
  prompt, so a word in a field like `cwd` can trigger a note.
- **Duplicate loads:** the script records loaded notes in
  `/tmp/lab5-context-<session_id>.txt`. If `session_id` doesn't parse,
  every session shares the `default` file.
- **Line endings:** if Windows CRLF line endings get into the script, Bash
  fails with errors like `$'\r': command not found`. `.gitattributes` keeps
  `.sh` files on LF.

Passing these checks shows that routing and once-per-session loading work.
It doesn't show that Claude Code actually adds the notes to the conversation.
For that, follow the in-session steps in `README.md`.
