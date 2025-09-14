#!/usr/bin/env python3
"""
SubAgent Testing Harness - Fixtures Loader
Comprehensive fixture management for all 41 agents
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

class FixturesLoader:
    """Load and manage test fixtures for all pipeline agents"""

    def __init__(self, base_path: str = None):
        """Initialize fixtures loader"""
        self.base_path = Path(base_path or os.path.dirname(__file__)).parent
        self.fixtures_dir = self.base_path / "data" / "fixtures"

        # Agent to phase mapping
        self.agent_phases = {
            # Research & Discovery
            "topic-scout": "research",
            "source-gatherer": "research",
            "competitor-analyzer": "research",
            "fact-verifier": "research",
            "keyword-researcher": "research",

            # Strategy & Planning
            "content-planner": "strategy",
            "angle-definer": "strategy",
            "audience-profiler": "strategy",
            "spec-writer": "strategy",
            "template-selector": "strategy",

            # Content Creation
            "outline-builder": "content",
            "intro-writer": "content",
            "body-writer": "content",
            "conclusion-writer": "content",
            "quote-integrator": "content",

            # Technical Content
            "code-example-writer": "technical",
            "api-documenter": "technical",
            "command-demonstrator": "technical",
            "error-handler": "technical",

            # Tutorial Creation
            "step-sequencer": "tutorial",
            "exercise-designer": "tutorial",
            "solution-provider": "tutorial",
            "concept-explainer": "tutorial",

            # Quality Assurance
            "grammar-checker": "qa",
            "style-editor": "qa",
            "flow-optimizer": "qa",
            "readability-scorer": "qa",
            "link-validator": "qa",

            # Visual Creation
            "ai-prompt-engineer": "visual",
            "chart-designer": "visual",
            "infographic-planner": "visual",
            "thumbnail-creator": "visual",
            "diagram-sketcher": "visual",

            # Distribution
            "content-atomizer": "distribution",
            "twitter-formatter": "distribution",
            "linkedin-adapter": "distribution",
            "instagram-packager": "distribution",
            "newsletter-curator": "distribution",

            # Performance Analysis
            "metrics-collector": "performance",
            "trend-spotter": "performance",
            "improvement-advisor": "performance"
        }

        # Load all fixtures
        self.all_fixtures = self._load_all_fixtures()

    def _load_all_fixtures(self) -> Dict[str, List[Dict]]:
        """Load all fixtures from various sources"""
        all_fixtures = {}

        # Load main test_fixtures.json
        main_fixtures_path = self.base_path / "data" / "test_fixtures.json"
        if main_fixtures_path.exists():
            with open(main_fixtures_path, 'r') as f:
                data = json.load(f)
                if "fixtures" in data:
                    all_fixtures.update(data["fixtures"])

        # Load phase-specific fixtures
        phase_files = [
            "research_phase_fixtures.json",
            "strategy_phase_fixtures.json",
            "content_phase_fixtures.json",
            "all_phase_fixtures.json"
        ]

        for phase_file in phase_files:
            phase_path = self.fixtures_dir / phase_file
            if phase_path.exists():
                with open(phase_path, 'r') as f:
                    data = json.load(f)

                    # Handle nested phase structure
                    for key, value in data.items():
                        if isinstance(value, dict):
                            # This is a phase grouping
                            for agent_name, agent_fixtures in value.items():
                                if agent_name not in all_fixtures:
                                    all_fixtures[agent_name] = []
                                all_fixtures[agent_name].extend(agent_fixtures)
                        elif isinstance(value, list):
                            # Direct agent fixtures
                            if key not in all_fixtures:
                                all_fixtures[key] = []
                            all_fixtures[key].extend(value)

        return all_fixtures

    def get_fixtures_for_agent(self, agent_name: str) -> List[Dict]:
        """Get all fixtures for a specific agent"""
        return self.all_fixtures.get(agent_name, [])

    def get_fixtures_for_phase(self, phase: str) -> Dict[str, List[Dict]]:
        """Get all fixtures for agents in a specific phase"""
        phase_fixtures = {}

        for agent, agent_phase in self.agent_phases.items():
            if agent_phase == phase:
                fixtures = self.get_fixtures_for_agent(agent)
                if fixtures:
                    phase_fixtures[agent] = fixtures

        return phase_fixtures

    def get_fixture_by_name(self, agent_name: str, test_name: str) -> Optional[Dict]:
        """Get a specific fixture by agent and test name"""
        agent_fixtures = self.get_fixtures_for_agent(agent_name)

        for fixture in agent_fixtures:
            if fixture.get("test_name") == test_name:
                return fixture

        return None

    def get_coverage_report(self) -> Dict:
        """Generate coverage report for all agents"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "total_agents": len(self.agent_phases),
            "agents_with_fixtures": 0,
            "agents_without_fixtures": 0,
            "total_test_cases": 0,
            "coverage_by_phase": {},
            "missing_fixtures": [],
            "fixture_counts": {}
        }

        # Calculate coverage by phase
        for phase in set(self.agent_phases.values()):
            phase_agents = [a for a, p in self.agent_phases.items() if p == phase]
            phase_with_fixtures = 0
            phase_test_count = 0

            for agent in phase_agents:
                fixtures = self.get_fixtures_for_agent(agent)
                if fixtures:
                    phase_with_fixtures += 1
                    phase_test_count += len(fixtures)
                    report["fixture_counts"][agent] = len(fixtures)
                else:
                    report["missing_fixtures"].append(agent)

            report["coverage_by_phase"][phase] = {
                "total_agents": len(phase_agents),
                "agents_with_fixtures": phase_with_fixtures,
                "coverage_percentage": (phase_with_fixtures / len(phase_agents)) * 100 if phase_agents else 0,
                "total_test_cases": phase_test_count
            }

        # Calculate totals
        report["agents_with_fixtures"] = len(self.all_fixtures)
        report["agents_without_fixtures"] = len(self.agent_phases) - len(self.all_fixtures)
        report["total_test_cases"] = sum(len(fixtures) for fixtures in self.all_fixtures.values())
        report["overall_coverage"] = (report["agents_with_fixtures"] / report["total_agents"]) * 100

        return report

    def validate_fixtures(self) -> Dict:
        """Validate all fixtures have required fields"""
        validation_report = {
            "valid_fixtures": 0,
            "invalid_fixtures": 0,
            "errors": []
        }

        required_fields = ["test_name", "input", "expected_output"]

        for agent_name, fixtures in self.all_fixtures.items():
            for i, fixture in enumerate(fixtures):
                is_valid = True

                for field in required_fields:
                    if field not in fixture:
                        is_valid = False
                        validation_report["errors"].append({
                            "agent": agent_name,
                            "fixture_index": i,
                            "missing_field": field
                        })

                if is_valid:
                    validation_report["valid_fixtures"] += 1
                else:
                    validation_report["invalid_fixtures"] += 1

        return validation_report

    def generate_fixture_template(self, agent_name: str) -> Dict:
        """Generate a fixture template for an agent"""
        phase = self.agent_phases.get(agent_name, "unknown")

        template = {
            "test_name": f"{agent_name}_test_case",
            "input": {
                "TODO": "Add input fields based on agent requirements"
            },
            "expected_output": {
                "TODO": "Add expected output structure"
            },
            "metadata": {
                "agent": agent_name,
                "phase": phase,
                "created": datetime.now().isoformat()
            }
        }

        return template

    def export_fixtures(self, output_path: str = None):
        """Export all fixtures to a consolidated file"""
        if not output_path:
            output_path = self.base_path / "data" / "consolidated_fixtures.json"

        export_data = {
            "metadata": {
                "generated": datetime.now().isoformat(),
                "total_agents": len(self.agent_phases),
                "total_fixtures": sum(len(f) for f in self.all_fixtures.values())
            },
            "fixtures_by_agent": self.all_fixtures,
            "fixtures_by_phase": {}
        }

        # Organize by phase
        for phase in set(self.agent_phases.values()):
            export_data["fixtures_by_phase"][phase] = self.get_fixtures_for_phase(phase)

        with open(output_path, 'w') as f:
            json.dump(export_data, f, indent=2)

        return output_path

    def print_coverage_summary(self):
        """Print a summary of fixture coverage"""
        report = self.get_coverage_report()

        print("\n" + "="*60)
        print("FIXTURE COVERAGE REPORT")
        print("="*60)
        print(f"Total Agents: {report['total_agents']}")
        print(f"Agents with Fixtures: {report['agents_with_fixtures']}")
        print(f"Overall Coverage: {report['overall_coverage']:.1f}%")
        print(f"Total Test Cases: {report['total_test_cases']}")

        print("\nCoverage by Phase:")
        for phase, stats in report['coverage_by_phase'].items():
            print(f"  {phase.capitalize():12} {stats['agents_with_fixtures']}/{stats['total_agents']} agents "
                  f"({stats['coverage_percentage']:.0f}%) - {stats['total_test_cases']} tests")

        if report['missing_fixtures']:
            print(f"\nAgents Missing Fixtures ({len(report['missing_fixtures'])}):")
            for agent in report['missing_fixtures'][:10]:
                print(f"  - {agent}")
            if len(report['missing_fixtures']) > 10:
                print(f"  ... and {len(report['missing_fixtures']) - 10} more")

        print("="*60)


# Utility functions
def create_fixture_for_agent(agent_name: str, test_cases: List[Dict]) -> Dict:
    """Create fixtures for a specific agent"""
    return {
        agent_name: test_cases
    }


def merge_fixtures(*fixture_dicts) -> Dict:
    """Merge multiple fixture dictionaries"""
    merged = {}
    for fixtures in fixture_dicts:
        for agent, cases in fixtures.items():
            if agent not in merged:
                merged[agent] = []
            merged[agent].extend(cases)
    return merged


if __name__ == "__main__":
    # Test the fixtures loader
    loader = FixturesLoader()

    # Print coverage summary
    loader.print_coverage_summary()

    # Validate fixtures
    validation = loader.validate_fixtures()
    print(f"\nValidation: {validation['valid_fixtures']} valid, "
          f"{validation['invalid_fixtures']} invalid fixtures")

    # Export consolidated fixtures
    export_path = loader.export_fixtures()
    print(f"\nExported fixtures to: {export_path}")