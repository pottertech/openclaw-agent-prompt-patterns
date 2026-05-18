# Integration Checklist

## Phase 1: Core Policies
- [ ] Copy policies to openclaw-cli-forge/docs/
- [ ] Update Karpathy Loop document
- [ ] Add feature flags for destructive action gating

## Phase 2: Agent-Specific
- [ ] Update Arty's system prompt
- [ ] Update Brodie's system prompt
- [ ] Update Emily's system prompt

## Phase 3: CI/CD
- [ ] Add policy tests to CI pipeline
- [ ] Set required vs optional test gates

## Phase 4: Security Hardening
- [ ] Implement destructive action gate
- [ ] Add secret redaction
- [ ] Enable capability gating
- [ ] Audit tool schema exposure
