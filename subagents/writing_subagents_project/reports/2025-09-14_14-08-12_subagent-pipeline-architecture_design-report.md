# Sub-Agent Pipeline Architecture
## Design Report for Intellidoc Content Creation System

**Report Date**: 2025-09-14
**Report Time**: 14:08:12 CET
**Report Type**: Design Report
**Author**: Intellidoc Development Team
**Purpose**: Define comprehensive sub-agent pipeline with logical decomposition and interconnections

---

## Executive Summary

This report presents a complete architectural design for the Intellidoc content creation system, decomposing the current monolithic sub-agents into 41 focused, single-purpose agents. The new architecture creates a flexible pipeline where agents can be combined in various configurations to produce different content types, with clear dependencies and optional branches that maximize efficiency through parallel processing.

### Key Design Principles
- **Single Responsibility**: Each agent performs one specific task (20-35 lines)
- **Flexible Composition**: Agents combine differently for different content needs
- **Parallel Processing**: Independent agents can run simultaneously
- **Optional Branches**: Not all agents required for every content type
- **Feedback Loops**: Continuous improvement through performance analysis

---

## Complete Sub-Agent Inventory (41 Agents)

### Phase 1: Research & Discovery (5 agents)

| Agent Name | Purpose | Model | Inputs From | Outputs To |
|------------|---------|-------|-------------|------------|
| **topic-scout** | Identifies trending topics and content opportunities | sonnet | metrics feedback or standalone | source-gatherer, content-planner |
| **source-gatherer** | Collects authoritative sources and references | sonnet | topic-scout or spec-writer | fact-verifier, competitor-analyzer |
| **competitor-analyzer** | Analyzes competing content for gaps | sonnet | source-gatherer | angle-definer, spec-writer |
| **fact-verifier** | Validates claims and statistics | sonnet | source-gatherer | spec-writer, body-writer |
| **keyword-researcher** | Identifies SEO opportunities | haiku | topic-scout or content-planner | spec-writer, body-writer |

### Phase 2: Strategy & Planning (5 agents)

| Agent Name | Purpose | Model | Inputs From | Outputs To |
|------------|---------|-------|-------------|------------|
| **content-planner** | Creates content calendar and priorities | opus | topic-scout or standalone | spec-writer |
| **angle-definer** | Determines unique perspective and approach | sonnet | competitor-analyzer | spec-writer |
| **audience-profiler** | Defines target audience characteristics | sonnet | content-planner | spec-writer, body-writer |
| **spec-writer** | Creates detailed content specifications | opus | multiple sources | template-selector, outline-builder |
| **template-selector** | Chooses appropriate content templates | haiku | spec-writer | outline-builder, body-writer |

### Phase 3: Content Creation (5 agents)

| Agent Name | Purpose | Model | Inputs From | Outputs To |
|------------|---------|-------|-------------|------------|
| **outline-builder** | Creates structured content outlines | sonnet | spec-writer | intro-writer, body-writer |
| **intro-writer** | Crafts compelling introductions | sonnet | outline-builder | body-writer |
| **body-writer** | Writes main content sections | sonnet | outline-builder, intro-writer | conclusion-writer |
| **conclusion-writer** | Creates effective closings and CTAs | sonnet | body-writer | grammar-checker |
| **quote-integrator** | Incorporates expert quotes and citations | haiku | fact-verifier | body-writer |

### Phase 4: Technical Content (4 agents)

| Agent Name | Purpose | Model | Inputs From | Outputs To |
|------------|---------|-------|-------------|------------|
| **code-example-writer** | Creates working code snippets | sonnet | spec-writer | command-demonstrator |
| **api-documenter** | Writes technical API documentation | sonnet | spec-writer | code-example-writer |
| **command-demonstrator** | Shows CLI/terminal examples | haiku | code-example-writer | error-handler |
| **error-handler** | Documents error scenarios and solutions | sonnet | command-demonstrator | body-writer |

### Phase 5: Tutorial Creation (4 agents)

| Agent Name | Purpose | Model | Inputs From | Outputs To |
|------------|---------|-------|-------------|------------|
| **step-sequencer** | Orders learning steps progressively | sonnet | spec-writer | exercise-designer |
| **exercise-designer** | Creates practice problems | sonnet | step-sequencer | solution-provider |
| **solution-provider** | Writes exercise solutions | haiku | exercise-designer | concept-explainer |
| **concept-explainer** | Clarifies complex concepts | opus | step-sequencer | body-writer |

### Phase 6: Quality Assurance (5 agents)

| Agent Name | Purpose | Model | Inputs From | Outputs To |
|------------|---------|-------|-------------|------------|
| **grammar-checker** | Reviews grammar and spelling | haiku | conclusion-writer | style-editor |
| **style-editor** | Ensures brand voice consistency | sonnet | grammar-checker | flow-optimizer |
| **flow-optimizer** | Improves content structure | sonnet | style-editor | readability-scorer |
| **readability-scorer** | Assesses and improves clarity | haiku | flow-optimizer | link-validator |
| **link-validator** | Verifies all links and references | haiku | readability-scorer | content-atomizer |

### Phase 7: Visual Creation (5 agents)

| Agent Name | Purpose | Model | Inputs From | Outputs To |
|------------|---------|-------|-------------|------------|
| **ai-prompt-engineer** | Creates image generation prompts | sonnet | body-writer | visual pipeline |
| **chart-designer** | Specifies data visualizations | sonnet | fact-verifier | infographic-planner |
| **infographic-planner** | Designs infographic layouts | sonnet | chart-designer | visual pipeline |
| **thumbnail-creator** | Designs video/article thumbnails | haiku | ai-prompt-engineer | distribution |
| **diagram-sketcher** | Creates technical diagrams | sonnet | code-example-writer | visual pipeline |

### Phase 8: Distribution (5 agents)

| Agent Name | Purpose | Model | Inputs From | Outputs To |
|------------|---------|-------|-------------|------------|
| **content-atomizer** | Extracts key points for reuse | sonnet | link-validator | all formatters |
| **twitter-formatter** | Creates Twitter threads | haiku | content-atomizer | publishing |
| **linkedin-adapter** | Formats for LinkedIn posts | haiku | content-atomizer | publishing |
| **instagram-packager** | Creates Instagram content | haiku | content-atomizer | publishing |
| **newsletter-curator** | Formats for email newsletters | sonnet | content-atomizer | publishing |

### Phase 9: Performance Analysis (3 agents)

| Agent Name | Purpose | Model | Inputs From | Outputs To |
|------------|---------|-------|-------------|------------|
| **metrics-collector** | Gathers engagement data | haiku | published content | trend-spotter |
| **trend-spotter** | Identifies performance patterns | sonnet | metrics-collector | improvement-advisor |
| **improvement-advisor** | Suggests optimizations | opus | trend-spotter | spec-writer, topic-scout |

---

## Pipeline Flow Diagrams

### Main Content Pipeline
```
[Entry Points]
    ↓
topic-scout → source-gatherer → fact-verifier
                    ↓
            competitor-analyzer
                    ↓
            angle-definer → audience-profiler
                    ↓
                spec-writer
                    ↓
            template-selector
                    ↓
            outline-builder
                    ↓
    [intro-writer] + [body-writer] + [conclusion-writer]
                    ↓
            [Quality Assurance Chain]
                    ↓
            [Visual Creation] (parallel)
                    ↓
            content-atomizer
                    ↓
        [Distribution Formatters]
                    ↓
            metrics-collector
                    ↓
    [Performance Analysis → Feedback Loop]
```

### Technical Content Branch
```
spec-writer
    ↓
[code-example-writer] + [api-documenter]
    ↓
command-demonstrator
    ↓
error-handler
    ↓
→ Merge with main pipeline at body-writer
```

### Tutorial Content Branch
```
spec-writer
    ↓
step-sequencer
    ↓
[exercise-designer] + [concept-explainer]
    ↓
solution-provider
    ↓
→ Merge with main pipeline at body-writer
```

### Visual Content Parallel Track
```
body-writer → ai-prompt-engineer → thumbnail-creator
    ↓
fact-verifier → chart-designer → infographic-planner
    ↓
code-example-writer → diagram-sketcher
    ↓
All converge → Visual Pipeline Output
```

---

## Pipeline Configuration Examples

### Configuration 1: News Article (Quick Turnaround)
```
Active Agents (9 total):
1. topic-scout
2. source-gatherer
3. fact-verifier
4. spec-writer (simplified)
5. body-writer
6. grammar-checker
7. ai-prompt-engineer
8. content-atomizer
9. twitter-formatter

Time: 30 minutes
Model Mix: 70% Haiku, 30% Sonnet
```

### Configuration 2: Technical Tutorial (Comprehensive)
```
Active Agents (18 total):
1. source-gatherer
2. fact-verifier
3. spec-writer
4. outline-builder
5. intro-writer
6. body-writer
7. conclusion-writer
8. code-example-writer
9. command-demonstrator
10. error-handler
11. step-sequencer
12. exercise-designer
13. solution-provider
14. concept-explainer
15. All QA agents (5)
16. diagram-sketcher
17. content-atomizer
18. linkedin-adapter

Time: 90 minutes
Model Mix: 20% Haiku, 60% Sonnet, 20% Opus
```

### Configuration 3: Social Media Campaign (From Existing Content)
```
Active Agents (7 total):
1. content-atomizer (entry point)
2. ai-prompt-engineer
3. thumbnail-creator
4. twitter-formatter
5. linkedin-adapter
6. instagram-packager
7. metrics-collector

Time: 15 minutes
Model Mix: 85% Haiku, 15% Sonnet
```

---

## Interconnection Benefits

### 1. Parallel Processing Opportunities
- **Visual Track**: Runs while content is being written
- **Distribution Formatting**: All platforms processed simultaneously
- **QA Checks**: Grammar and link validation in parallel

### 2. Flexible Entry Points
- **New Content**: Start with topic-scout
- **Assigned Topic**: Start with spec-writer
- **Content Repurposing**: Start with content-atomizer
- **Performance Improvement**: Start with metrics-collector

### 3. Optional Branches
- **Skip Technical**: For non-technical content
- **Skip Tutorial**: For news/opinion pieces
- **Skip Visual**: For text-only requirements
- **Skip Distribution**: For internal documents

### 4. Feedback Loops
```
improvement-advisor → spec-writer (Better specifications)
trend-spotter → topic-scout (Topic selection)
metrics-collector → template-selector (Template optimization)
readability-scorer → body-writer (Writing improvement)
```

---

## Resource Optimization

### Model Distribution Strategy

| Model | Agent Count | Primary Use | Cost/1000 Runs |
|-------|------------|-------------|----------------|
| **Haiku** | 15 agents (37%) | Formatting, validation, simple tasks | $12 |
| **Sonnet** | 20 agents (49%) | Content creation, analysis | $60 |
| **Opus** | 6 agents (14%) | Strategy, complex reasoning | $90 |

### Token Usage Projection

| Pipeline Type | Average Tokens | Cost per Run | Time |
|--------------|---------------|--------------|------|
| News Article | 8,000 | $0.024 | 30 min |
| Technical Tutorial | 25,000 | $0.075 | 90 min |
| Social Campaign | 3,000 | $0.009 | 15 min |
| Full Pipeline | 40,000 | $0.120 | 120 min |

---

## Implementation Priorities

### Phase 1: Core Pipeline (Week 1-2)
**15 Essential Agents**
- Research: source-gatherer, fact-verifier
- Planning: spec-writer, template-selector
- Writing: outline-builder, body-writer
- QA: grammar-checker, style-editor
- Distribution: content-atomizer, twitter-formatter
- Analysis: metrics-collector

### Phase 2: Enhanced Quality (Week 3)
**10 Quality Agents**
- Writing: intro-writer, conclusion-writer, quote-integrator
- QA: flow-optimizer, readability-scorer, link-validator
- Planning: angle-definer, audience-profiler
- Analysis: trend-spotter, improvement-advisor

### Phase 3: Specialized Content (Week 4)
**11 Specialty Agents**
- Technical: All 4 technical agents
- Tutorial: All 4 tutorial agents
- Visual: ai-prompt-engineer, chart-designer, thumbnail-creator

### Phase 4: Complete Ecosystem (Week 5)
**5 Remaining Agents**
- Research: topic-scout, competitor-analyzer, keyword-researcher
- Planning: content-planner
- Visual: infographic-planner, diagram-sketcher
- Distribution: linkedin-adapter, instagram-packager, newsletter-curator

---

## Success Metrics

### System Performance
- **Agent Size**: All under 35 lines (vs 305 average currently)
- **Token Efficiency**: 80% reduction from monolithic agents
- **Processing Speed**: 3-5x faster through parallelization
- **Cost Reduction**: 75% lower operational costs
- **Flexibility**: 15+ different pipeline configurations

### Content Quality
- **Consistency**: 100% brand voice adherence
- **Accuracy**: 100% fact verification
- **Engagement**: 40% higher than baseline
- **Production**: 5-10x content output increase
- **Error Rate**: <1% post-QA

---

## Risk Mitigation

### Potential Challenges & Solutions

| Challenge | Risk Level | Mitigation Strategy |
|-----------|------------|-------------------|
| Agent coordination complexity | Medium | Clear interface contracts, extensive testing |
| Data passing overhead | Low | Lightweight JSON, shared memory optimization |
| Parallel processing conflicts | Low | Isolated execution environments |
| Quality consistency | Medium | Strict QA chain, template enforcement |
| Cost management | Low | Model selection optimization, caching |

---

## Conclusion

This pipeline architecture transforms the Intellidoc content creation system from monolithic, inefficient agents into a flexible, scalable ecosystem of 41 focused sub-agents. The design enables:

1. **Modular Composition**: Build custom pipelines for any content type
2. **Parallel Processing**: Maximize efficiency through simultaneous execution
3. **Cost Optimization**: 75% reduction through right-sized agents and models
4. **Quality Assurance**: Multiple checkpoints ensure consistent excellence
5. **Continuous Improvement**: Feedback loops drive ongoing optimization

The phased implementation plan allows for incremental deployment while maintaining system stability, with the core pipeline operational in 2 weeks and full ecosystem within 5 weeks.

---

## Appendices

### Appendix A: Agent Naming Conventions
- **Action-Object**: grammar-checker, content-atomizer
- **Role-Based**: trend-spotter, concept-explainer
- **Platform-Specific**: twitter-formatter, linkedin-adapter

### Appendix B: Data Flow Formats
```json
// Lightweight inter-agent communication
{
  "agent_id": "source-gatherer",
  "timestamp": "2025-09-14T14:08:12Z",
  "content_id": "article_123",
  "output": {
    "sources": [...],
    "metadata": {...}
  },
  "next_agents": ["fact-verifier", "competitor-analyzer"]
}
```

### Appendix C: Quick Reference Matrix

| Content Type | Required Agents | Optional Agents | Time | Cost |
|-------------|----------------|-----------------|------|------|
| News | 9 | 3 | 30m | $0.024 |
| Blog Post | 12 | 5 | 45m | $0.036 |
| Tutorial | 18 | 4 | 90m | $0.075 |
| Technical Doc | 15 | 3 | 60m | $0.050 |
| Social Campaign | 7 | 2 | 15m | $0.009 |

---

*This design report serves as the architectural blueprint for implementing the Intellidoc sub-agent pipeline system, providing a clear path from current monolithic agents to a flexible, efficient content creation ecosystem.*

---

## References & Sources

### Anthropic Documentation
- Sub-agents Documentation: https://docs.anthropic.com/en/docs/claude-code/sub-agents
- Claude Code Best Practices: https://www.anthropic.com/engineering/claude-code-best-practices
- Building Effective Agents: https://www.anthropic.com/research/building-effective-agents
- Multi-Agent Research System: https://www.anthropic.com/engineering/multi-agent-research-system
- Agent Framework: https://www.anthropic.com/news/our-framework-for-developing-safe-and-trustworthy-agents
- Claude Code Overview: https://docs.anthropic.com/en/docs/claude-code/overview
- MCP Documentation: https://docs.anthropic.com/en/docs/mcp

### GitHub Repositories
- Anthropic Claude Code: https://github.com/anthropics/claude-code
- Anthropic Cookbook - Agent Patterns: https://github.com/anthropics/anthropic-cookbook/tree/main/patterns/agents
- Example Sub-agents Collection (wshobson): https://github.com/wshobson/agents
- MCP Servers Directory: https://github.com/modelcontextprotocol/servers
- MCP Agent Framework: https://github.com/lastmile-ai/mcp-agent

### Industry Research Sources
- IBM Content Operations Case Study: https://www.clearvoice.com/resources/successful-content-operations-team/
- Shopify Plus Content Team Analysis: https://www.superside.com/blog/content-operations
- Tech News Landscape Analysis (Digiday): https://digiday.com/media/whos-winning-tech-news-web/
- Jasper AI Platform: https://www.jasper.ai
- Jasper Workflow Automation: https://www.jasper.ai/blog/how-to-automate-your-workflows-with-ai

### Internal Project Documentation
- Implementation Report: `/subagents/code/subagents-implementation-report.md`
- Sub-agent Positions: `/subagents/writing/content-creation-firm_Intellidoc-op/subagent-positions.md`
- Research Resources: `/subagents/writing/content-creation-firm_Intellidoc-op/research-resources.md`
- Sub-agent Template: `/subagents/writing/content_creation_subagents/SUBAGENT_POSITION_TEMPLATE.md`
- Project CLAUDE.md: `/subagents/writing_subagents_project/CLAUDE.md`