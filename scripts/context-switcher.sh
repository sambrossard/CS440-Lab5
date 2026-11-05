#!/usr/bin/env bash
# UserPromptSubmit hook: prints .claude/context notes matching prompt keywords,
# each at most once per session.

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"
CONTEXT_DIR="$PROJECT_DIR/.claude/context"
INPUT="$(cat)"

SESSION_ID="$(printf '%s' "$INPUT" | sed -n 's/.*"session_id"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')"
LOADED="/tmp/lab5-context-${SESSION_ID:-default}.txt"
touch "$LOADED"

add_context() {
  local file="$1"
  grep -qxF "$file" "$LOADED" && return 0
  echo "$file" >> "$LOADED"
  echo "--- context: $file ---"
  cat "$CONTEXT_DIR/$file"
  echo
}

if printf '%s' "$INPUT" | grep -Eiq 'grid|wall|cell|reward|terminal|environment'; then
  add_context environment.md
fi
if printf '%s' "$INPUT" | grep -Eiq 'mdp|bellman|value iteration|policy iteration|transition'; then
  add_context mdp.md
fi
if printf '%s' "$INPUT" | grep -Eiq 'q-learning|qlearning|q learning|q-value|epsilon|explor|reinforcement'; then
  add_context qlearning.md
fi

exit 0