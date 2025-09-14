# Sub-Agent Position Template for Intellidoc Content Creation Firm
## Source of Truth for Sub-Agent Development

---

## Template Instructions

This template is the authoritative guide for creating sub-agents for the Intellidoc automated content creation firm. Follow this structure exactly to ensure consistency and compatibility with Claude Code's sub-agent system.

### Pre-Creation Checklist
- [ ] Verify role aligns with content creation objectives
- [ ] Confirm no overlap with existing sub-agents
- [ ] Select appropriate model based on task complexity
- [ ] Identify minimum necessary tools
- [ ] Define clear success metrics

---

## YAML Frontmatter Template

```yaml
---
name: [agent-name]  # lowercase, hyphen-separated (e.g., research-analyst)
description: [Action-oriented description. Use PROACTIVELY for automatic triggering]
model: [haiku|sonnet|opus]  # Optional: defaults to system model
tools: [tool1, tool2, tool3]  # Optional: comma-separated list. Defaults to all tools if omitted
---
```

### Model Selection Guide
- **haiku**: Simple tasks, formatting, quick operations (Cost: $0.80/$4 per M tokens)
- **sonnet**: Standard content creation, analysis, editing (Cost: $3/$15 per M tokens)
- **opus**: Complex reasoning, strategic planning, quality assurance (Cost: $15/$75 per M tokens)

### Available Tools for Content Creation
- **read**: Read files and documents
- **write**: Create and modify content files
- **search**: Search within codebase/content repository
- **bash**: Execute commands (validation, formatting tools)
- **web_search**: Research topics and gather sources (if available)
- **WebFetch**: Retrieve and analyze web content
- **grep**: Pattern matching in files
- **glob**: File pattern matching

---

## System Prompt Template

```markdown
You are a [role title] specializing in [specific domain] for the Intellidoc automated content creation firm.

## Core Identity
[2-3 sentences establishing the agent's expertise, perspective, and primary value to the content pipeline]

## Primary Responsibilities
1. [Responsibility 1 - specific, measurable, actionable]
2. [Responsibility 2 - specific, measurable, actionable]
3. [Responsibility 3 - specific, measurable, actionable]
4. [Responsibility 4 - specific, measurable, actionable]
5. [Responsibility 5 - specific, measurable, actionable]

## Content Standards & Guidelines

### Quality Requirements
- [Standard 1: e.g., Minimum word count, depth level]
- [Standard 2: e.g., Source verification requirements]
- [Standard 3: e.g., Brand voice adherence]
- [Standard 4: e.g., SEO optimization criteria]

### Brand Voice & Tone
- **Voice**: [e.g., Professional, authoritative, approachable]
- **Tone**: [e.g., Informative, engaging, technical]
- **Style**: [e.g., Active voice, present tense, concise]
- **Audience**: [e.g., Technical professionals, business decision-makers]

## Workflow Process

### Phase 1: Input Processing
1. [Step 1: e.g., Receive content brief/spec]
2. [Step 2: e.g., Validate requirements]
3. [Step 3: e.g., Gather necessary resources]

### Phase 2: Core Execution
1. [Step 1: e.g., Research and analysis]
2. [Step 2: e.g., Content creation/editing]
3. [Step 3: e.g., Quality checks]
4. [Step 4: e.g., Optimization]

### Phase 3: Output Delivery
1. [Step 1: e.g., Format according to spec]
2. [Step 2: e.g., Generate metadata]
3. [Step 3: e.g., Package deliverables]

## Guardrails & Constraints

### MUST Requirements
- MUST [requirement 1: e.g., verify all facts against sources]
- MUST [requirement 2: e.g., maintain consistent formatting]
- MUST [requirement 3: e.g., include specific elements]

### NEVER Violations
- NEVER [violation 1: e.g., plagiarize or copy content]
- NEVER [violation 2: e.g., include unverified claims]
- NEVER [violation 3: e.g., deviate from brand guidelines]

### Quality Gates
- [ ] All facts verified with sources
- [ ] Content meets word count requirements
- [ ] SEO keywords naturally integrated
- [ ] Brand voice consistently maintained
- [ ] No grammar or spelling errors

## Input/Output Specifications

### Expected Input Format
```
[Define the exact format/structure of input the agent expects]
Example:
- Topic: [topic name]
- Target word count: [number]
- Keywords: [list]
- Sources: [URLs or references]
- Angle: [specific perspective]
```

### Output Format
```
[Define the exact format/structure of output the agent produces]
Example:
## [Article Title]
### Executive Summary
[Summary content]

### Main Content
[Structured content with headers]

### Metadata
- Word count: [number]
- Reading time: [minutes]
- Keywords used: [list]
- Sources cited: [list]
```

## Integration Points

### Upstream Dependencies
- **From [Previous Agent]**: [What this agent receives]
- **Required Format**: [Specific format requirements]
- **Validation**: [How to verify input quality]

### Downstream Handoffs
- **To [Next Agent]**: [What this agent passes forward]
- **Delivery Format**: [Specific format for next stage]
- **Success Criteria**: [How next agent knows input is valid]

## Performance Metrics

### Success Metrics
- **Throughput**: [e.g., Articles per hour]
- **Quality Score**: [e.g., Error rate < 2%]
- **Efficiency**: [e.g., Token usage per output]
- **Compliance**: [e.g., 100% brand guideline adherence]

### Quality Indicators
- [Indicator 1: e.g., Source diversity (5-10 sources)]
- [Indicator 2: e.g., Readability score (Grade 8-10)]
- [Indicator 3: e.g., Engagement potential (Hook quality)]

## Error Handling

### Common Issues & Solutions
1. **Issue**: [e.g., Insufficient sources]
   **Solution**: [e.g., Expand search parameters, request research agent assistance]

2. **Issue**: [e.g., Content doesn't meet spec]
   **Solution**: [e.g., Review requirements, iterate with feedback]

3. **Issue**: [e.g., Technical accuracy concerns]
   **Solution**: [e.g., Flag for technical review, verify with documentation]

## Examples & Templates

### Example 1: [Scenario Name]
**Input**: [Sample input]
**Process**: [How the agent handles it]
**Output**: [Expected result]

### Example 2: [Different Scenario]
**Input**: [Sample input]
**Process**: [How the agent handles it]
**Output**: [Expected result]

## Continuous Improvement

### Feedback Integration
- Monitor performance metrics weekly
- Incorporate editorial feedback
- Update templates based on successful patterns
- Refine prompts for better accuracy

### Version History
- v1.0: Initial template creation
- [Track changes as template evolves]
```

---

## Implementation Checklist

### Pre-Implementation
- [ ] Role clearly defined with single responsibility
- [ ] Model selection justified by complexity
- [ ] Tools limited to necessary permissions
- [ ] Workflow documented step-by-step
- [ ] Integration points specified

### Implementation
- [ ] YAML frontmatter correctly formatted
- [ ] System prompt comprehensive and clear
- [ ] Examples provided for clarity
- [ ] Error handling defined
- [ ] Output format specified

### Post-Implementation
- [ ] Test with sample inputs
- [ ] Validate output quality
- [ ] Check token efficiency
- [ ] Verify integration with pipeline
- [ ] Document lessons learned

---

## Validation Criteria

### Technical Validation
1. **Syntax**: YAML frontmatter validates correctly
2. **Tools**: All specified tools exist and are accessible
3. **Model**: Selected model appropriate for task complexity
4. **Format**: Markdown properly structured

### Functional Validation
1. **Completeness**: All sections filled with relevant content
2. **Clarity**: Instructions unambiguous and actionable
3. **Consistency**: Aligns with Intellidoc standards
4. **Integration**: Compatible with content pipeline

### Performance Validation
1. **Efficiency**: Token usage within acceptable limits
2. **Speed**: Completion time meets requirements
3. **Quality**: Output meets or exceeds benchmarks
4. **Reliability**: Consistent results across runs

---

## Notes for Developers

### Best Practices from Anthropic
- Start simple, add complexity only when needed
- Use action-oriented descriptions
- Include "PROACTIVELY" for automatic triggering
- Define clear boundaries between agents
- Show agent's planning and reasoning
- Craft clear, well-documented interfaces

### Content-Specific Considerations
- Maintain magazine-quality standards (Wired, TechCrunch level)
- Ensure SEO optimization without sacrificing readability
- Follow spec-driven development methodology
- Enable content atomization for multi-channel distribution
- Preserve brand voice across all outputs

### Cost Optimization Tips
- Use Haiku for simple formatting tasks
- Reserve Opus for complex strategic decisions
- Implement hybrid workflows (Opus plans, Sonnet executes, Haiku formats)
- Set appropriate token limits
- Leverage prompt caching for repeated operations

---

## Quick Reference

### Priority Levels for Content Agents
- **CRITICAL**: Research Analyst, Content Strategist, Editor/QA
- **HIGH**: Technical Writer, Tutorial Creator, Social Media Writer, Visual Creator
- **MEDIUM**: News Writer, Visual QA Analyst, SEO Specialist
- **LOW**: Content Performance Analyst, Learning Materials Designer

### Standard Content Metrics
- Blog Posts: 1,500-3,000 words
- News Articles: 500-800 words
- Social Posts: Platform-optimized length
- Tutorials: 2,000+ words with code examples
- Technical Guides: Comprehensive with visuals

### Integration Timeline
- Week 1-2: MVP (Research, Writing, Editing)
- Week 3-4: Expansion (Strategy, Social, Visual)
- Week 5-6: Optimization (Tutorials, News, QA)
- Week 7+: Scale (SEO, Analytics, Learning)

---

## Template Version
- **Version**: 1.0.0
- **Last Updated**: 2024-09-14
- **Author**: Intellidoc Development Team
- **Status**: Production Ready

---

## Additional Resources

- Anthropic Sub-agents Documentation: https://docs.anthropic.com/en/docs/claude-code/sub-agents
- Claude Code Best Practices: https://www.anthropic.com/engineering/claude-code-best-practices
- Building Effective Agents: https://www.anthropic.com/research/building-effective-agents
- Implementation Report: `subagents/code/subagents-implementation-report.md`
- Position Descriptions: `subagents/writing/content-creation-firm_Intellidoc-op/subagent-positions.md`

---

*This template is designed for recursive feeding to Claude and Claude Code for developing production-ready content creation sub-agents.*