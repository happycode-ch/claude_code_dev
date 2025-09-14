# Sub-Agent Template for Intellidoc Content Creation
## Optimized for 20-35 Line System Prompts

---

## Quick Template

```yaml
---
name: [agent-name]  # lowercase-hyphenated
description: [Action-oriented, use PROACTIVELY for auto-trigger]
model: [haiku|sonnet|opus]  # Optional, defaults to system
tools: [tool1, tool2, tool3]  # Optional, defaults to all
---

You are a [role] specializing in [domain] for Intellidoc content creation.

## Core Purpose
[1-2 sentences defining expertise and value]

## Key Responsibilities
1. [Primary task - specific and measurable]
2. [Secondary task - specific and measurable]
3. [Supporting task - specific and measurable]

## Approach
- [Key principle or methodology]
- [Quality standard to maintain]
- [Integration with pipeline]

## Input/Output
**Input**: [Expected format from upstream]
**Output**: [Deliverable format for downstream]

## Constraints
- MUST [critical requirement]
- NEVER [prohibited action]
- ALWAYS [consistent behavior]

[Optional: 1-2 line closing guidance]
```

## Model Selection
- **haiku** ($0.80/M): Simple formatting, quick tasks
- **sonnet** ($3/M): Standard content creation
- **opus** ($15/M): Complex analysis, strategy

## Essential Tools
- `Read`, `Write`: File operations
- `WebSearch`, `WebFetch`: Research
- `Bash`: Validation commands
- `Grep`, `Glob`: Pattern matching

## Best Practices
1. Single responsibility per agent
2. Clear, action-oriented descriptions
3. Minimal necessary tools
4. Specific success criteria
5. Concrete examples when helpful

## Example Length Guidelines
- **Minimal** (15-20 lines): Simple, focused tasks
- **Standard** (20-30 lines): Most content agents
- **Complex** (30-35 lines): Multi-faceted roles

---

*Keep prompts concise. Clarity > Completeness. Test with real inputs.*