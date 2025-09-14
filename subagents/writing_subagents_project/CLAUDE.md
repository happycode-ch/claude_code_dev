# Intellidoc Content Creation Subagents Project

## Project Overview
Intellidoc is a spec-driven, AI-powered content production system that delivers magazine-quality written and visual content across multiple channels. This project implements specialized writing subagents that work together as a virtual content creation firm, maintaining editorial excellence while leveraging automation for scale.

## Mission
Transform ideas into high-quality, multi-format content through orchestrated AI subagents, each specializing in specific aspects of the content lifecycle - from research and strategy to writing, editing, and distribution.

## Tech Stack & Dependencies
- **Framework**: Claude Code Subagents (Anthropic)
- **Models**: Haiku 3.5, Sonnet 4, Opus 4 (task-appropriate selection)
- **Visual Analysis**: Playwright/Puppeteer integration
- **Version Control**: Git-based content versioning
- **Tools**: WebSearch, WebFetch, Read, Write, Bash, Grep, Glob

## Project Structure
```
/writing_subagents_project/
├── /content_creation_subagents/        # Subagent definitions
│   ├── SUBAGENT_POSITION_TEMPLATE.md  # Master template (SOURCE OF TRUTH)
│   ├── research-analyst-EXAMPLE.md    # Reference implementation
│   └── /content_subagent_files/       # Active subagents
├── /content-creation-firm_Intellidoc-op/  # Firm documentation
│   ├── firm-description.md            # What we do
│   ├── mission-statement.md           # Why we exist
│   ├── subagent-positions.md          # Role definitions
│   └── research-resources.md          # Source materials
└── /reports/                           # Timestamped outputs
```

## File Naming Convention

**Format**: `[seq]_YYYY-MM-DD_HHMMSS_[descriptive-name].md`

**Timezone**: Zürich, Switzerland (CET/CEST)

**Example**: `04_2025-09-05_170200_content-strategy-report.md`

Components:
- Sequential number (01, 02, 03...)
- ISO date format (YYYY-MM-DD)
- 24-hour time (HHMMSS)
- Descriptive name with underscores

## Content Production Pipeline

### Phase 1: Research & Planning
```
Research Analyst → Content Strategist → Spec Generation
```
- Gather 5-10 authoritative sources
- Analyze competitor content
- Define angle, tone, structure
- Create detailed content specifications

### Phase 2: Content Creation
```
Technical Writer / News Writer / Tutorial Creator → Draft Content
```
- Long-form articles (1,500-3,000 words)
- Technical tutorials with code examples
- Breaking news coverage (500-800 words)
- Educational materials

### Phase 3: Enhancement & QA
```
Editor/QA → Visual Creator → SEO Specialist → Final Output
```
- Quality verification against spec
- Brand voice consistency
- Visual asset creation
- SEO optimization

### Phase 4: Distribution
```
Social Media Writer → Content Atomization → Multi-Channel Publishing
```
- Platform-specific content adaptation
- Twitter threads, LinkedIn posts
- Newsletter segments
- Documentation updates

## Subagent Implementation Status

| Agent | Priority | Model | Status | Location |
|-------|----------|-------|--------|----------|
| Research Analyst | CRITICAL | sonnet | ✅ Example | `research-analyst-EXAMPLE.md` |
| Content Strategist | CRITICAL | sonnet | ⏳ Pending | - |
| Technical Writer | HIGH | opus/sonnet | ⏳ Pending | - |
| Editor/QA | CRITICAL | sonnet | ⏳ Pending | - |
| Social Media Writer | HIGH | haiku | ⏳ Pending | - |
| Visual Creator | HIGH | opus | ⏳ Pending | - |
| Tutorial Creator | HIGH | sonnet | ⏳ Pending | - |
| News Writer | MEDIUM | haiku | ⏳ Pending | - |
| SEO Specialist | MEDIUM | haiku | ⏳ Pending | - |

## Development Workflow

### Creating New Subagents
1. Copy `SUBAGENT_POSITION_TEMPLATE.md`
2. Name as `[agent-name].md` in `/content_subagent_files/`
3. Fill all template sections
4. Validate YAML frontmatter
5. Test with sample inputs
6. Document in this CLAUDE.md

### Testing Subagents
```bash
# Individual agent test
claude --model sonnet
> Test the [agent-name] agent with [sample input]

# Pipeline test
> Use research-analyst to gather sources on [topic]
> Use technical-writer to create article from research
> Use editor-qa to review the article
```

## Quality Standards

### Content Requirements
- **Magazine Quality**: Match Wired, TechCrunch, The Verge standards
- **Research Depth**: Minimum 5 authoritative sources
- **Technical Accuracy**: Code examples must be validated
- **Brand Consistency**: Maintain voice across all outputs
- **SEO Integration**: Natural keyword placement

### Output Specifications
- **Blog Posts**: 1,500-3,000 words with visuals
- **News Articles**: 500-800 words, <2 hour turnaround
- **Tutorials**: 2,000+ words with working code
- **Social Posts**: Platform-optimized lengths
- **Visual Assets**: Hero images, infographics, diagrams

## Coding Conventions

### Subagent Files
- Use lowercase with hyphens: `content-strategist.md`
- Include complete YAML frontmatter
- Follow SUBAGENT_POSITION_TEMPLATE.md structure
- Document all integration points
- Provide concrete examples

### Documentation
- Use timestamped format for reports
- Include metadata in outputs
- Track sources and citations
- Version all spec changes

## Architecture Patterns

### Model Selection Strategy
```
Complexity Assessment → Model Selection:
- Simple formatting → Haiku ($0.80/M)
- Content creation → Sonnet ($3/M)
- Complex reasoning → Opus ($15/M)
```

### Tool Access Philosophy
- Grant minimum necessary permissions
- Read-only for review agents
- Write access only when essential
- Bash restricted to safe operations

### Integration Pattern
```
Spec → Agent Selection → Execution → Validation → Handoff
```

## Common Tasks

### Adding a New Content Type
1. Define specification template
2. Identify required subagents
3. Create workflow sequence
4. Test with sample content
5. Document in `/reports/`

### Running Content Pipeline
1. Create content spec with requirements
2. Invoke research-analyst for sources
3. Pass to appropriate writer agent
4. Run through editor-qa
5. Generate visuals if needed
6. Optimize for SEO
7. Create social derivatives

### Quality Verification
1. Check spec compliance
2. Verify source citations
3. Validate technical accuracy
4. Ensure brand consistency
5. Test SEO optimization

## Known Issues & Solutions

### Token Limit Approaching
- Summarize research before writing
- Break long content into sections
- Use external storage for sources

### Quality Below Standard
- Review and strengthen specs
- Add more specific examples
- Increase model tier if needed

### Integration Failures
- Verify input/output formats match
- Check tool permissions
- Review error logs for specifics

## Security & Compliance

### Data Handling
- No storage of sensitive information
- Cite all sources properly
- Respect copyright and licensing
- Maintain transparency about AI use

### Access Controls
- Subagents have minimal permissions
- No direct database access
- Sandboxed execution environment
- Audit trail for all operations

## Performance Metrics

### Success Indicators
- Content quality score: >90%
- Spec compliance rate: 100%
- Production velocity: 5-10 articles/week
- Error rate: <2%
- Source verification: 100%

### Monitoring Points
- Token usage per content piece
- Time from spec to publication
- Quality scores by agent
- Integration success rates

## Best Practices

### DO
- Start with detailed specifications
- Use templates for consistency
- Validate at each pipeline stage
- Document all customizations
- Monitor performance metrics

### DON'T
- Skip quality verification steps
- Grant excessive permissions
- Mix agent responsibilities
- Ignore spec requirements
- Create content without sources

## Troubleshooting

### Agent Not Triggering
- Add "PROACTIVELY" to description
- Make description more specific
- Check tool availability

### Output Quality Issues
- Review and improve specs
- Add concrete examples
- Adjust model selection
- Strengthen guardrails

### Performance Problems
- Optimize token usage
- Use appropriate models
- Implement caching
- Parallelize where possible

## Integration Points

### With Parent Orchestrator
- Receives content requests from main CLAUDE.md
- Reports completion status upstream
- Integrates with other category subagents

### With External Systems
- Publishing platforms via API
- Analytics tools for metrics
- Version control for content
- Social media schedulers

## Future Enhancements

### Planned Features
- Parallel agent execution
- Advanced memory management
- Real-time collaboration
- Automated performance tuning
- Multi-language support

### Scaling Considerations
- Distributed processing capability
- State persistence across sessions
- Advanced caching strategies
- Cost optimization algorithms

## Resources

### Documentation
- [Anthropic Subagents Guide](https://docs.anthropic.com/en/docs/claude-code/sub-agents)
- Implementation Report: `/subagents/code/subagents-implementation-report.md`
- Template: `SUBAGENT_POSITION_TEMPLATE.md`
- Positions: `content-creation-firm_Intellidoc-op/subagent-positions.md`

### Examples
- Research Analyst: `research-analyst-EXAMPLE.md`
- Reports: `/reports/` directory

---

*This CLAUDE.md serves as the authoritative guide for the Intellidoc writing subagents project, providing context for Claude Code to effectively orchestrate content creation tasks.*