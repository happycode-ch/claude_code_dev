#!/usr/bin/env python3
"""
SubAgent Testing Harness - Agent Specification Loader
Load and parse agent specifications from markdown files
"""

import os
import re
import yaml
import json
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from dataclasses import dataclass

@dataclass
class AgentSpecification:
    """Parsed agent specification"""
    name: str
    description: str
    model: str
    tools: List[str]
    prompt: str
    examples: Optional[str] = None
    guardrails: Optional[str] = None
    metadata: Dict = None

    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "name": self.name,
            "description": self.description,
            "model": self.model,
            "tools": self.tools,
            "prompt": self.prompt,
            "examples": self.examples,
            "guardrails": self.guardrails,
            "metadata": self.metadata or {}
        }


class AgentSpecLoader:
    """Load agent specifications from optimized_versions directory"""

    def __init__(self, base_path: str = None):
        """Initialize specification loader"""
        if base_path:
            self.base_path = Path(base_path)
        else:
            # Default to the content_subagent_files directory
            self.base_path = Path(__file__).parent.parent.parent / "content_creation_subagents" / "content_subagent_files"

        self.optimized_dir = self.base_path / "optimized_versions"
        self.cache = {}

    def load_agent_spec(self, agent_name: str) -> str:
        """
        Load and parse agent markdown specification

        Args:
            agent_name: Name of the agent (e.g., 'keyword-researcher')

        Returns:
            Complete agent specification as string
        """
        # Check cache first
        if agent_name in self.cache:
            return self.cache[agent_name]

        # Try to find the agent file
        agent_file = self._find_agent_file(agent_name)

        if not agent_file:
            # Return a default specification if file not found
            return self._generate_default_spec(agent_name)

        try:
            with open(agent_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Cache the content
            self.cache[agent_name] = content
            return content

        except Exception as e:
            print(f"Error loading agent spec for {agent_name}: {e}")
            return self._generate_default_spec(agent_name)

    def parse_agent_spec(self, agent_name: str) -> AgentSpecification:
        """
        Parse agent specification into structured format

        Args:
            agent_name: Name of the agent

        Returns:
            Parsed AgentSpecification object
        """
        content = self.load_agent_spec(agent_name)

        # Extract YAML frontmatter if present
        yaml_data = self.extract_yaml_frontmatter(content)

        # Extract sections from markdown
        sections = self._extract_markdown_sections(content)

        # Build specification
        spec = AgentSpecification(
            name=yaml_data.get("name", agent_name),
            description=yaml_data.get("description", sections.get("description", "")),
            model=yaml_data.get("model", "sonnet"),
            tools=yaml_data.get("tools", []),
            prompt=sections.get("prompt", content),
            examples=sections.get("examples"),
            guardrails=sections.get("guardrails"),
            metadata=yaml_data
        )

        return spec

    def extract_yaml_frontmatter(self, content: str) -> Dict:
        """
        Extract YAML configuration from agent file

        Args:
            content: Markdown file content

        Returns:
            Parsed YAML data as dictionary
        """
        # Check for YAML frontmatter (between --- markers)
        yaml_pattern = r'^---\s*\n(.*?)\n---\s*\n'
        match = re.match(yaml_pattern, content, re.DOTALL)

        if match:
            yaml_content = match.group(1)
            try:
                return yaml.safe_load(yaml_content) or {}
            except yaml.YAMLError as e:
                print(f"Error parsing YAML frontmatter: {e}")
                return {}

        return {}

    def _find_agent_file(self, agent_name: str) -> Optional[Path]:
        """Find the agent specification file"""
        # Check if optimized_versions directory exists
        if not self.optimized_dir.exists():
            # Try non-optimized location
            alt_dir = self.base_path / "non-optimized" / "optimized_versions"
            if alt_dir.exists():
                self.optimized_dir = alt_dir

        # Look for the agent file
        possible_names = [
            f"{agent_name}.md",
            f"{agent_name}-agent.md",
            f"{agent_name}_agent.md"
        ]

        for name in possible_names:
            file_path = self.optimized_dir / name
            if file_path.exists():
                return file_path

        return None

    def _extract_markdown_sections(self, content: str) -> Dict[str, str]:
        """Extract sections from markdown content"""
        sections = {}

        # Remove YAML frontmatter if present
        content = re.sub(r'^---\s*\n.*?\n---\s*\n', '', content, flags=re.DOTALL)

        # Extract common sections
        section_patterns = {
            "description": r'##?\s*Description\s*\n(.*?)(?=\n##?\s|\Z)',
            "prompt": r'##?\s*Prompt\s*\n(.*?)(?=\n##?\s|\Z)',
            "examples": r'##?\s*Examples?\s*\n(.*?)(?=\n##?\s|\Z)',
            "guardrails": r'##?\s*Guardrails?\s*\n(.*?)(?=\n##?\s|\Z)',
            "instructions": r'##?\s*Instructions?\s*\n(.*?)(?=\n##?\s|\Z)'
        }

        for section_name, pattern in section_patterns.items():
            match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
            if match:
                sections[section_name] = match.group(1).strip()

        # If no prompt section found, use the entire content as prompt
        if "prompt" not in sections:
            sections["prompt"] = content.strip()

        return sections

    def _generate_default_spec(self, agent_name: str) -> str:
        """Generate a default specification for agents without files"""
        # Agent-specific default specifications
        default_specs = {
            "keyword-researcher": """
---
name: keyword-researcher
description: Research and identify relevant keywords for content optimization
model: haiku
tools: [WebSearch]
---

## Role
You are a keyword research specialist who identifies high-value keywords and search terms for content optimization.

## Instructions
1. Analyze the given topic and target audience
2. Identify primary keywords with good search volume
3. Find 3-5 relevant long-tail keywords
4. Assess keyword difficulty (easy/medium/hard)
5. Determine search volume levels (high/medium/low)

## Output Format
Return a JSON object with:
- primary_keyword: The main keyword to target
- long_tail: Array of 3-5 long-tail variations
- search_volume: Overall search volume level
- difficulty: Competition difficulty level
""",
            "body-writer": """
---
name: body-writer
description: Write main body content for articles and posts
model: sonnet
tools: [Write]
---

## Role
You are a skilled content writer who creates engaging, informative body content for articles.

## Instructions
1. Follow the provided outline structure
2. Write comprehensive content for each section
3. Maintain consistent tone and style
4. Include relevant examples and details
5. Ensure smooth transitions between sections

## Output Format
Return a JSON object with:
- body_content: The complete body text
- sections_written: Array of section names completed
""",
            "grammar-checker": """
---
name: grammar-checker
description: Check and correct grammar, spelling, and punctuation errors
model: haiku
tools: [Read]
---

## Role
You are a meticulous grammar checker who identifies and corrects language errors.

## Instructions
1. Scan the content for grammar errors
2. Identify spelling mistakes
3. Check punctuation usage
4. Correct any errors found
5. Maintain the original meaning and style

## Output Format
Return a JSON object with:
- corrected_content: The error-free version
- errors_found: Array of errors that were corrected
"""
        }

        # Return specific default or generic
        if agent_name in default_specs:
            return default_specs[agent_name]
        else:
            return f"""
---
name: {agent_name}
description: Specialized agent for content pipeline
model: sonnet
tools: []
---

## Role
You are the {agent_name} agent in the content creation pipeline.

## Instructions
Process the input according to your specialized role and return structured output.

## Output Format
Return appropriate JSON output based on your function.
"""

    def list_available_agents(self) -> List[str]:
        """List all available agent specifications"""
        agents = []

        if self.optimized_dir.exists():
            for file in self.optimized_dir.glob("*.md"):
                # Extract agent name from filename
                name = file.stem
                # Remove common suffixes
                name = name.replace("-agent", "").replace("_agent", "")
                agents.append(name)

        return sorted(agents)

    def get_agent_metadata(self, agent_name: str) -> Dict:
        """Get metadata for an agent without loading full spec"""
        content = self.load_agent_spec(agent_name)
        return self.extract_yaml_frontmatter(content)

    def validate_spec(self, agent_name: str) -> Tuple[bool, List[str]]:
        """
        Validate an agent specification

        Returns:
            Tuple of (is_valid, list_of_issues)
        """
        issues = []

        try:
            spec = self.parse_agent_spec(agent_name)

            # Check required fields
            if not spec.name:
                issues.append("Missing agent name")
            if not spec.description:
                issues.append("Missing description")
            if not spec.model:
                issues.append("Missing model specification")
            if not spec.prompt:
                issues.append("Missing prompt/instructions")

            # Validate model choice
            valid_models = ["haiku", "sonnet", "opus"]
            if spec.model and spec.model not in valid_models:
                issues.append(f"Invalid model: {spec.model}")

            # Check tools are valid
            valid_tools = [
                "Read", "Write", "Edit", "MultiEdit",
                "WebSearch", "WebFetch", "Bash", "Grep", "Glob"
            ]
            for tool in spec.tools:
                if tool not in valid_tools:
                    issues.append(f"Unknown tool: {tool}")

        except Exception as e:
            issues.append(f"Error parsing specification: {e}")

        return len(issues) == 0, issues

    def export_all_specs(self, output_path: str = None) -> str:
        """Export all agent specifications to a JSON file"""
        if not output_path:
            output_path = "agent_specifications.json"

        all_specs = {}
        agents = self.list_available_agents()

        for agent in agents:
            try:
                spec = self.parse_agent_spec(agent)
                all_specs[agent] = spec.to_dict()
            except Exception as e:
                print(f"Error exporting {agent}: {e}")

        with open(output_path, 'w') as f:
            json.dump(all_specs, f, indent=2)

        return output_path


# Model selection helper
class ModelSelector:
    """Select appropriate model based on agent requirements"""

    def __init__(self):
        """Initialize model selector"""
        self.model_mapping = {
            "haiku": [
                "keyword-researcher", "grammar-checker", "readability-scorer",
                "link-validator", "command-demonstrator", "solution-provider",
                "twitter-formatter", "linkedin-adapter", "instagram-packager",
                "metrics-collector"
            ],
            "sonnet": [
                "topic-scout", "source-gatherer", "competitor-analyzer",
                "fact-verifier", "angle-definer", "audience-profiler",
                "template-selector", "outline-builder", "intro-writer",
                "body-writer", "conclusion-writer", "quote-integrator",
                "code-example-writer", "api-documenter", "error-handler",
                "step-sequencer", "exercise-designer", "style-editor",
                "flow-optimizer", "ai-prompt-engineer", "chart-designer",
                "infographic-planner", "thumbnail-creator", "diagram-sketcher",
                "content-atomizer", "newsletter-curator", "trend-spotter"
            ],
            "opus": [
                "content-planner", "spec-writer", "concept-explainer",
                "improvement-advisor"
            ]
        }

        # Reverse mapping for quick lookup
        self.agent_to_model = {}
        for model, agents in self.model_mapping.items():
            for agent in agents:
                self.agent_to_model[agent] = model

    def get_model_for_agent(self, agent_name: str) -> str:
        """
        Return appropriate model for agent

        Args:
            agent_name: Name of the agent

        Returns:
            Model name (haiku, sonnet, or opus)
        """
        return self.agent_to_model.get(agent_name, "sonnet")

    def get_agents_for_model(self, model: str) -> List[str]:
        """Get all agents that use a specific model"""
        return self.model_mapping.get(model, [])


if __name__ == "__main__":
    # Test the specification loader
    print("Testing Agent Specification Loader...")

    # Create loader
    loader = AgentSpecLoader()

    # List available agents
    agents = loader.list_available_agents()
    print(f"\nFound {len(agents)} agent specifications")

    # Test loading a specification
    test_agent = "keyword-researcher"
    print(f"\nLoading specification for: {test_agent}")

    spec = loader.parse_agent_spec(test_agent)
    print(f"  Name: {spec.name}")
    print(f"  Model: {spec.model}")
    print(f"  Tools: {spec.tools}")
    print(f"  Description: {spec.description[:100]}...")

    # Validate specification
    is_valid, issues = loader.validate_spec(test_agent)
    print(f"  Valid: {is_valid}")
    if issues:
        print(f"  Issues: {issues}")

    # Test model selector
    print("\nTesting Model Selector...")
    selector = ModelSelector()

    for agent in ["keyword-researcher", "body-writer", "spec-writer"]:
        model = selector.get_model_for_agent(agent)
        print(f"  {agent}: {model}")

    # Export all specifications
    print("\nExporting all specifications...")
    export_path = loader.export_all_specs("test_agent_specs.json")
    print(f"  Exported to: {export_path}")