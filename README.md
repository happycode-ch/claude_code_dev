# Claude Code Development Environment

A sophisticated subagent orchestration system for AI-powered content creation and development workflows.

## 🎯 Overview

This repository implements a hierarchical Claude Code environment with specialized subagents organized by domain expertise. It demonstrates best practices for creating CLAUDE.md configuration files and orchestrating multiple AI agents for complex tasks.

## 🏗️ Architecture

```
claude_code_dev/
├── .claude/                    # User-level configuration
│   └── CLAUDE.md              # Orchestration guidelines
├── .docs/                      # Documentation
│   └── best_practices/        # CLAUDE.md best practices
├── subagents/                  # Subagent categories
│   ├── code/                  # Development subagents
│   └── writing_subagents_project/  # Content creation
└── README.md                   # This file
```

## 🚀 Features

- **Hierarchical CLAUDE.md Structure**: User → Project → Module level configuration
- **Intellidoc Content System**: Spec-driven content production pipeline
- **Specialized Subagents**: Domain-specific AI agents for different tasks
- **Timestamped Documentation**: Zürich timezone convention for tracking
- **Best Practices Integration**: Based on Anthropic's official guidelines

## 📋 Prerequisites

- [Claude Code](https://claude.ai/code) installed and configured
- Git for version control
- GitHub CLI (`gh`) for repository management (optional)

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/happycode-ch/claude_code_dev.git
cd claude_code_dev
```

2. The CLAUDE.md files will automatically be loaded by Claude Code when you open the project.

## 📖 Documentation Structure

### CLAUDE.md Files

- **`.claude/CLAUDE.md`**: User-level orchestration and project-wide conventions
- **`subagents/writing_subagents_project/CLAUDE.md`**: Folder-level configuration for content creation

### File Naming Convention

All timestamped documentation follows this format:
```
[seq]_YYYY-MM-DD_HHMMSS_[descriptive-name].md
```

Example: `04_2025-09-05_170200_content-strategy-report.md`

## 🤖 Subagent Categories

### Writing Subagents (Intellidoc)

A complete content creation pipeline with specialized agents:

| Agent | Purpose | Model | Status |
|-------|---------|-------|--------|
| Research Analyst | Source gathering and fact-checking | Sonnet | ✅ Example |
| Content Strategist | Spec creation and planning | Sonnet | ⏳ Pending |
| Technical Writer | Long-form technical content | Opus/Sonnet | ⏳ Pending |
| Editor/QA | Quality assurance and editing | Sonnet | ⏳ Pending |
| Social Media Writer | Platform-optimized content | Haiku | ⏳ Pending |

### Future Categories

- **Code Subagents**: Development, testing, and code review
- **Research Subagents**: Data analysis and information gathering
- **Automation Subagents**: Task automation and workflow optimization

## 💡 Usage

### Creating New Subagents

1. Navigate to the appropriate category folder
2. Copy the `SUBAGENT_POSITION_TEMPLATE.md`
3. Fill in all required sections
4. Save as `[agent-name].md`
5. Test with Claude Code

### Running Content Pipeline

```bash
# Example workflow
claude --model sonnet
> Use the research-analyst to gather sources on [topic]
> Use the technical-writer to create an article
> Use the editor-qa to review the content
```

## 📊 Project Standards

### Quality Requirements
- Magazine-quality content (Wired, TechCrunch level)
- Minimum 5 authoritative sources per article
- 100% spec compliance
- Brand voice consistency

### Performance Metrics
- Content quality score: >90%
- Error rate: <2%
- Production velocity: 5-10 articles/week

## 🔧 Configuration

### Model Selection Guide

| Model | Use Case | Cost/M Tokens |
|-------|----------|---------------|
| Haiku 3.5 | Simple tasks, formatting | $0.80/$4 |
| Sonnet 4 | Standard development, content | $3/$15 |
| Opus 4 | Complex reasoning, strategy | $15/$75 |

### Tool Access

Subagents have access to:
- Read/Write files
- Web search and fetch
- Bash commands (restricted)
- Pattern matching (Grep/Glob)

## 🤝 Contributing

1. Follow the CLAUDE.md template structure
2. Use timestamped naming convention
3. Document all customizations
4. Test thoroughly before committing

## 📝 License

This project is designed for use with Claude Code and follows Anthropic's best practices for AI-assisted development.

## 🔗 Resources

- [Anthropic Subagents Documentation](https://docs.anthropic.com/en/docs/claude-code/sub-agents)
- [Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)
- [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)

## 📞 Support

For issues or questions:
- Create an issue in this repository
- Refer to the documentation in `.docs/best_practices/`
- Check the implementation report in `subagents/code/`

---

*Built with Claude Code - Orchestrating AI for intelligent content creation*