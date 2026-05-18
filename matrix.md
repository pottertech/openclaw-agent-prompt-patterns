# OpenClaw Policy-to-Agent Assignment Matrix

| Policy | Tests | Agents | Prompt Rules | Runtime Rules | WAL Rules | Feature Flag |
|--------|-------|--------|--------------|---------------|-----------|--------------|
| agent_loop_policy.md | agent_loop_cases.yaml | Arty, Brodie, Emily, Jack Mercer, Professor Emily | One tool per turn, terminal states | Retry limits, state transitions | Loop iteration logs | — |
| coding_agent_policy.md | — | Arty, Brodie, Jack Mercer | Read before edit, minimal changes | Batching enforcement | Edit audit trail | — |
| database_safety_policy.md | database_safety_cases.yaml | Arty, Brodie, Emily | Read-only by default, use ORM | Query gating, approval flows | Query intent + result logs | ENABLE_DB_WRITE_APPROVAL |
| destructive_action_policy.md | destructive_action_cases.yaml | Arty, Brodie, Emily, Jack Mercer, Professor Emily | Describe consequences | Approval gate, dry-run | Intent + approval + result | ENABLE_DESTRUCTIVE_ACTIONS |
| edit_policy.md | — | Arty, Brodie, Jack Mercer | Exact match, atomicity | Edit validation | Pre/post file hashes | — |
| evidence_logging_policy.md | evidence_logging_cases.yaml | Arty, Brodie, Emily, Jack Mercer, Professor Emily | Log significant actions | Structured log emission | WAL entries, audit trail | — |
| frontend_generation_policy.md | frontend_generation_cases.yaml | Arty, Brodie, Jack Mercer | Framework defaults, component rules | Build lint, preview gate | Deploy logs | ENABLE_AUTO_DEPLOY |
| progress_reporting_policy.md | — | Arty, Brodie, Emily, Jack Mercer, Professor Emily | Concise updates, evidence attachments | Notification routing | Status change logs | — |
| rollback_policy.md | rollback_cases.yaml | Arty, Brodie, Jack Mercer, Professor Emily | Undo capability, git best practices | Revert tool execution | Rollback records | — |
| secret_handling_policy.md | secret_handling_cases.yaml | Arty, Brodie, Emily, Jack Mercer, Professor Emily | Never hardcode, redact logs | Secret scanner, redaction filter | Access logs (without values) | ENABLE_SECRET_INJECTION |
| tool_use_policy.md | — | Arty, Brodie, Emily, Jack Mercer, Professor Emily | Schema verification, one tool per turn | Tool call validation | Tool invocation logs | — |
| verification_policy.md | verification_cases.yaml | Arty, Brodie, Jack Mercer | Run tests, fix lint errors | CI gate, test runner | Test result logs | — |

## CI Test Mapping

All `*_cases.yaml` files in `tests/` should run in CI.

| Test File | Policy Covered | Priority |
|-----------|----------------|----------|
| agent_loop_cases.yaml | agent_loop_policy.md | Standard |
| database_safety_cases.yaml | database_safety_policy.md | Critical |
| destructive_action_cases.yaml | destructive_action_policy.md | Critical |
| edit_policy_cases.yaml | edit_policy_policy.md | Standard |
| evidence_logging_cases.yaml | evidence_logging_policy.md | Standard |
| frontend_generation_cases.yaml | frontend_generation_policy.md | Standard |
| rollback_cases.yaml | rollback_policy.md | Standard |
| secret_handling_cases.yaml | secret_handling_policy.md | Critical |
| tool_selection_cases.yaml | tool_selection_policy.md | Standard |
| verification_cases.yaml | verification_policy.md | Standard |

## Legend

- **Prompt Rules**: Injected into the agent's system prompt at runtime.
- **Runtime Rules**: Enforced by the OpenClaw executor / gatekeeper layer.
- **WAL Rules**: Logged to the Write-Ahead Log for audit and replay.
- **Feature Flag**: Must be enabled explicitly; disables the policy's risky paths by default.
