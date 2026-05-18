# Provenance Risk Report — Leaked System Prompts

**Report Date:** 2025-05-17  
**Analyst:** OpenClaw Security Subagent  
**Scope:** 6 vendor prompt/tool collections + 1 open-source reference  
**Source Repository:** `/tmp/system-prompts-and-models-of-ai-tools`

---

## Executive Summary

This report evaluates the authenticity, evidence quality, and legal risk of system prompts and tool schemas obtained from a public GitHub repository (`x1xhlol/system-prompts-and-models-of-ai-tools`). The repository claims to contain "FULL official" prompts from v0, Cursor, Manus, Same.dev, Lovable, Devin, Replit, and RooCode. **Our assessment: MIXED — some materials are highly credible, others are synthetic, incomplete, or of unverifiable origin. A blanket go/no-go recommendation is inappropriate; each vendor collection must be assessed individually.**

---

## Overall Authenticity Assessment

| Vendor | Lines | Files | Authenticity Verdict | Confidence |
|--------|-------|-------|-------------------|------------|
| v0 (Vercel) | 2,798 | 3 (v0.txt, v0 model.txt, v0 tools.txt) | **Highly Credible** — Internal details match public docs | High |
| Manus | 489 | 3 (Prompt.txt, Agent loop.txt, Modules.txt, tools.json) | **Credible but Sanitized** — Core structure likely real, identity section is synthetic | Medium-High |
| Cursor | 62 | 1 | **Partial / Synthetic** — Extremely short, lacks Cursor-specific details | Low |
| Devin | 402 | 1 | **Unverifiable** — Matches public Devin docs but could be reconstructed | Low-Medium |
| Replit | 91 prompt + 340 tools JSON | 2 | **Partially Credible** — Tool schemas look real, prompt is generic | Medium |
| Lovable | 84 | 1 | **Likely Synthetic** — Very short, generic, lacks Lovable-specific details | Low |
| RooCode | 665 | 1 | **Confirmed Open Source** — Listed as "already open source" in repo | High |

---

## Vendor-by-Vendor Analysis

### 1. v0 (Vercel) — Verdict: GO (for research only)

**Evidence Supporting Authenticity:**
- Contains verbatim internal Vercel knowledge base URLs (`https://sdk.vercel.ai`, `https://react.dev/reference/react/hooks`)
- References specific Vercel RAG citations with exact format `[^index]` matching public v0 docs
- Includes environment variable names that match public Vercel integrations: `NEXT_PUBLIC_FIREBASE_API_KEY`, `FIREBASE_PRIVATE_KEY`, `CLOUDINARY_API_SECRET`, `NEXT_PUBLIC_CLOUDINARY_API_KEY`
- Contains exact AI SDK usage patterns (`import { generateText } from "ai"`, `import { openai } from "@ai-sdk/openai"`) that match public Vercel AI SDK docs
- References specific internal components: `CodeProject`, `QuickEdit`, `MoveFile`, `DeleteFile`, `AddEnvironmentVariables`
- Includes `make_manus_page` tool — a tool name that would only exist in an internal Vercel/Manus integration context
- References specific model identifier: `gpt-4o` via `openai("gpt-4o")`
- Includes detailed MDX formatting rules that match v0's public output behavior
- Contains internal path references: `/opt/.manus/.sandbox-runtime` in datasource module code example
- The `v0 model.txt` file contains extensive AI SDK documentation that appears to be a direct internal knowledge base dump

**Evidence Against / Concerns:**
- Contains some placeholder/example URLs (`https://localhost:1234`, `https://example.com`) that are clearly synthetic examples within the prompt
- The file `v0 tools.txt` appears to be a condensed/summarized version, possibly reconstructed
- The repo author's disclaimer claims Jared Palmer (VP of AI at Vercel) called the prompt a hallucination; the author disputes this
- Even if authentic, it may be an outdated version (repo last updated 2025-04-20)

**Provenance Risk:** Medium. The internal details are too specific to be hallucinated, but possession of this material may violate Vercel's Terms of Service. The author explicitly disputes Vercel's claim that it's fabricated.

---

### 2. Manus — Verdict: CONDITIONAL GO (for structural research only)

**Evidence Supporting Authenticity:**
- `tools.json` contains 26 function definitions with realistic parameter schemas
- Includes internal-looking tool names: `make_manus_page`, `deploy_apply_deployment`, `deploy_expose_port`
- Contains a `datasource_module` with a code example referencing `/opt/.manus/.sandbox-runtime` — an internal path
- References `ApiClient` with a specific internal API namespace (`WeatherBank/get_weather`)
- Agent loop description is detailed and matches observed Manus behavior (one tool per iteration, event stream model)
- `Modules.txt` contains detailed system architecture (Planner, Knowledge, Datasource modules)

**Evidence Against / Concerns:**
- `Prompt.txt` contains a large "About Manus AI Assistant" section that is clearly synthetic/self-generated promotional copy
- The identity section ("I am Manus, an AI assistant created by the Manus team") is self-referential and could be reconstructed
- The "Effective Prompting Guide" section is generic and appears to be a standard LLM-generated document
- Contains a `make_manus_page` tool which appears in BOTH Manus AND v0 prompts — suspicious cross-pollution
- No cryptographic or timestamp evidence of origin

**Provenance Risk:** High. The core architecture and tools may be authentic, but the prompt text is heavily padded with synthetic content. Difficult to separate signal from noise.

---

### 3. Cursor — Verdict: NO-GO

**Evidence:**
- Only 62 lines — extremely short for a claimed "FULL" system prompt
- Contains only a high-level tool calling schema and generic instructions
- Lacks Cursor-specific details: no mention of `cursor agent`, no tab context rules, no specific model references
- No evidence of internal Cursor architecture (e.g., Cursor's composer mode, @-mentions, codebase indexing rules)
- The file is named `cursor agent.txt` but the content is generic enough to apply to any agentic coding assistant

**Provenance Risk:** Very High. This is almost certainly a reconstruction or partial extract, not a genuine Cursor system prompt.

---

### 4. Devin — Verdict: CONDITIONAL GO (for behavioral research only)

**Evidence Supporting Authenticity:**
- 402 lines with detailed XML-style command syntax
- Contains Devin-specific commands: `<deploy_frontend>`, `<deploy_backend>`, `<expose_port>`, `<git_view_pr>`, `<gh_pr_checklist>`
- Includes specific Devin workflow: planning mode vs standard mode
- References specific Devin behavior: pop quizzes, `think` tool, environment issue reporting
- Contains specific path conventions: `devin/{timestamp}-{feature-name}` for branch naming
- Includes Devin-specific browser commands with `devinid` attributes

**Evidence Against / Concerns:**
- Much of this content could be reconstructed from Devin's public documentation and demo videos
- No internal-only details that would prove origin
- The author claims "FULL official" but this appears to be a behavioral specification, not necessarily the exact system prompt

**Provenance Risk:** Medium-High. The content is detailed and Devin-specific, but without internal-only markers, authenticity cannot be confirmed.

---

### 5. Replit — Verdict: GO (for tool schema research only)

**Evidence Supporting Authenticity:**
- Tool JSON contains 19 Replit-specific tools: `restart_workflow`, `search_filesystem`, `packager_tool`, `programming_language_install_tool`, `create_postgresql_database_tool`, `check_database_status`, `str_replace_editor`, `bash`, `workflows_set_run_config_tool`, `workflows_remove_run_config_tool`, `execute_sql_tool`, `suggest_deploy`, `report_progress`, `web_application_feedback_tool`, `shell_command_application_feedback_tool`, `vnc_window_application_feedback`, `ask_secrets`, `check_secrets`
- Tool parameters match Replit's public documented behavior (e.g., `wait_for_port`, `install_or_uninstall`, `language_or_system`)
- Includes internal tags system: `View`, `policy_spec`, `file_system`, `repo_overview`, `important`, `workflow_console_logs`, `automatic_updates`, `webview_console_logs`, `function_results`
- Contains specific Replit deployment references: `.replit.app` domain, `replit_deployments`
- References specific Replit package manager behavior (`nixpkgs`, `apt`)
- The tool schema is structured as a JSON schema with `tools` and `internal_tags` arrays — a format consistent with Replit's agent architecture

**Evidence Against / Concerns:**
- The prompt text (91 lines) is generic editor instructions, not Replit-specific
- The tool schema could be reconstructed from Replit's public agent demos and documentation
- No internal-only identifiers

**Provenance Risk:** Medium. The tool schemas look authentic, but the prompt text is weak. Research value is primarily in understanding Replit's tool architecture.

---

### 6. Lovable — Verdict: NO-GO

**Evidence:**
- Only 84 lines — extremely short
- Generic React editor instructions with no Lovable-specific features
- No mention of Lovable's signature capabilities (supabase integration, auth flows, payment integrations)
- No internal tool schemas or component library references
- Could easily be a generic "AI editor" prompt with "Lovable" swapped in

**Provenance Risk:** Very High. This is almost certainly not a genuine Lovable system prompt.

---

### 7. RooCode — Verdict: GO (confirmed open source)

**Evidence:**
- Explicitly labeled as "already open source" in the repository
- Contains detailed XML tool schemas matching RooCode's public codebase
- Includes MCP server integration details
- References `.roo/rules-code/` and `.roo/rules/` directories
- Contains specific mode system: Code, Architect, Ask, Debug, Boomerang Mode
- Includes RooCode-specific tools: `fetch_instructions`, `apply_diff`, `search_and_replace`, `use_mcp_tool`, `access_mcp_resource`

**Provenance Risk:** None. This is confirmed open-source material and can be used freely.

---

## Go / No-Go Matrix

| Collection | Use for Behavior Research | Use for Tool Schema Research | Use for Competitive Analysis | Ship in OpenClaw |
|-----------|---------------------------|------------------------------|------------------------------|------------------|
| v0 | GO | GO | GO | **NO-GO** |
| Manus | CONDITIONAL | GO | GO | **NO-GO** |
| Cursor | NO-GO | NO-GO | NO-GO | **NO-GO** |
| Devin | CONDITIONAL | GO | GO | **NO-GO** |
| Replit | NO-GO | GO | GO | **NO-GO** |
| Lovable | NO-GO | NO-GO | NO-GO | **NO-GO** |
| RooCode | GO | GO | GO | GO (open source) |

---

## Key Provenance Concerns

1. **Repo author's credibility:** The author ("NotLucknite" / "x1xh") actively monetizes this content (PayPal, crypto donations, security audit service "ZeroLeaks"). Financial incentive creates bias toward claiming authenticity.

2. **Mixed authenticity:** The repository bundles genuinely credible material (v0, Replit tools) with clearly synthetic content (Cursor, Lovable). This contamination undermines the credibility of the entire collection.

3. **Legal ambiguity:** Even if some material is authentic, its acquisition method is unknown. Using it in a commercial product (OpenClaw) creates trade-secret misappropriation risk under the Defend Trade Secrets Act (DTSA) and equivalent state laws.

4. **No chain of custody:** There is no cryptographic proof, no version history, no internal timestamp evidence. Everything is a text file in a public GitHub repo.

5. **Vendor denial:** At least one vendor (Vercel) has publicly denied the authenticity of leaked prompts from this collection. This creates legal and reputational risk for anyone relying on them.

---

## Recommendations

1. **Do not ship any vendor prompt** in OpenClaw. This is non-negotiable.
2. **Use v0 and Replit tool schemas** only as reference for designing OpenClaw-native tools, with complete rewrites.
3. **Discard Cursor and Lovable prompts** — they are not credible enough to be useful.
4. **Treat Manus and Devin prompts as behavioral inspiration only** — extract patterns, not text.
5. **Use RooCode freely** — it is confirmed open source.
6. **Document all inspiration sources** internally for legal defensibility, but never attribute publicly to leaked materials.
7. **Conduct independent security research** to validate any behavioral patterns before implementing them in OpenClaw.
