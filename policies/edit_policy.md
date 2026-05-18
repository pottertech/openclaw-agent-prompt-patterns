# Edit Policy

## Purpose
Define rules for file editing operations, including batching, atomicity, and safe modification practices.

## Policy

### 1. Read Before Writing
- Always read the current contents of a file before modifying it.
- For large files, read specific line ranges to avoid context overflow.
- Understand the file's structure and conventions before making changes.

### 2. Exact Text Matching
- Edits must match the exact text in the file, including whitespace and indentation.
- Use unique, non-overlapping regions for replacements.
- If two changes affect the same block, merge them into a single edit.

### 3. Atomicity
- File writes are atomic — the entire file is replaced.
- For partial edits, use exact replacement to ensure consistency.
- Never leave files in a partially edited state.

### 4. Batching Rules
- Batch multiple edits to the **same file** into a single operation.
- Do not batch edits to **different files** in the same operation if the tool does not support it.
- Prefer surgical edits (replacing specific lines) over full-file rewrites when possible.

### 5. Creation and Deletion
- When creating new files, provide the complete intended content.
- When deleting files, verify the file is not referenced elsewhere.
- Use `trash` over `rm` for recoverable deletion.

### 6. Verification
- After editing, verify the file was modified correctly.
- Check for syntax errors if the file is code.
- Re-read the modified section if unsure about the result.

## Risk Assessment
- **High Risk**: Overlapping edits can corrupt files.
- **Medium Risk**: Full-file rewrites can accidentally remove content.
- **Mitigation**: Use exact matching, batch intelligently, and verify after each edit.

## References
- OpenClaw `edit` tool documentation
- File system safety guidelines
