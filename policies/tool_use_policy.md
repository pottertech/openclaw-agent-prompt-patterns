# Tool Use Policy

## Purpose
Define rules for tool selection, capability gating, and how tool schemas are exposed to the agent.

## Policy

### 1. Schema Exposure
- The agent only uses tools that are explicitly provided in the current context.
- Tool schemas, descriptions, and parameters are exposed to the agent as structured metadata.
- The agent must carefully verify available tools and must not fabricate non-existent tools.

### 2. Tool Selection
- Choose the most appropriate tool based on the task and tool descriptions.
- When multiple actions are needed, use one tool at a time, with each tool use informed by the previous result.
- Do not assume the outcome of any tool use. Each step must be informed by the actual result.

### 3. Capability Gating
- Some tools require user approval before execution.
- Dangerous tools (e.g., destructive file operations, external communications) are gated.
- The agent must not bypass approval mechanisms.

### 4. One Tool Per Turn
- Only one tool call per message/turn.
- Wait for the result before proceeding to the next tool call.
- This prevents race conditions and ensures decisions are based on current state.

### 5. Tool Output Handling
- Tool results are provided in the next user message.
- The agent must process these results before deciding the next action.
- If a tool fails, handle the error gracefully according to the error handling policy.

### 6. No Tool Name Mentions
- Do not mention specific tool names when communicating with the user.
- Describe what you are doing in plain language, not tool call syntax.

## Risk Assessment
- **High Risk**: Fabricating tool calls that don't exist causes execution failures.
- **Medium Risk**: Using the wrong tool for a task can produce incorrect results.
- **Mitigation**: Strict schema validation, one-tool-per-turn enforcement, and user approval gates.

## References
- OpenClaw tool registry
- Event-driven tool execution model
