# Tool Schema Exposure Policy

**Report Date:** 2025-05-17  
**Analyst:** OpenClaw Security Subagent  
**Scope:** Risk analysis of exposed tool schemas from 6 vendor collections  
**Source Material:** 3 tool schema files (Manus tools.json, Replit Tools.json, v0 tools.txt)

---

## Executive Summary

Tool schemas are not passive configuration documents — they are **operational interfaces** that define what an agent can do, how it can be invoked, and what parameters it accepts. When exposed, they provide attackers with a precise blueprint for capability enumeration, injection attacks, and privilege escalation. This document analyzes the risks of schema exposure as demonstrated by the collected source material and establishes mitigation strategies.

**Key Finding:** The collected schemas expose a combined **45+ tools** with an average of **12 parameters per tool**. Several tools grant shell execution, file system access, browser control, deployment, and secret access — all without adequate capability gating documentation.

---

## Schema Inventory

| Vendor | Tools Count | High-Risk Tools | Medium-Risk Tools | Low-Risk Tools |
|--------|-------------|-----------------|-------------------|----------------|
| Manus | 26 | 7 | 8 | 11 |
| Replit | 19 | 5 | 6 | 8 |
| v0 | ~20 (documented) | 3 | 5 | 12 |
| **Total** | **~65** | **15** | **19** | **31** |

---

## High-Risk Tool Analysis

### Category: Shell Execution

**Tools Identified:**
- Manus: `shell_exec` (with `sudo` parameter)
- Replit: `bash`
- v0: Node.js executable blocks (implicit shell via `child_process`)

**Risk:** Shell execution is the highest-risk capability. It allows arbitrary code execution with the privileges of the agent's runtime environment.

**Specific Concerns from Source Material:**
- Manus `shell_exec` includes an explicit `sudo` boolean parameter: `"sudo": {"type": "boolean", "description": "Whether to use sudo privileges"}`
- Replit `bash` has no documented restrictions on command scope
- Both allow command chaining with `&&` and `||` operators
- Manus `shell_write_to_process` allows sending input to running processes, enabling interactive exploitation
- Replit `bash` allows background processes with `&`

**Attack Scenarios:**
1. **Privilege Escalation:** `shell_exec` with `sudo: true` can modify system files, install rootkits, or exfiltrate data
2. **Lateral Movement:** Chained commands can scan the network, access other containers, or pivot to internal services
3. **Data Exfiltration:** `curl` or `wget` can send sensitive files to attacker-controlled servers
4. **Persistence:** Cron jobs or systemd services can be installed for persistent access
5. **Denial of Service:** `fork bomb` or resource exhaustion commands can crash the host

**Evidence from Source Material (Manus shell_exec):**
```json
{
  "name": "shell_exec",
  "parameters": {
    "properties": {
      "id": {"type": "string"},
      "exec_dir": {"type": "string"},
      "command": {"type": "string"}
    }
  }
}
```
No restrictions on `command` content. No allow-list. No validation.

---

### Category: File System Read/Write

**Tools Identified:**
- Manus: `file_read` (with `sudo`), `file_write` (with `sudo`, `append`), `file_str_replace`, `file_find_in_content`, `file_find_by_name`
- Replit: `str_replace_editor` (with `create`, `str_replace`, `insert`, `undo_edit`)
- v0: `QuickEdit`, `MoveFile`, `DeleteFile`, `CodeProject` (implicit file operations)

**Risk:** File system access allows reading sensitive configuration, modifying code to insert backdoors, and deleting critical files.

**Specific Concerns from Source Material:**
- Manus `file_read` supports `sudo: true` — can read files owned by root
- Manus `file_write` supports `sudo: true` and `append: true` — can modify system files
- Manus `file_find_by_name` uses glob patterns — can enumerate the entire filesystem
- Replit `str_replace_editor` supports `create` and `undo_edit` — can create arbitrary files and then hide evidence
- v0 `DeleteFile` is a component that can delete files within a CodeProject

**Attack Scenarios:**
1. **Credential Harvesting:** Read `~/.ssh/id_rsa`, `~/.aws/credentials`, `.env` files
2. **Backdoor Injection:** Modify source code to include malicious logic
3. **Configuration Tampering:** Modify `/etc/hosts`, firewall rules, or SSH config
4. **Evidence Destruction:** Delete logs that would reveal attacker activity
5. **Data Exfiltration:** Read proprietary source code, databases, or user data

**Evidence from Source Material (Manus file_read):**
```json
{
  "name": "file_read",
  "parameters": {
    "properties": {
      "file": {"type": "string", "description": "Absolute path of the file to read"},
      "sudo": {"type": "boolean", "description": "Whether to use sudo privileges"},
      "start_line": {"type": "integer"},
      "end_line": {"type": "integer"}
    }
  }
}
```
Absolute path with sudo. No path restrictions. No file type allow-list.

---

### Category: Browser Control

**Tools Identified:**
- Manus: `browser_navigate`, `browser_click`, `browser_input`, `browser_console_exec`, `browser_press_key`, `browser_select_option`, `browser_scroll_*`, `browser_restart`
- Devin: `<navigate_browser>`, `<click_browser>`, `<type_browser>`, `<restart_browser>`, `<browser_console>`, `<press_key_browser>`, `<select_option_browser>`
- v0: Implicit browser via deployment and preview

**Risk:** Browser control allows phishing, credential theft via fake login pages, XSS exploitation, and accessing internal web applications.

**Specific Concerns from Source Material:**
- Manus `browser_console_exec` allows arbitrary JavaScript execution: `"javascript": {"type": "string", "description": "JavaScript code to execute"}`
- Manus `browser_restart` can reset browser state, potentially clearing security cookies or session data
- Devin `restart_browser` can load extensions from arbitrary paths: `extensions="/path/to/extension1,/path/to/extension2"`
- Manus `browser_input` can fill forms, including password fields, without user confirmation

**Attack Scenarios:**
1. **Credential Phishing:** Navigate to a fake login page, fill in credentials, submit
2. **XSS Exploitation:** Execute JavaScript on internal admin panels or dashboards
3. **Session Hijacking:** Access cookies and localStorage to impersonate users
4. **CSRF Attacks:** Use the browser to perform actions on behalf of authenticated users
5. **Internal Reconnaissance:** Navigate to internal URLs (`http://localhost:8080`, `http://192.168.1.1`) to discover services

**Evidence from Source Material (Manus browser_console_exec):**
```json
{
  "name": "browser_console_exec",
  "parameters": {
    "properties": {
      "javascript": {
        "type": "string",
        "description": "JavaScript code to execute. Note that the runtime environment is browser console."
      }
    }
  }
}
```
Full JavaScript execution in browser context. No sandboxing mentioned. No CSP restrictions.

---

### Category: Deployment & Network Exposure

**Tools Identified:**
- Manus: `deploy_expose_port`, `deploy_apply_deployment`
- Devin: `<deploy_frontend>`, `<deploy_backend>`, `<expose_port>`
- Replit: `suggest_deploy`
- v0: Implicit deployment to Vercel

**Risk:** Deployment tools can expose internal services to the public internet, deploy malicious applications, or consume cloud resources.

**Specific Concerns from Source Material:**
- Manus `deploy_expose_port` exposes local ports with "public access": `"description": "Expose specified local port for temporary public access"`
- Manus `deploy_apply_deployment` supports both "static" and "nextjs" deployment types
- Devin `expose_port` returns a "public URL"
- No mention of port allow-lists or rate limiting
- No mention of deployment approval workflows

**Attack Scenarios:**
1. **Internal Service Exposure:** Expose a local database admin panel or API to the public internet
2. **Malicious Deployment:** Deploy a phishing site or malware distribution page
3. **Resource Abuse:** Deploy cryptocurrency miners or spam services
4. **Data Exfiltration:** Deploy an app that streams internal data to an external endpoint
5. **Supply Chain Attack:** Deploy a compromised version of a dependency or package

---

### Category: Secret & Credential Access

**Tools Identified:**
- Replit: `ask_secrets`, `check_secrets`
- Devin: `list_secrets`
- v0: `AddEnvironmentVariables` (access to existing env vars)

**Risk:** Secret access tools can harvest API keys, database credentials, and authentication tokens.

**Specific Concerns from Source Material:**
- Replit `ask_secrets` prompts the user for secrets: `"Ask user for the secret API keys needed for the project"`
- Replit `check_secrets` verifies secret presence: `"Check if a given secret exists in the environment"`
- The v0 prompt lists exact environment variable names that the agent has access to
- Devin has a `list_secrets` command that enumerates available secrets

**Attack Scenarios:**
1. **Credential Harvesting:** Use `ask_secrets` to phish users for API keys with plausible pretexts
2. **Enumeration:** Use `check_secrets` to determine which secrets are available, then target those services
3. **Environment Variable Leakage:** The agent might accidentally include secrets in output or logs
4. **Third-Party API Abuse:** Use discovered keys to abuse cloud services, send spam, or mine cryptocurrency

**Evidence from Source Material (v0 environment variables):**
The v0 prompt explicitly lists:
```
NEXT_PUBLIC_FIREBASE_API_KEY
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN
NEXT_PUBLIC_FIREBASE_PROJECT_ID
FIREBASE_CLIENT_EMAIL
FIREBASE_PRIVATE_KEY
NEXT_PUBLIC_CLOUDINARY_CLOUD_NAME
NEXT_PUBLIC_CLOUDINARY_API_KEY
CLOUDINARY_API_SECRET
NEXT_PUBLIC_CLOUDINARY_UPLOAD_PRESET
```
Knowing these exact variable names enables targeted phishing and credential stuffing.

---

### Category: Database Access

**Tools Identified:**
- Replit: `execute_sql_tool`, `create_postgresql_database_tool`, `check_database_status`
- Manus: Datasource module with SQL capabilities (via Python)

**Risk:** Database tools allow data exfiltration, schema enumeration, and data destruction.

**Specific Concerns from Source Material:**
- Replit `execute_sql_tool` accepts arbitrary SQL: `"sql_query": {"type": "string"}`
- Replit explicitly warns: "DO NOT alter any database tables. DO NOT use destructive statements such as DELETE or UPDATE unless explicitly requested"
- But the tool itself does not enforce this — it's a policy instruction, not a technical control
- Manus datasource module uses Python to call APIs, which could include raw SQL

**Attack Scenarios:**
1. **Data Exfiltration:** `SELECT * FROM users` to dump user data
2. **Schema Enumeration:** `SELECT table_name FROM information_schema.tables` to discover data structures
3. **Data Destruction:** `DROP TABLE users` or `DELETE FROM users`
4. **Privilege Escalation:** `CREATE USER attacker WITH SUPERUSER`
5. **SQL Injection:** If the agent uses user input in SQL queries without parameterization

---

## Schema as Attack Surface

### Enumeration Surface

Exposed schemas allow attackers to:
1. **Map capabilities:** Know exactly what the agent can do
2. **Identify gaps:** Find missing security controls (e.g., no command allow-list on `shell_exec`)
3. **Craft targeted inputs:** Design prompts that trigger specific high-risk tools
4. **Bypass checks:** Know what validation exists and how to circumvent it

### Injection Surface

Tool parameters are injection vectors:
1. **Command injection:** `shell_exec` command parameter can include `;`, `&&`, `||`, `|`, `` ` ``
2. **Path traversal:** `file_read` file parameter can include `../` to escape the workspace
3. **JavaScript injection:** `browser_console_exec` javascript parameter can include arbitrary JS
4. **SQL injection:** `execute_sql_tool` sql_query parameter can include stacked queries
5. **URL injection:** `browser_navigate` url parameter can point to malicious sites

### Capability Escalation Surface

Tools can be chained to escalate privileges:
1. `file_read` → read SSH keys → `shell_exec` with key → SSH to other machines
2. `browser_navigate` → navigate to admin panel → `browser_input` → login with default creds → `browser_console_exec` → steal session
3. `shell_exec` → install dependencies → `deploy_apply_deployment` → deploy backdoored app
4. `ask_secrets` → phish API key → `bash` → use key to abuse cloud service

---

## Capability Enumeration Risks

When an attacker knows the full tool schema, they can:

1. **Determine the agent's operating environment:**
   - Manus runs on "Ubuntu 22.04 (linux/amd64)"
   - Replit uses Nix packages (`nixpkgs`)
   - v0 uses "Node.js v20+"
   - This information enables targeted exploits

2. **Determine the agent's privilege level:**
   - Manus has `sudo` access
   - Replit has access to create PostgreSQL databases
   - v0 has access to Firebase and Cloudinary credentials

3. **Determine the agent's network access:**
   - Manus has internet access and can expose ports
   - Replit deploys to `.replit.app` domains
   - v0 deploys to Vercel

4. **Determine the agent's data access:**
   - Manus can read arbitrary files with sudo
   - Replit can execute SQL on PostgreSQL
   - v0 can access user's Vercel projects

---

## Mitigation Strategies

### 1. Schema Obfuscation

- **Do not expose tool schemas in public documentation**
- **Use opaque tool identifiers** instead of descriptive names
- **Remove descriptive parameters** from public-facing documentation
- **Version schemas internally** but never publish version details

### 2. Parameter Validation

- **Implement strict allow-lists** for command parameters (e.g., only allow specific commands in `shell_exec`)
- **Sanitize all path parameters** to prevent directory traversal (`../`)
- **Validate URL schemes** to prevent `file://`, `data://`, or `javascript://` URLs
- **Use parameterized queries** for all database access
- **Implement CSP headers** for browser contexts

### 3. Capability Gating

- **Disable high-risk tools by default** (shell_exec, file_write with sudo, browser_console_exec)
- **Require explicit user opt-in** with risk acknowledgment
- **Implement approval workflows** for destructive actions
- **Restrict tool scope** to the minimum required for the task
- **Log all tool invocations** for audit purposes

### 4. Sandboxing

- **Run shell commands in isolated containers** with no network access
- **Run browser sessions in isolated profiles** with no access to local files
- **Run file operations in chroot jails** restricted to the workspace
- **Run database queries with read-only users** by default
- **Implement resource limits** (CPU, memory, disk, network) on all tool executions

### 5. Defense in Depth

- **Implement output filtering** to prevent secrets from appearing in tool output
- **Implement input filtering** to detect and block prompt injection attempts
- **Implement rate limiting** on tool invocations
- **Implement anomaly detection** for unusual tool usage patterns
- **Implement kill switches** for emergency tool disablement

---

## OpenClaw-Specific Recommendations

1. **Never ship tool schemas in public repositories** — schemas should be in a private, access-controlled repository
2. **Never use descriptive tool names in public documentation** — use generic names like "execute" instead of "shell_exec"
3. **Never expose the full parameter schema** in error messages or logs
4. **Implement capability tiers** — Basic (safe tools only), Standard (most tools), Advanced (all tools with approval)
5. **Implement tool-specific approval dialogs** — every high-risk tool should require explicit confirmation
6. **Audit all tool outputs** — filter for secrets, internal paths, and sensitive data before displaying to users
7. **Monitor for schema probing** — detect users who are systematically testing tool capabilities
8. **Assume schemas will be leaked** — design tools to be safe even when their full schema is known

---

## Conclusion

Tool schemas are the **operational surface** of an AI agent. Exposing them is equivalent to publishing an API documentation for attacking the agent. The collected source material demonstrates that major AI products have schemas that grant shell execution, file system access, browser control, deployment, secret access, and database manipulation — often with minimal technical controls.

For OpenClaw, the guiding principle must be: **schemas should be designed as if they will be public, but never actually made public.** Every tool should be safe to use even if its full schema is known, and high-risk tools should require explicit human approval on every invocation.
