# Evidence Logging Policy

## Purpose
Define how the agent maintains audit trails, logs actions, and preserves evidence of work.

## Policy

### 1. Audit Trail
- Log all significant actions taken by the agent.
- Include timestamps, action types, and outcomes.
- Maintain the audit trail in a durable, append-only format.

### 2. WAL (Write-Ahead Logging)
- Before executing destructive actions, log the intent.
- Log the result of the action after execution.
- This ensures that actions can be replayed or audited later.

### 3. Tool Result Logging
- Save intermediate results to files when they are too large for context.
- Store different types of reference information in separate files.
- Log tool outputs for debugging and verification.

### 4. User Communication Logging
- Log user messages and agent responses for continuity.
- Do not log sensitive information (secrets, credentials).
- Respect user privacy in all logs.

### 5. Evidence Preservation
- Preserve evidence of completed work (files, outputs, screenshots).
- Make deliverables available as attachments when possible.
- Ensure logs are readable and useful for debugging.

### 6. Log Rotation
- Rotate logs to prevent unbounded growth.
- Retain logs for a reasonable period (e.g., 30 days).
- Archive old logs if they need to be kept longer.

## Risk Assessment
- **Low Risk**: Excessive logging can consume resources.
- **Medium Risk**: Missing logs can make debugging difficult.
- **Mitigation**: Structured logging, log rotation, and exclusion of sensitive data.

## References
- OpenClaw logging guidelines
- Audit trail best practices
