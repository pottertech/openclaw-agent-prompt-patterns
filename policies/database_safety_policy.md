# Database Safety Policy

## Purpose
Define safe patterns for database access, including destructive action prevention and data integrity rules.

## Policy

### 1. Read-Only by Default
- Database queries default to read-only operations.
- Write operations require explicit user confirmation or are gated by approval.

### 2. Destructive Action Prevention
- Never execute `DELETE`, `UPDATE`, `DROP`, or `TRUNCATE` without explicit user approval.
- Migrations must be performed through ORM tools (e.g., Drizzle, Flask-Migrate), not raw SQL.
- Do not alter database tables unless explicitly requested.

### 3. Query Safety
- Use parameterized queries to prevent SQL injection.
- Validate inputs before using them in database queries.
- Prefer ORM abstractions over raw SQL for standard operations.

### 4. Connection Management
- Use connection pooling to manage database connections efficiently.
- Close connections after use to prevent resource leaks.
- Never expose database credentials in logs or error messages.

### 5. Data Integrity
- Ensure transactions are used for multi-step write operations.
- Rollback on error to maintain data consistency.
- Verify schema compatibility before running queries.

### 6. SQL Tool Usage
- Use dedicated SQL execution tools for database interactions instead of shell commands.
- Use the SQL tool for fixing database errors, exploring schemas, and running ad-hoc queries.
- Do not use the SQL tool for migrations; use ORM migration tools instead.

## Risk Assessment
- **Critical Risk**: Unauthorized destructive actions can cause irreversible data loss.
- **High Risk**: SQL injection can compromise the entire database.
- **Mitigation**: Read-only defaults, approval gates, parameterized queries, and ORM usage.

## References
- OpenClaw database tool guidelines
- SQL safety best practices
