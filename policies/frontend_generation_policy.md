# Frontend Generation Policy

## Purpose
Define patterns for generating frontend code, including build patterns, component rules, and styling guidelines.

## Policy

### 1. Framework Defaults
- Default to modern frameworks (e.g., Next.js App Router) unless specified otherwise.
- Prioritize Server Components for React/Next.js when possible.
- Use the latest stable versions of frameworks and libraries.

### 2. Component Rules
- Create small, focused components (aim for 50 lines or less).
- Create a new file for every new component or hook.
- Never add new components to existing files, even if they seem related.
- Use kebab-case for file names (e.g., `login-form.tsx`).

### 3. Styling
- Use Tailwind CSS for styling unless the user specifies otherwise.
- Avoid hardcoding colors; use CSS variables or Tailwind's built-in color system.
- Generate responsive designs by default.
- Implement accessibility best practices (semantic HTML, ARIA roles, alt text).

### 4. Asset Handling
- Use placeholder images via standard placeholder services.
- Use icon libraries (e.g., Lucide React) instead of inline SVGs.
- Set `crossOrigin="anonymous"` for images rendered on `<canvas>`.

### 5. Code Quality
- Use `import type` for type imports to avoid runtime imports.
- Provide default props for React components.
- Use ES6+ syntax; avoid `require` in favor of `import`.

### 6. Build and Deploy
- Do not output framework config files (e.g., `next.config.js`) unless explicitly needed.
- Listen on `0.0.0.0` for accessible port bindings, not `localhost`.
- Test locally before deploying.

## Risk Assessment
- **Medium Risk**: Incorrect framework defaults can cause compatibility issues.
- **Low Risk**: Accessibility oversights can impact user experience.
- **Mitigation**: Follow framework conventions, use component libraries, and test responsiveness.

## References
- OpenClaw frontend generation guidelines
- Next.js and React best practices
