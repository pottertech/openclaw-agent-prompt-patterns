# OpenClaw Integration Plan

## Where Each Policy Should Live

| Policy | Location | Format | Notes |
|--------|----------|--------|-------|
| `agent_loop_policy.md` | `~/.openclaw/workspace/openclaw-cli-forge/docs/` | Markdown | Core Karpathy Loop extension |
| `coding_agent_policy.md` | `~/.openclaw/workspace/openclaw-cli-forge/docs/` | Markdown | Coding agent behavior rules |
| `tool_use_policy.md` | `~/.openclaw/workspace/openclaw-cli-forge/docs/` | Markdown | Tool schema exposure rules |
| `edit_policy.md` | `~/.openclaw/workspace/openclaw-cli-forge/docs/` | Markdown | File editing atomicity |
| `database_safety_policy.md` | `~/.openclaw/workspace/openclaw-cli-forge/docs/` | Markdown | DB access patterns |
| `frontend_generation_policy.md` | `~/.openclaw/skills/` | SKILL.md | Frontend skill guidance |
| `secret_handling_policy.md` | `~/.openclaw/workspace/SECURITY.md` | Markdown | Secrets security |
| `progress_reporting_policy.md` | `~/.openclaw/workspace/openclaw-cli-forge/docs/` | Markdown | Status update rules |
| `destructive_action_policy.md` | `~/.openclaw/workspace/openclaw-cli-forge/docs/` | Markdown | Dangerous ops gate |
| `verification_policy.md` | `~/.openclaw/workspace/openclaw-cli-forge/docs/` | Markdown | Testing/linting rules |
| `rollback_policy.md` | `~/.openclaw/workspace/openclaw-cli-forge/docs/` | Markdown | Undo behavior |
| `evidence_logging_policy.md` | `~/.openclaw/workspace/openclaw-cli-forge/docs/` | Markdown | WAL patterns |

## Which Agents Should Use Which Policies

### Arty (Research Agent)
- `agent_loop_policy.md` - For research task loops
- `tool_use_policy.md` - For web search and browsing
- `evidence_logging_policy.md` - For citation tracking
- `progress_reporting_policy.md` - For status updates

### Brodie (Repo-Building Agent)
- `coding_agent_policy.md` - Primary policy
- `edit_policy.md` - For file modifications
- `verification_policy.md` - For testing changes
- `destructive_action_policy.md` - For rm/drop operations
- `rollback_policy.md` - For git reverts

### Emily (Infrastructure Agent)
- `database_safety_policy.md` - For DB operations
- `secret_handling_policy.md` - For credential management
- `destructive_action_policy.md` - For infrastructure changes
- `evidence_logging_policy.md` - For audit trails

### Jack Mercer (Security Agent)
- `tool_schema_exposure_policy.md` - For security analysis
- `secret_handling_policy.md` - For credential audits
- `destructive_action_policy.md` - For security boundaries
- `safe_reuse_policy.md` - For vendor prompt handling

### Professor Emily (Strategy Agent)
- `agent_loop_policy.md` - For planning loops
- `progress_reporting_policy.md` - For strategic updates
- `evidence_logging_policy.md` - For decision records

## Which Tests Should Run in CI

### Required Tests (Block Merge)
1. `agent_loop_cases.yaml` - Core loop behavior
2. `edit_policy_cases.yaml` - File editing safety
3. `destructive_action_cases.yaml` - Dangerous ops gates
4. `secret_handling_cases.yaml` - Credential handling
5. `database_safety_cases.yaml` - DB access safety

### Recommended Tests (Report Only)
6. `tool_selection_cases.yaml` - Tool choice logic
7. `verification_cases.yaml` - Testing requirements
8. `rollback_cases.yaml` - Undo behavior
9. `evidence_logging_cases.yaml` - Audit trail completeness
10. `frontend_generation_cases.yaml` - Frontend rules

### CI Integration
```yaml
# .github/workflows/policy-tests.yml
name: Policy Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run Policy Tests
        run: python tests/run_tests.py --required-only
      - name: Run Full Test Suite
        run: python tests/run_tests.py
```

## Rules in Agent Prompts vs Runtime Enforcement

### Agent Prompts (Soft Constraints)
- Read-before-edit guidance
- Minimal change preference
- Responsive design requirements
- Accessibility best practices
- Concise reporting style

### Runtime Enforcement (Hard Gates)
- Destructive action approval (require user confirm)
- Shell execution gating (capability check)
- Database write confirmation (explicit approve)
- Secret redaction (automatic)
- Tool schema access control (capability gating)

### WAL/Evidence Logging
- All tool calls logged
- File edit history preserved
- Test results recorded
- Error events captured
- User confirmations logged

## Feature Flags

| Feature | Flag | Default | Description |
|---------|------|---------|-------------|
| Destructive action gate | `GATE_DESTRUCTIVE` | `true` | Require approval for rm/drop/deploy |
| Shell execution | `ALLOW_SHELL` | `false` | Enable shell tool access |
| Database write | `ALLOW_DB_WRITE` | `false` | Enable DB mutation operations |
| Secret injection | `ALLOW_SECRET_INJECTION` | `false` | Allow runtime secret insertion |
| Frontend generation | `ENABLE_FRONTEND` | `true` | Enable web UI generation |
| Sub-agent delegation | `ALLOW_SUBAGENTS` | `true` | Enable parallel sub-agent spawning |
| MCP server access | `ALLOW_MCP` | `false` | Enable MCP tool server connections |
| Auto-deployment | `AUTO_DEPLOY` | `false` | Enable automatic deployment |

## Integration Steps

### Phase 1: Core Policies (Week 1)
1. Copy `agent_loop_policy.md` to `openclaw-cli-forge/docs/`
2. Copy `destructive_action_policy.md` to `openclaw-cli-forge/docs/`
3. Copy `edit_policy.md` to `openclaw-cli-forge/docs/`
4. Update Karpathy Loop document to reference new policies

### Phase 2: Agent-Specific (Week 2)
1. Update Arty's system prompt with research loop rules
2. Update Brodie's system prompt with coding rules
3. Update Emily's system prompt with infrastructure rules
4. Add feature flags to agent configuration

### Phase 3: CI/CD (Week 3)
1. Add policy tests to CI pipeline
2. Set required vs. optional test gates
3. Add test reporting

### Phase 4: Security Hardening (Week 4)
1. Implement destructive action gate
2. Add secret redaction
3. Enable capability gating
4. Audit tool schema exposure

## OpenClaw-Native Adaptations

### Karpathy Loop Integration
- `Observe` → Read files, check status
- `Orient` → Apply relevant policy
- `Decide` → Check feature flags
- `Act` → Execute with WAL logging

### Skill Integration
- Frontend generation policy → `frontend/` skill
- Database safety policy → `database/` skill
- Secret handling policy → `secrets/` skill

### Memory Integration
- Evidence logging → `MEMORY.md` and `memory/YYYY-MM-DD.md`
- Progress reporting → `HEARTBEAT.md`
- Rollback tracking → Git history + `memory/`
