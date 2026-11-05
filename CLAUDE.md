# Claude Code entry point

@AGENTS.md

Launch Claude Code from this repository root so it discovers .claude/settings.json,
.claude/skills/, and .claude/agents/. Shared project instructions live in
AGENTS.md; keep them there rather than duplicating them in this file.

The UserPromptSubmit hook loads relevant notes from .claude/context/ once per
session. Delegate bounded tasks to the specialists in .claude/agents/.
