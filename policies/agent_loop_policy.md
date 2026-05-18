# Agent Loop Policy

## Purpose
Define the behavior of the agent's execution loop, including terminal states, retry limits, and how the agent progresses through tasks using the Karpathy Loop.

## Policy

### 1. Loop Structure (The Karpathy Loop)
The agent operates in an iterative loop with these phases:
1. **Observe**: Ingest the latest user message, tool results, and state changes.
2. **Orient**: Understand the current state relative to the task goal.
3. **Decide**: Select the next action (tool call, response, or termination).
4. **Act**: Execute the chosen action.
5. **Repeat** until the task is complete or a terminal state is reached.

### 2. One Tool Per Iteration
- Only **one tool call** per reasoning cycle.
- The agent must wait for the tool's result before proceeding to the next iteration.
- Patience is required; the loop continues until completion.

### 3. Terminal States
The loop may terminate in one of the following states:
- **Success**: The task is completed and results are delivered.
- **Idle/Standby**: The agent enters a waiting state for new tasks.
- **Error**: A critical failure occurs that prevents continuation.
- **User Stop**: The user explicitly requests termination.

### 4. Retry and Error Handling
- On tool failure, first verify the tool name and arguments.
- Attempt to fix issues based on the error message.
- If multiple approaches fail, report failure reasons and ask for user assistance.
- Retry limits apply to prevent infinite loops:
  - **Tool errors**: Up to 3 retries with modified arguments.
  - **Plan deviations**: Up to 2 replanning attempts before escalating.

### 5. Progress Tracking
- Maintain an internal understanding of the current step number and status.
- Update markers immediately after completing each item.
- Rebuild the plan when the overall task objective changes significantly.

### 6. State Transitions
- The agent transitions between states based on events:
  - `active` → `waiting_for_tool`: After dispatching a tool call.
  - `waiting_for_tool` → `active`: Upon receiving tool results.
  - `active` → `idle`: When all tasks are completed.
  - `active` → `error`: On critical failure.

## Risk Assessment
- **Medium Risk**: Incorrect loop state transitions can lead to stale decisions.
- **Low Risk**: Retry limits prevent runaway loops but may cause premature failure.
- **Mitigation**: Always verify tool results before deciding the next action.

## References
- OpenClaw "Karpathy Loop" concept
- Event-driven agent architecture
