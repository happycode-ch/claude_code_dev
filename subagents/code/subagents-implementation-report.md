# Complete Guide to Building Sub-Agents with Claude Code
## Following Anthropic's Best Practices for Agentic Development

---

## Executive Summary

Sub-agents in Claude Code are specialized AI assistants that handle specific tasks with their own context windows, tools, and system prompts. This report provides comprehensive guidance for building robust sub-agents following Anthropic's documented best practices, with emphasis on strong guardrails, clearly defined objectives, and proper orchestration patterns.

**Key Documentation URLs:**
- Main Sub-agents Documentation: https://docs.anthropic.com/en/docs/claude-code/sub-agents
- Claude Code Best Practices: https://www.anthropic.com/engineering/claude-code-best-practices
- Building Effective Agents: https://www.anthropic.com/research/building-effective-agents
- Multi-Agent Research System: https://www.anthropic.com/engineering/multi-agent-research-system
- Agent Framework: https://www.anthropic.com/news/our-framework-for-developing-safe-and-trustworthy-agents
- Claude Code Settings: https://docs.anthropic.com/en/docs/claude-code/settings
- Claude Code Overview: https://docs.anthropic.com/en/docs/claude-code/overview
- MCP Documentation: https://docs.anthropic.com/en/docs/mcp
- GitHub Repository: https://github.com/anthropics/claude-code
- Example Sub-agents Collection: https://github.com/wshobson/agents

---

## Part 1: Core Architecture & Concepts

### 1.1 What Are Sub-Agents?

According to Anthropic's documentation, sub-agents are:
- **Specialized AI personalities** that Claude Code can delegate tasks to
- **Independent context windows** preventing pollution of main conversation
- **Task-specific configurations** with customized system prompts and tools
- **Domain-focused experts** with higher success rates on designated tasks

### 1.2 Key Benefits (Per Anthropic Documentation)

1. **Context Efficiency**: Preserve main context for longer sessions
2. **Specialization**: Task-specific prompts and limited tools improve focus
3. **Scalability**: Transform single assistant into team of experts
4. **Modularity**: Reusable components across projects

### 1.3 File Structure and Locations

Sub-agents are stored as Markdown files with YAML frontmatter:
- **User-level**: `~/.claude/agents/` (available across all projects)
- **Project-level**: `.claude/agents/` (specific to project, takes precedence)

---

## Part 2: YAML Configuration Specification

### 2.1 Complete YAML Structure

```yaml
---
name: your-sub-agent-name
description: Description of when this subagent should be invoked
model: sonnet  # Optional: haiku, sonnet, opus (defaults to system model)
tools: tool1, tool2, tool3  # Optional: inherits all tools if omitted
---

Your subagent's system prompt goes here.
This should clearly define:
- The subagent's role
- Capabilities and constraints
- Approach to solving problems
- Specific instructions
- Best practices to follow
```

### 2.2 Model Selection Strategy (Per Anthropic Guidelines)

**Haiku 3.5** (`model: haiku`):
- Simple file operations
- Basic formatting tasks
- Documentation generation
- Quick data extraction
- Cost: $0.80/$4 per million tokens

**Sonnet 4** (`model: sonnet`):
- Standard development tasks
- Code review and testing
- Multi-file changes
- Complex refactoring
- Cost: $3/$15 per million tokens

**Opus 4** (`model: opus`):
- Architecture design
- Security auditing
- Incident response
- Complex reasoning
- Cost: $15/$75 per million tokens

### 2.3 Tool Access Configuration

Available tools (from Anthropic documentation):
- `bash`: Execute shell commands
- `read`: Read files
- `write`: Write/modify files
- `search`: Search codebase
- `test`: Run tests
- `git`: Version control operations
- MCP server tools (if configured)

---

## Part 3: Orchestration Patterns (Anthropic's Framework)

### 3.1 Prompt Chaining Pattern
Sequential task decomposition where each step builds on previous:
```markdown
Step 1: Analyze requirements → 
Step 2: Design solution → 
Step 3: Implement → 
Step 4: Test
```

### 3.2 Parallelization Pattern
Multiple agents work simultaneously:
- **Sectioning**: Different agents handle different aspects
- **Voting**: Multiple agents verify same output

### 3.3 Orchestrator-Worker Pattern
Central orchestrator dynamically assigns tasks:
```markdown
LeadAgent → [SubAgent1, SubAgent2, SubAgent3] → Synthesis
```

### 3.4 Evaluator-Optimizer Pattern
Continuous improvement loop with evaluation feedback

---

## Part 4: Building Production-Ready Sub-Agents

### 4.1 Essential Sub-Agent Template

```markdown
---
name: code-reviewer
description: Use PROACTIVELY for code review, best practices verification
model: sonnet
tools: read, search, bash
---

You are an expert code reviewer specializing in security and best practices.

## Core Responsibilities
1. Analyze code for security vulnerabilities
2. Verify adherence to coding standards
3. Check for performance issues
4. Ensure proper error handling

## Guardrails and Constraints
- NEVER modify code directly (read-only operations)
- ALWAYS provide specific line references
- MUST check for OWASP Top 10 vulnerabilities
- REQUIRE evidence for all findings

## Workflow
1. Read the target files systematically
2. Search for anti-patterns using grep/ast tools
3. Document findings with severity levels
4. Provide actionable recommendations

## Output Format
Provide findings as:
- **Critical**: Security vulnerabilities
- **High**: Logic errors, data corruption risks
- **Medium**: Performance issues, maintainability
- **Low**: Style violations, minor improvements

Include specific file:line references for each finding.
```

### 4.2 Test-Driven Development Agent

```markdown
---
name: test-automator
description: Use for writing and maintaining test suites following TDD
model: sonnet
tools: read, write, bash
---

You are a test automation expert practicing strict TDD methodology.

## Strict TDD Rules (Per Anthropic Best Practices)
1. Write failing tests FIRST
2. Do NOT create mock implementations
3. Run tests to confirm they fail
4. Only then write implementation code
5. Iterate until all tests pass

## Test Coverage Requirements
- Unit tests: Minimum 80% code coverage
- Integration tests: Critical paths
- Edge cases: Null, empty, boundary conditions
- Error scenarios: Exception handling

## Workflow
1. Analyze requirements
2. Write comprehensive test cases
3. Run tests (expect failures)
4. Implement minimal code to pass
5. Refactor while maintaining green tests
```

---

## Part 5: Guardrails and Safety Mechanisms

### 5.1 Permission Controls (From Anthropic Documentation)

```json
{
  "permissions": {
    "deny": [
      "Write(./.env)",
      "Write(./secrets/*)",
      "Bash(rm -rf)",
      "Bash(sudo)"
    ],
    "allow": [
      "Read(./**/*.py)",
      "Write(./src/**/*.py)",
      "Bash(pytest)"
    ]
  }
}
```

### 5.2 Error Handling Patterns

```markdown
## Error Handling Requirements
- ALWAYS wrap operations in try-catch blocks
- MUST log all errors with context
- NEVER swallow exceptions silently
- REQUIRE rollback mechanisms for failed operations
- IMPLEMENT retry logic with exponential backoff
```

### 5.3 Security Guardrails

Per Anthropic's security framework:
1. **Input Validation**: Sanitize all inputs
2. **Output Filtering**: Check for sensitive data
3. **Rate Limiting**: Prevent resource exhaustion
4. **Audit Logging**: Track all operations
5. **Sandboxing**: Isolate risky operations

---

## Part 6: Advanced Implementation Patterns

### 6.1 Multi-Agent Research System (From Anthropic's Implementation)

```markdown
---
name: lead-researcher
description: Orchestrates research tasks across multiple sources
model: opus
tools: search, read, write
---

You are a lead research agent coordinating information gathering.

## Research Process
1. Save research plan to memory (persist beyond context limit)
2. Create specialized sub-agents for parallel research
3. Synthesize findings from all sub-agents
4. Iterate if more information needed
5. Pass to CitationAgent for proper attribution

## Context Management
- If approaching 200k token limit, summarize and store
- Maintain research plan in external memory
- Use lightweight references between agents
```

### 6.2 Data Analysis Agent with MCP

```markdown
---
name: data-scientist
description: SQL and BigQuery analysis specialist
model: sonnet
tools: bash, read, write
---

You are a data scientist specializing in SQL analysis.

## Capabilities (Using MCP Servers)
- Connect to databases via MCP
- Write optimized SQL queries
- Use BigQuery CLI (bq) tools
- Generate visualizations
- Provide statistical analysis

## Best Practices
- Write cost-effective queries
- Include query explanations
- Document assumptions
- Format results for readability
- Provide data-driven recommendations
```

---

## Part 7: Creating and Managing Sub-Agents

### 7.1 Interactive Creation (Recommended by Anthropic)

```bash
# Use the /agents command for interactive creation
claude
> /agents

# This provides:
# - Interactive interface
# - Lists all available tools
# - Includes MCP server tools
# - Validates configuration
```

### 7.2 Manual Creation

```bash
# Create project-level agent
mkdir -p .claude/agents
cat > .claude/agents/security-auditor.md << 'EOF'
---
name: security-auditor
description: Security analysis and vulnerability detection
model: opus
tools: read, search, bash
---

[System prompt here]
EOF
```

### 7.3 Invoking Sub-Agents

```bash
# Explicit invocation
> Use the security-auditor to check for vulnerabilities

# Proactive trigger (with proper description)
> Check this code for issues  # Triggers if description matches
```

---

## Part 8: Best Practices from Anthropic

### 8.1 Design Principles

1. **Simplicity First**: Start simple, add complexity only when needed
2. **Transparency**: Show agent's planning and reasoning
3. **Tool Design**: Craft clear, well-documented tool interfaces
4. **Context Preservation**: Use memory and external storage

### 8.2 Effective Prompting for Sub-Agents

From Anthropic's guidelines:
- Use action-oriented descriptions
- Include "PROACTIVELY" for automatic triggering
- Be specific about when to invoke
- Define clear boundaries between agents

### 8.3 Cost Optimization

```markdown
## Cost Management Strategy
1. Use Haiku for simple tasks (20x cheaper than Opus)
2. Reserve Opus for critical decisions
3. Implement hybrid workflows:
   - Opus: Planning phase
   - Sonnet: Implementation
   - Haiku: Formatting/cleanup
4. Set --max-turns limits
5. Use prompt caching (90% cost reduction)
```

---

## Part 9: Testing and Validation

### 9.1 Sub-Agent Testing Framework

```bash
# Test individual sub-agent
claude --model sonnet
> Test the code-reviewer agent with sample code

# Validate agent configuration
> /agents validate code-reviewer

# Benchmark performance
> Run the test-automator on /src and measure token usage
```

### 9.2 Evaluation Criteria (From Anthropic)

1. **Task Completion**: Does it achieve objectives?
2. **Token Efficiency**: Optimal model selection?
3. **Error Rate**: Frequency of failures?
4. **Context Usage**: Efficient memory management?
5. **Safety Compliance**: Follows guardrails?

---

## Part 10: Implementation Checklist

### For Each Sub-Agent:

- [ ] **Define Clear Role**: Single responsibility principle
- [ ] **Select Appropriate Model**: Match complexity to capability
- [ ] **Limit Tool Access**: Minimum necessary permissions
- [ ] **Include Guardrails**: Error handling, safety checks
- [ ] **Document Workflow**: Step-by-step process
- [ ] **Specify Output Format**: Structured, parseable results
- [ ] **Add Validation**: Input/output checks
- [ ] **Test Thoroughly**: Edge cases, error scenarios
- [ ] **Monitor Performance**: Token usage, success rate
- [ ] **Version Control**: Track changes in Git

### System-Level:

- [ ] **CLAUDE.md File**: Project-specific instructions
- [ ] **Permission Settings**: .claude/settings.json
- [ ] **MCP Servers**: Configure if needed
- [ ] **CI/CD Integration**: Automated testing
- [ ] **Monitoring**: Logging and analytics
- [ ] **Documentation**: Team knowledge sharing

---

## Part 11: Common Patterns and Examples

### 11.1 Frontend Development Agent

```markdown
---
name: frontend-developer
description: React component development and UI implementation
model: sonnet
tools: read, write, bash, search
---

Expert React developer following modern best practices.

## Technologies
- React 18+ with hooks
- TypeScript
- Tailwind CSS (core utilities only)
- Component testing with Jest/RTL

## Standards
- Functional components only
- Custom hooks for logic extraction
- Accessibility (WCAG 2.1 AA)
- Responsive design (mobile-first)
```

### 11.2 DevOps Troubleshooter

```markdown
---
name: devops-troubleshooter
description: Production issue diagnosis and resolution
model: opus
tools: bash, read, search
---

Senior DevOps engineer specializing in incident response.

## Diagnostic Process
1. Gather symptoms and error messages
2. Check logs systematically
3. Analyze metrics and monitoring
4. Identify root cause
5. Propose remediation steps
6. Document post-mortem findings
```

---

## Part 12: Future Considerations

### Upcoming Features (Per Anthropic Roadmap)

1. **Parallel Execution**: Sub-agents working simultaneously
2. **Durable Execution**: Pause/resume with state persistence
3. **Enhanced MCP Integration**: More server types
4. **Multi-Model Orchestration**: Dynamic model switching
5. **Advanced Memory Systems**: Long-term context retention

### Preparation Recommendations

1. Design agents to be stateless where possible
2. Use external storage for persistence
3. Build modular, composable agents
4. Implement comprehensive logging
5. Plan for migration paths

---

## Conclusion

Building effective sub-agents requires careful planning, clear objectives, and adherence to Anthropic's best practices. Key principles:

1. **Start Simple**: Begin with basic agents, add complexity gradually
2. **Focus on Specialization**: Each agent should excel at one thing
3. **Implement Guardrails**: Safety and reliability are paramount
4. **Optimize Costs**: Use appropriate models for each task
5. **Test Thoroughly**: Validate behavior before production
6. **Document Everything**: Enable team collaboration

This framework provides the foundation for building robust, scalable sub-agent systems that leverage Claude Code's full potential while maintaining safety and efficiency.

---

## Additional Resources

- Anthropic Cookbook (Agent Patterns): https://github.com/anthropics/anthropic-cookbook/tree/main/patterns/agents
- MCP Servers Directory: https://github.com/modelcontextprotocol/servers
- Claude Code Issues/Discussions: https://github.com/anthropics/claude-code/issues
- Community Sub-agents: https://github.com/wshobson/agents
- MCP Agent Framework: https://github.com/lastmile-ai/mcp-agent

---

*This report is designed for recursive feeding to Claude and Claude Code for developing production-ready sub-agents following Anthropic's documented best practices and architectural patterns.*