# Optimized Content Pipeline Implementation

## Context Inheritance
@../CLAUDE.md  # Inherits parent context for content creation subagents framework

## Operational Procedures
@./OPERATIONAL_GUIDE.md  # Complete pipeline execution instructions and workflows

## Overview
This directory contains the production-ready implementation of the Intellidoc content pipeline with 41 specialized subagents organized into 9 operational phases. Each agent is optimized for specific tasks with appropriate model selection (Haiku/Sonnet/Opus) based on complexity and cost efficiency.

## Directory Structure
```
/content_subagent_files/
├── CLAUDE.md                    # This file - implementation context
├── OPERATIONAL_GUIDE.md         # Detailed execution procedures
└── /optimized_versions/         # 41 production subagents
    ├── topic-scout.md          # Phase 1: Research agents
    ├── body-writer.md          # Phase 3: Content creation
    ├── grammar-checker.md      # Phase 6: QA agents
    └── [38 other agents...]
```

## File Naming Convention

**Format**: `[seq]_YYYY-MM-DD_HHMMSS_[descriptive-name].md`

**Timezone**: Zürich, Switzerland (CET/CEST)

This ensures chronological ordering for all pipeline outputs and reports.

## Subagent Registry by Phase

### Phase 1: Research & Discovery (5 agents)
| Agent | Model | Purpose |
|-------|-------|---------|
| `topic-scout` | sonnet | Identify trending topics and opportunities |
| `source-gatherer` | sonnet | Collect 5-7 authoritative sources |
| `competitor-analyzer` | sonnet | Analyze competing content |
| `fact-verifier` | sonnet | Validate claims and statistics |
| `keyword-researcher` | haiku | Identify SEO opportunities |

### Phase 2: Strategy & Planning (5 agents)
| Agent | Model | Purpose |
|-------|-------|---------|
| `content-planner` | opus | Create editorial calendar |
| `angle-definer` | sonnet | Determine unique perspective |
| `audience-profiler` | sonnet | Define target readers |
| `spec-writer` | opus | Create detailed specifications |
| `template-selector` | sonnet | Choose content structure |

### Phase 3: Content Creation (5 agents)
| Agent | Model | Purpose |
|-------|-------|---------|
| `outline-builder` | sonnet | Create content structure |
| `intro-writer` | sonnet | Craft engaging introductions |
| `body-writer` | sonnet | Write main content sections |
| `conclusion-writer` | sonnet | Create compelling closings |
| `quote-integrator` | sonnet | Add citations and sources |

### Phase 4: Technical Content (4 agents)
| Agent | Model | Purpose |
|-------|-------|---------|
| `code-example-writer` | sonnet | Create code snippets |
| `api-documenter` | sonnet | Write API documentation |
| `command-demonstrator` | haiku | Show CLI examples |
| `error-handler` | sonnet | Document troubleshooting |

### Phase 5: Tutorial Creation (4 agents)
| Agent | Model | Purpose |
|-------|-------|---------|
| `step-sequencer` | sonnet | Order learning steps |
| `exercise-designer` | sonnet | Create practice problems |
| `solution-provider` | haiku | Write solutions |
| `concept-explainer` | opus | Clarify complex concepts |

### Phase 6: Quality Assurance (5 agents)
| Agent | Model | Purpose |
|-------|-------|---------|
| `grammar-checker` | haiku | Fix language errors |
| `style-editor` | sonnet | Ensure brand voice |
| `flow-optimizer` | sonnet | Improve structure |
| `readability-scorer` | haiku | Assess clarity |
| `link-validator` | haiku | Verify references |

### Phase 7: Visual Creation (5 agents)
| Agent | Model | Purpose |
|-------|-------|---------|
| `ai-prompt-engineer` | sonnet | Generate image prompts |
| `chart-designer` | sonnet | Create data visualizations |
| `infographic-planner` | sonnet | Design infographic layouts |
| `thumbnail-creator` | sonnet | Create social thumbnails |
| `diagram-sketcher` | sonnet | Technical diagram specs |

### Phase 8: Distribution (5 agents)
| Agent | Model | Purpose |
|-------|-------|---------|
| `content-atomizer` | sonnet | Extract key points |
| `twitter-formatter` | haiku | Create Twitter threads |
| `linkedin-adapter` | haiku | Format LinkedIn posts |
| `instagram-packager` | haiku | Package Instagram content |
| `newsletter-curator` | sonnet | Format email newsletters |

### Phase 9: Performance Analysis (3 agents)
| Agent | Model | Purpose |
|-------|-------|---------|
| `metrics-collector` | haiku | Gather performance data |
| `trend-spotter` | sonnet | Identify patterns |
| `improvement-advisor` | opus | Recommend optimizations |

## Pipeline Architecture

### Execution Flow
```
User Request → Orchestrator → Phase Selection → Agent Invocation → Output Assembly
                                    ↓
                            Parallel Execution Groups
```

### Model Distribution
- **Haiku (35%)**: 14 agents - Simple formatting, validation, metrics
- **Sonnet (50%)**: 20 agents - Content creation, analysis, planning
- **Opus (15%)**: 7 agents - Complex reasoning, strategy, improvement

### Cost Optimization Strategy
1. Use Haiku for repetitive, simple tasks
2. Deploy Sonnet for standard content operations
3. Reserve Opus for critical decision points
4. Enable parallel execution where possible

## Integration Context

### With Parent System
This implementation integrates with the broader Intellidoc content creation framework:
- Receives specifications from parent orchestrator
- Reports completion metrics upstream
- Maintains compatibility with template system

### With OPERATIONAL_GUIDE
The OPERATIONAL_GUIDE.md in this directory provides:
- Detailed command sequences
- Pipeline configuration examples
- Testing and debugging procedures
- Performance optimization tactics

## Common Workflows

### Quick Reference
For detailed execution instructions, see OPERATIONAL_GUIDE.md sections:
- Quick News Article (30 min) - 9 agents
- Blog Post (45 min) - 12 agents
- Comprehensive Tutorial (90 min) - 18 agents
- Social Campaign (15 min) - 7 agents

### Parallel Execution Groups
Agents that can run simultaneously:
1. Research Group: `source-gatherer`, `competitor-analyzer`
2. Content Group: `intro-writer`, `body-writer`
3. QA Group: `grammar-checker`, `link-validator`, `readability-scorer`
4. Distribution Group: All social formatters

## Quality Standards

### Output Requirements
- Magazine-quality writing (Wired/TechCrunch level)
- 5-7 authoritative sources minimum
- SEO optimization without keyword stuffing
- Brand voice consistency across all outputs
- Accessibility compliance (WCAG 2.1)

### Performance Metrics
- Pipeline completion rate: >95%
- Average time per article: <60 minutes
- Cost per 1000 words: <$0.02
- Quality score: >90%

## Development Guidelines

### Adding New Agents
1. Use appropriate template from parent directory
2. Select model based on complexity
3. Place in `/optimized_versions/`
4. Update this registry
5. Test with sample inputs
6. Document in OPERATIONAL_GUIDE

### Modifying Existing Agents
1. Maintain backward compatibility
2. Test thoroughly before deployment
3. Update performance metrics
4. Document changes in version history

## Best Practices

### DO
- Follow the 9-phase pipeline structure
- Use parallel execution for efficiency
- Monitor token usage per agent
- Validate outputs at phase boundaries
- Maintain clear handoffs between agents

### DON'T
- Skip QA phase for speed
- Use high-cost models unnecessarily
- Modify agent interfaces without testing
- Process without specifications
- Mix responsibilities between phases

## Troubleshooting Context

### Common Issues
- **Agent timeouts**: Break content into smaller chunks
- **Inconsistent voice**: Strengthen style-editor constraints
- **High costs**: Review model selection, use more Haiku
- **Pipeline failures**: Check agent input/output formats

For detailed troubleshooting procedures, see OPERATIONAL_GUIDE.md#troubleshooting-guide

## Monitoring & Maintenance

### Key Metrics to Track
- Token usage by agent and phase
- Success rates per agent
- Time per phase completion
- Cost per content type
- Quality scores by category

### Regular Reviews
- Weekly: Performance metrics analysis
- Monthly: Cost optimization review
- Quarterly: Agent prompt refinement

---

*This CLAUDE.md provides implementation context for the optimized content pipeline. For execution procedures, refer to OPERATIONAL_GUIDE.md. For framework context, see parent CLAUDE.md files.*