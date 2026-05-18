# Verification Policy

## Purpose
Define rules for testing, linting, and validating code and actions before completion.

## Policy

### 1. Testing
- Run tests before marking a task as complete.
- Never modify test code unless explicitly asked.
- If tests fail, investigate the code under test before suspecting the tests.
- Use the test commands provided in the project (e.g., `npm test`, `pytest`).

### 2. Linting
- Run linters before submitting code changes.
- Fix linter errors if the fix is clear and straightforward.
- Do not make uneducated guesses to fix linter errors.
- If linter errors persist after 3 attempts, stop and ask the user.

### 3. Validation
- Verify that code compiles or runs without errors.
- Check that the output matches the expected behavior.
- For web apps, test locally before deploying.

### 4. Review
- Before completing a task, review all changes made.
- Ensure all relevant files were updated.
- Verify no unintended side effects were introduced.

### 5. CI/CD
- If CI checks exist, ensure they pass before considering the task complete.
- If CI fails, investigate and fix the root cause.
- Ask for user help if CI does not pass after the third attempt.

## Risk Assessment
- **Medium Risk**: Skipping verification can lead to broken code in production.
- **Low Risk**: Over-reliance on automated checks may miss logical errors.
- **Mitigation**: Run tests, lint, and manually verify critical paths.

## References
- OpenClaw verification guidelines
- Software testing best practices
