# Coding Agent Policy

## Purpose
Define patterns for code editing, reading, and writing that minimize errors and preserve code quality.

## Policy

### 1. Read Before Edit
- **Always read a file before editing it.** Never modify code without understanding its full context.
- When reading large files, prefer reading specific line ranges over loading the entire file into context.
- Use semantic search to find relevant code sections when the exact location is unknown.

### 2. Minimal Changes
- Complete tasks with the **minimal code changes** necessary.
- Focus on maintainability and readability.
- Preserve existing code style, conventions, and patterns.

### 3. Context Awareness
- Before making changes, examine surrounding context, especially imports, to understand framework choices.
- When creating new components, first look at existing components to understand naming conventions and typing.
- Never assume a library is available; verify it exists in the project before using it.

### 4. Batch Edits
- When multiple changes are needed in the **same file**, batch them into a single edit operation.
- Group edits that affect the same block or nearby lines.
- Use atomic replacement for file edits to prevent partial updates.

### 5. Code Quality
- Do not add comments that simply restate what the code does.
- Only add comments when the code is complex and requires additional context.
- Follow the project's existing linting and formatting rules.
- Fix linter errors if clear how to, but do not make uneducated guesses.

### 6. Testing
- When provided with test commands, run them before submitting changes.
- Never modify test code unless explicitly asked.
- If tests fail, assume the issue is in the code under test before suspecting the tests.

### 7. No Shell for File Operations
- Use file editing tools for creating, viewing, and editing files.
- Never use shell commands (`cat`, `sed`, `echo`, `vim`) for file manipulation.

## Risk Assessment
- **High Risk**: Editing files without reading them first can corrupt code.
- **Medium Risk**: Batching too many changes increases the chance of syntax errors.
- **Mitigation**: Read files in chunks, use exact text matching for replacements, and verify results.

## References
- OpenClaw `edit` tool guidelines
- LSP (Language Server Protocol) integration for diagnostics
