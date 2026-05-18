# Safe Reuse Policy — OpenClaw Agent Prompt Patterns

**Status:** CRITICAL — MUST READ BEFORE ANY PROMPT ADOPTION  
**Version:** 1.0  
**Date:** 2025-05-17  
**Authority:** OpenClaw Security Policy  

---

## Purpose

This repository contains leaked or publicly-circulated system prompts and tool schemas from third-party AI products (v0, Cursor, Manus, Devin, Replit, Lovable, RooCode). These materials carry significant legal, ethical, and operational risks. This policy establishes the non-negotiable rules for handling them within OpenClaw.

---

## Non-Negotiable Rules

### 1. Do Not Ship Vendor Prompts

Under no circumstances may any prompt, system instruction, tool schema, or internal operational document from a third-party vendor be shipped as part of OpenClaw, included in OpenClaw's default configuration, or distributed to OpenClaw users. This applies regardless of whether the material was obtained from public leaks, reverse engineering, or independent research.

**Rationale:** Shipping vendor prompts constitutes potential trade-secret misappropriation, violates the vendor's terms of service, and exposes OpenClaw to legal liability. It also undermines trust in the OpenClaw ecosystem.

### 2. Do Not Copy Source Prompts Directly into OpenClaw

Copy-pasting leaked prompts into OpenClaw's codebase, configuration files, or documentation is prohibited. This includes:
- Full system prompts
- Excerpts longer than a single sentence
- Paraphrased versions that retain vendor-specific identity claims
- Tool schemas copied verbatim

**Rationale:** Direct copying creates a clear chain of evidence for trade-secret claims and contaminates OpenClaw's intellectual property with derived work liability.

### 3. Do Not Preserve Vendor-Specific Identity Claims

Any prompt or instruction that contains a vendor identity claim ("You are Manus", "You are v0, Vercel's AI-powered assistant", "You are Devin", "You are Lovable", "You are Roo") must be stripped of that identity before any useful behavior is extracted.

**Rationale:** Identity claims are the most legally sensitive portion of leaked prompts. Preserving them is equivalent to impersonating the vendor's product and creates trademark and false-endorsement exposure.

### 4. Rewrite Useful Behavior into OpenClaw-Native Policy

If a leaked prompt contains genuinely useful behavioral patterns (e.g., "ask clarifying questions before coding", "validate output against requirements"), that behavior must be:
- Described in generic, vendor-neutral language
- Rewritten as OpenClaw-native policy or instructions
- Attributed only as "inspired by industry practice" if documented publicly
- Never attributed to the specific leaked source

**Rationale:** Behavioral patterns are not protectable, but their expression in a specific prompt may be. Rewriting ensures clean provenance.

### 5. Store Production Prompts Separately from Public Examples

Production system prompts used by OpenClaw's runtime must be stored in a separate, access-controlled repository or vault. They must never coexist in the same directory, branch, or documentation as public examples, research notes, or leaked-source comparisons.

**Rationale:** Co-location creates accidental disclosure risk. Separation ensures that even if a public example is compromised, production prompts remain protected.

### 6. Treat Tool Schemas as Privileged Operational Surfaces

Tool schemas define what an agent can do and how it interacts with the host system. They are not inert configuration — they are operational attack surfaces. Rules:
- Never expose tool schemas in public documentation without security review
- Never grant a tool more permissions than its minimum required function
- Never include tools that can execute arbitrary code without sandboxing
- Never include tools that can modify the host filesystem outside a restricted workspace
- Never include tools that can make outbound network requests without explicit allow-listing

**Rationale:** Exposed schemas enable attackers to enumerate capabilities, craft targeted jailbreaks, and exploit implementation gaps.

### 7. Require Capability Gating for Powerful Tools

Any tool that can:
- Execute shell commands
- Read or write arbitrary files
- Deploy code to production
- Access sensitive APIs or databases
- Send messages or emails externally
- Modify system configuration

...must require explicit capability gating. This means:
- The tool is disabled by default
- Enabling it requires explicit user opt-in
- Enabling it requires acknowledgment of risk
- The tool's scope is restricted to the minimum necessary
- Usage is logged and auditable

**Rationale:** Default-enable for powerful tools is the leading cause of agent-induced security incidents.

### 8. Require Explicit Approval for Destructive Actions

Any action that is destructive, irreversible, or has side effects outside the agent's workspace must require explicit user approval before execution. Destructive actions include but are not limited to:
- Deleting files or directories
- Modifying production databases
- Deploying to production environments
- Sending external communications
- Executing commands with elevated privileges
- Modifying system configuration
- Accessing credentials or secrets

The approval mechanism must:
- Clearly describe the action and its consequences
- Require an affirmative user gesture (not passive timeout)
- Be non-bypassable by prompt engineering or tool chaining
- Be logged for audit purposes

**Rationale:** Autonomous destructive actions are the most common vector for agent-induced harm, both accidental and malicious.

---

## Enforcement

- Violations of this policy are treated as security incidents
- Any commit that adds vendor prompts directly to OpenClaw will be reverted
- Any PR that ships vendor identity claims will be rejected
- Any production deployment that lacks capability gating for powerful tools will be blocked
- Any tool that performs destructive actions without approval will be flagged for emergency removal

---

## Exceptions

There are no exceptions to rules 1–3. Rules 4–8 may be tailored to specific OpenClaw modes or configurations, but the core principle (never ship vendor IP, always gate dangerous capabilities) is absolute.

---

## Related Documents

- `provenance_risk_report.md` — Analysis of authenticity and legal risk for each vendor prompt
- `prompt_leakage_risk_model.md` — Attack vectors from exposed system instructions
- `tool_schema_exposure_policy.md` — Schema-specific risk analysis and mitigation
