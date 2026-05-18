# Secret Handling Policy

## Purpose
Define how secrets, credentials, and sensitive data are managed and protected.

## Policy

### 1. Secret Isolation
- Secrets must never be hardcoded in source code.
- Use environment variables or secret management tools for all credentials.
- Keep secrets out of logs, error messages, and user-facing output.

### 2. Credential Access
- The agent can access secrets provided by the user through secure channels.
- Use the `list_secrets` tool to discover available secrets.
- Never reveal secrets in tool arguments that might be logged.

### 3. Communication Security
- Never share sensitive data with third parties.
- Obtain explicit user permission before external communications.
- Use secure channels for any credential exchange.

### 4. Storage
- Do not commit secrets to version control.
- Use `.env` files or secret management services for local development.
- Rotate secrets regularly and avoid reuse across environments.

### 5. Exposure Prevention
- If a secret is accidentally exposed, immediately notify the user.
- Redact secrets from any output, including debug logs.
- Treat code and customer data as sensitive information.

## Risk Assessment
- **Critical Risk**: Secret exposure can lead to unauthorized access and data breaches.
- **High Risk**: Accidental logging of secrets in tool calls or errors.
- **Mitigation**: Environment variables, secret management tools, and output redaction.

## References
- OpenClaw secret management guidelines
- Security best practices
