# Sub-Agent Positions for Automated Content Firm

## Phase 1: Core Production Team (MVP)

### 1. Research Analyst
**Model**: Sonnet  
**Priority**: CRITICAL  
**Tools**: web_search, read, write  
**Responsibilities**:
- Gather 5-10 authoritative sources per topic
- Analyze competitor content and identify gaps
- Create research briefs with key facts, quotes, data
- Monitor tech trends and breaking news
- Verify claims and fact-check information
- **Prioritize business-relevant topics**: Document processing pain points, automation opportunities, AI integration challenges
- **Identify prospect industries**: Research sectors that would benefit from our services
- **Competitive landscape**: What solutions exist and where we differentiate

### 2. Content Strategist
**Model**: Sonnet  
**Priority**: CRITICAL  
**Tools**: read, write, search  
**Responsibilities**:
- Transform research into detailed content specs
- Define angle, tone, structure for each piece
- Create content templates with examples
- Manage editorial calendar
- Ensure topic relevance and audience fit

### 3. Technical Writer
**Model**: Opus (for complex topics), Sonnet (standard)  
**Priority**: HIGH  
**Tools**: read, write, bash  
**Responsibilities**:
- Long-form technical articles (2,000+ words)
- Code examples and implementation details
- API documentation and technical guides
- Depth comparable to Ars Technica technical reviews
- Accuracy in technical concepts

### 4. Editor/QA
**Model**: Sonnet  
**Priority**: CRITICAL  
**Tools**: read, write, search  
**Responsibilities**:
- Final quality check against spec
- Brand voice consistency
- Fact verification
- Grammar and style editing
- SEO optimization without sacrificing quality

## Phase 2: Content Diversification

### 5. Tutorial Creator
**Model**: Sonnet  
**Priority**: HIGH  
**Tools**: read, write, bash, test  
**Responsibilities**:
- Step-by-step technical guides
- Working code examples
- Progressive difficulty levels
- Clear learning objectives
- Practical exercises

### 6. News Writer
**Model**: Haiku (for speed)  
**Priority**: MEDIUM  
**Tools**: web_search, read, write  
**Responsibilities**:
- Breaking news coverage
- Quick turnaround (< 2 hours)
- 500-800 word news articles
- Timely analysis and context
- Similar to TechCrunch news coverage

### 7. Social Media Writer
**Model**: Haiku  
**Priority**: HIGH  
**Tools**: read, write  
**Responsibilities**:
- Twitter threads from long-form content
- LinkedIn posts with professional tone
- Platform-specific optimization
- Hashtag research and integration
- Engagement-focused hooks

## Phase 3: Visual & Enhancement

### 8. Visual Creator
**Model**: Opus  
**Priority**: HIGH  
**Tools**: read, write, bash (for image generation APIs)  
**Special Requirements**: Playwright integration  
**Responsibilities**:
- Hero images for articles
- Infographics from data
- Technical diagrams
- Social media graphics
- Prompt engineering for image generation

### 9. Visual QA Analyst
**Model**: Sonnet  
**Priority**: MEDIUM  
**Tools**: read, bash (Playwright for visual analysis)  
**Responsibilities**:
- Compare generated visuals to reference standards
- Verify visual-text alignment
- Check accessibility (contrast, alt text)
- Ensure brand consistency in visuals
- A/B testing visual elements

### 10. SEO Specialist
**Model**: Haiku  
**Priority**: MEDIUM  
**Tools**: web_search, read, write  
**Responsibilities**:
- Keyword research and integration
- Meta descriptions and titles
- Internal linking strategy
- Content structure optimization
- Performance tracking setup

## Phase 4: Advanced Operations

### 11. Content Performance Analyst
**Model**: Sonnet  
**Priority**: LOW (initially)  
**Tools**: read, write, bash  
**Responsibilities**:
- Analyze engagement metrics
- Identify successful patterns
- Recommend spec improvements
- A/B testing coordination
- ROI analysis per content type

### 12. Learning Materials Designer
**Model**: Sonnet  
**Priority**: LOW  
**Tools**: read, write  
**Responsibilities**:
- Educational content structure
- Quiz and exercise creation
- Progressive learning paths
- Concept explanations
- Interactive examples

## Implementation Priority

### MVP Launch (Week 1-2):
1. Research Analyst
2. Technical Writer
3. Editor/QA

### Expansion (Week 3-4):
4. Content Strategist
5. Social Media Writer
6. Visual Creator

### Optimization (Week 5-6):
7. Tutorial Creator
8. News Writer
9. Visual QA Analyst

### Scale (Week 7+):
10. SEO Specialist
11. Content Performance Analyst
12. Learning Materials Designer

## Key Design Principles

- **Specialization**: Each agent excels at one thing
- **Clear Handoffs**: Defined input/output between agents
- **Quality Gates**: Multiple checkpoints before publication
- **Cost Optimization**: Use Haiku where speed matters, Opus for complex reasoning
- **Parallel Processing**: Multiple agents can work simultaneously on different aspects
- **Feedback Loops**: Performance data flows back to improve specs

## Success Metrics Per Agent

- **Research Analyst**: Sources per hour, fact accuracy rate
- **Writers**: Words per hour, spec compliance rate
- **Editor**: Error detection rate, brand consistency score
- **Visual Creator**: Images per article, visual quality score
- **Social Media**: Engagement rate, platform optimization score

This structure mirrors successful content operations at companies like IBM and Shopify Plus, adapted for AI-powered execution.