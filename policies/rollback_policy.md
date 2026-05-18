# Rollback Policy

## Purpose
Define how the agent handles reversion, recovery, and undo behavior for file changes and actions.

## Policy

### 1. Undo Capability
- The agent must support undoing the last edit made to a file.
- Use the undo tool to revert changes when available.
- Document changes so they can be manually reversed if needed.

### 2. Recovery from Errors
- If an edit corrupts a file, immediately revert the change.
- If a tool execution fails, attempt to recover gracefully.
- When multiple approaches fail, report the failure and ask for user assistance.

### 3. Version Control
- Use git for version control when available.
- Make commits with clear messages after significant changes.
- Never force push; ask the user for help if push fails.

### 4. State Recovery
- The agent must recover from crashes or interruptions.
- On restart, read the current state to understand what has been done.
- Rebuild the plan if the task objective has changed.

### 5. User-Initiated Rollback
- If the user requests a rollback, comply immediately.
- Use the project's rollback mechanisms (e.g., git revert, undo_edit).
- Confirm the rollback was successful.

## Risk Assessment
- **High Risk**: Inability to rollback can lead to permanent data loss.
- **Medium Risk**: Incorrect rollback can revert wanted changes.
- **Mitigation**: Use version control, test after rollback, and confirm with the user.

## References
- OpenClaw rollback and recovery guidelines
- Git best practices
