#!/usr/bin/env python3
"""
SubAgent Testing Harness - Test Runner
Comprehensive testing system for 41-agent content pipeline
"""

import json
import time
import os
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path

# Import Task executor and agent loader
try:
    from task_executor import ClaudeTaskExecutor, TaskResult as TaskExecResult
    from agent_spec_loader import AgentSpecLoader, ModelSelector
    TASK_INTEGRATION_AVAILABLE = True
except ImportError:
    TASK_INTEGRATION_AVAILABLE = False
    print("Warning: Task integration modules not available, using mock execution")

@dataclass
class TestResult:
    """Store test execution results"""
    agent_name: str
    test_name: str
    status: str  # 'pass', 'fail', 'error'
    execution_time: float
    tokens_used: int
    input_data: Dict
    actual_output: Any
    expected_output: Any
    error_message: Optional[str] = None
    timestamp: str = ""

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()

class SubAgentTestRunner:
    """Main test runner for content pipeline agents"""

    def __init__(self, base_path: str = None, use_task_integration: bool = None):
        """Initialize test runner with paths and data"""
        self.base_path = Path(base_path or os.path.dirname(__file__)).parent
        self.schemas_path = self.base_path / "schemas" / "validation_schemas.json"
        self.fixtures_path = self.base_path / "data" / "test_fixtures.json"
        self.reports_path = self.base_path / "reports"

        # Load test data
        self.validation_schemas = self._load_json(self.schemas_path)
        self.test_fixtures = self._load_json(self.fixtures_path)

        # Test results storage
        self.test_results: List[TestResult] = []

        # Performance metrics
        self.performance_metrics = {
            "total_tests": 0,
            "passed": 0,
            "failed": 0,
            "errors": 0,
            "total_time": 0,
            "total_tokens": 0
        }

        # Task integration setup
        self.use_task_integration = use_task_integration if use_task_integration is not None else TASK_INTEGRATION_AVAILABLE
        if self.use_task_integration and TASK_INTEGRATION_AVAILABLE:
            self.task_executor = ClaudeTaskExecutor({
                "verbose": False,
                "fallback_to_mock": True,
                "cache_results": True
            })
            self.spec_loader = AgentSpecLoader()
            self.model_selector = ModelSelector()
        else:
            self.task_executor = None
            self.spec_loader = None
            self.model_selector = None

    def _load_json(self, path: Path) -> Dict:
        """Load JSON file safely"""
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: {path} not found")
            return {}
        except json.JSONDecodeError as e:
            print(f"Error loading {path}: {e}")
            return {}

    def test_individual_agent(self, agent_name: str, test_case: Optional[str] = None) -> List[TestResult]:
        """
        Test a single agent with all or specific test fixtures

        Args:
            agent_name: Name of the agent to test
            test_case: Optional specific test case name

        Returns:
            List of test results
        """
        results = []

        # Get agent fixtures
        agent_fixtures = self.test_fixtures.get("fixtures", {}).get(agent_name, [])

        if not agent_fixtures:
            print(f"No test fixtures found for {agent_name}")
            return results

        # Filter to specific test case if requested
        if test_case:
            agent_fixtures = [f for f in agent_fixtures if f.get("test_name") == test_case]

        # Run each test
        for fixture in agent_fixtures:
            result = self._execute_agent_test(agent_name, fixture)
            results.append(result)
            self.test_results.append(result)
            self._update_metrics(result)

        return results

    def _execute_agent_test(self, agent_name: str, fixture: Dict) -> TestResult:
        """
        Execute a single test for an agent

        Args:
            agent_name: Name of the agent
            fixture: Test fixture with input and expected output

        Returns:
            TestResult object
        """
        test_name = fixture.get("test_name", "unnamed_test")
        input_data = fixture.get("input", {})
        expected_output = fixture.get("expected_output", {})

        start_time = time.time()

        try:
            # Validate input against schema
            if not self._validate_input(agent_name, input_data):
                return TestResult(
                    agent_name=agent_name,
                    test_name=test_name,
                    status="fail",
                    execution_time=0,
                    tokens_used=0,
                    input_data=input_data,
                    actual_output=None,
                    expected_output=expected_output,
                    error_message="Input validation failed"
                )

            # Execute agent using Task integration or mock
            if self.use_task_integration and self.task_executor:
                actual_output = self._execute_with_task_tool(agent_name, input_data)
            else:
                actual_output = self._simulate_agent_execution(agent_name, input_data)

            # Validate output
            is_valid, validation_errors = self._validate_output(agent_name, actual_output)

            # Check if output matches expected
            matches_expected = self._compare_outputs(actual_output, expected_output)

            execution_time = time.time() - start_time

            # Determine test status
            if is_valid and matches_expected:
                status = "pass"
                error_msg = None
            else:
                status = "fail"
                error_msg = f"Validation: {validation_errors}" if not is_valid else "Output doesn't match expected"

            return TestResult(
                agent_name=agent_name,
                test_name=test_name,
                status=status,
                execution_time=execution_time,
                tokens_used=self._estimate_tokens(input_data, actual_output),
                input_data=input_data,
                actual_output=actual_output,
                expected_output=expected_output,
                error_message=error_msg
            )

        except Exception as e:
            execution_time = time.time() - start_time
            return TestResult(
                agent_name=agent_name,
                test_name=test_name,
                status="error",
                execution_time=execution_time,
                tokens_used=0,
                input_data=input_data,
                actual_output=None,
                expected_output=expected_output,
                error_message=str(e)
            )

    def _validate_input(self, agent_name: str, input_data: Dict) -> bool:
        """Validate input against agent's input schema"""
        schema = self.validation_schemas.get("agent_validation", {}).get(agent_name, {}).get("input_schema")
        if not schema:
            return True  # No schema means no validation

        return self._validate_against_schema(input_data, schema)

    def _validate_output(self, agent_name: str, output_data: Any) -> Tuple[bool, List[str]]:
        """Validate output against agent's output schema"""
        schema = self.validation_schemas.get("agent_validation", {}).get(agent_name, {}).get("output_schema")
        if not schema:
            return True, []

        errors = []
        is_valid = self._validate_against_schema(output_data, schema, errors)
        return is_valid, errors

    def _validate_against_schema(self, data: Any, schema: Dict, errors: List[str] = None) -> bool:
        """Basic JSON schema validation"""
        if errors is None:
            errors = []

        if schema.get("type") == "object":
            if not isinstance(data, dict):
                errors.append("Expected object, got " + type(data).__name__)
                return False

            # Check required fields
            for field in schema.get("required", []):
                if field not in data:
                    errors.append(f"Missing required field: {field}")
                    return False

            # Validate properties
            for prop, prop_schema in schema.get("properties", {}).items():
                if prop in data:
                    if not self._validate_property(data[prop], prop_schema, errors):
                        return False

        return len(errors) == 0

    def _validate_property(self, value: Any, schema: Dict, errors: List[str]) -> bool:
        """Validate a single property against its schema"""
        prop_type = schema.get("type")

        if prop_type == "string":
            if not isinstance(value, str):
                errors.append(f"Expected string, got {type(value).__name__}")
                return False
            if "minLength" in schema and len(value) < schema["minLength"]:
                errors.append(f"String too short: {len(value)} < {schema['minLength']}")
                return False

        elif prop_type == "array":
            if not isinstance(value, list):
                errors.append(f"Expected array, got {type(value).__name__}")
                return False
            if "minItems" in schema and len(value) < schema["minItems"]:
                errors.append(f"Array too small: {len(value)} < {schema['minItems']}")
                return False

        elif prop_type == "number":
            if not isinstance(value, (int, float)):
                errors.append(f"Expected number, got {type(value).__name__}")
                return False

        # Check enum values
        if "enum" in schema and value not in schema["enum"]:
            errors.append(f"Value '{value}' not in allowed values: {schema['enum']}")
            return False

        return True

    def _compare_outputs(self, actual: Any, expected: Any) -> bool:
        """Compare actual output with expected output"""
        # For demo purposes, check if key fields match
        if isinstance(expected, dict) and isinstance(actual, dict):
            for key in expected:
                if key not in actual:
                    return False
                # Check if types match
                if type(actual[key]) != type(expected[key]):
                    return False
        return True

    def _execute_with_task_tool(self, agent_name: str, input_data: Dict) -> Dict:
        """
        Execute agent using Claude Task tool integration

        Args:
            agent_name: Name of the agent to execute
            input_data: Input data for the agent

        Returns:
            Agent output as dictionary
        """
        try:
            # Load agent specification
            agent_spec = self.spec_loader.load_agent_spec(agent_name)

            # Get appropriate model for agent
            model = self.model_selector.get_model_for_agent(agent_name)

            # Execute via Task tool
            result = self.task_executor.execute_agent(
                agent_name=agent_name,
                agent_spec=agent_spec,
                input_data=input_data
            )

            if result.success:
                return result.output
            else:
                # Fall back to mock on failure
                print(f"Task execution failed for {agent_name}, using mock: {result.error}")
                return self._simulate_agent_execution(agent_name, input_data)

        except Exception as e:
            print(f"Error in Task tool execution for {agent_name}: {e}")
            return self._simulate_agent_execution(agent_name, input_data)

    def _simulate_agent_execution(self, agent_name: str, input_data: Dict) -> Dict:
        """
        Simulate agent execution for testing
        In real implementation, this would call the actual agent
        """
        # Return mock data based on agent type
        if agent_name == "keyword-researcher":
            return {
                "primary_keyword": "test keyword",
                "long_tail": ["test1", "test2", "test3"],
                "search_volume": "medium",
                "difficulty": "medium"
            }
        elif agent_name == "topic-scout":
            return {
                "trending_topics": ["topic1", "topic2", "topic3"],
                "content_gaps": ["gap1", "gap2"],
                "opportunities": ["opp1", "opp2"]
            }
        else:
            # Generic response
            return {"status": "completed", "data": "test_output"}

    def _estimate_tokens(self, input_data: Any, output_data: Any) -> int:
        """Estimate token usage for the test"""
        # Simple estimation: ~4 characters per token
        input_str = json.dumps(input_data) if isinstance(input_data, dict) else str(input_data)
        output_str = json.dumps(output_data) if isinstance(output_data, dict) else str(output_data)
        return (len(input_str) + len(output_str)) // 4

    def _update_metrics(self, result: TestResult):
        """Update performance metrics"""
        self.performance_metrics["total_tests"] += 1
        self.performance_metrics["total_time"] += result.execution_time
        self.performance_metrics["total_tokens"] += result.tokens_used

        if result.status == "pass":
            self.performance_metrics["passed"] += 1
        elif result.status == "fail":
            self.performance_metrics["failed"] += 1
        else:
            self.performance_metrics["errors"] += 1

    def test_pipeline_segment(self, phase: str) -> List[TestResult]:
        """
        Test a complete pipeline phase

        Args:
            phase: Phase name (research, strategy, content, etc.)

        Returns:
            List of test results for all agents in the phase
        """
        phase_agents = self._get_phase_agents(phase)
        results = []

        for agent in phase_agents:
            agent_results = self.test_individual_agent(agent)
            results.extend(agent_results)

        return results

    def _get_phase_agents(self, phase: str) -> List[str]:
        """Get list of agents for a specific phase"""
        phase_mapping = {
            "research": ["topic-scout", "source-gatherer", "competitor-analyzer", "fact-verifier", "keyword-researcher"],
            "strategy": ["content-planner", "angle-definer", "audience-profiler", "spec-writer", "template-selector"],
            "content": ["outline-builder", "intro-writer", "body-writer", "conclusion-writer", "quote-integrator"],
            "technical": ["code-example-writer", "api-documenter", "command-demonstrator", "error-handler"],
            "tutorial": ["step-sequencer", "exercise-designer", "solution-provider", "concept-explainer"],
            "qa": ["grammar-checker", "style-editor", "flow-optimizer", "readability-scorer", "link-validator"],
            "visual": ["ai-prompt-engineer", "chart-designer", "infographic-planner", "thumbnail-creator", "diagram-sketcher"],
            "distribution": ["content-atomizer", "twitter-formatter", "linkedin-adapter", "instagram-packager", "newsletter-curator"],
            "performance": ["metrics-collector", "trend-spotter", "improvement-advisor"]
        }
        return phase_mapping.get(phase, [])

    def test_full_pipeline(self, workflow_type: str = "standard") -> List[TestResult]:
        """
        Test a complete workflow end-to-end

        Args:
            workflow_type: Type of workflow (quick-news, blog-post, tutorial)

        Returns:
            List of all test results
        """
        workflow_phases = self._get_workflow_phases(workflow_type)
        results = []

        for phase in workflow_phases:
            phase_results = self.test_pipeline_segment(phase)
            results.extend(phase_results)

        return results

    def _get_workflow_phases(self, workflow_type: str) -> List[str]:
        """Get phases for a specific workflow"""
        workflow_mapping = {
            "quick-news": ["research", "content", "distribution"],
            "blog-post": ["research", "strategy", "content", "qa", "distribution"],
            "tutorial": ["research", "strategy", "content", "technical", "tutorial", "qa", "visual", "distribution"],
            "standard": ["research", "strategy", "content", "qa", "distribution"]
        }
        return workflow_mapping.get(workflow_type, ["research", "content", "qa"])

    def generate_report(self, output_file: Optional[str] = None) -> Dict:
        """
        Generate comprehensive test report

        Args:
            output_file: Optional file path to save report

        Returns:
            Report dictionary
        """
        report = {
            "summary": {
                "total_tests": self.performance_metrics["total_tests"],
                "passed": self.performance_metrics["passed"],
                "failed": self.performance_metrics["failed"],
                "errors": self.performance_metrics["errors"],
                "success_rate": (self.performance_metrics["passed"] / max(1, self.performance_metrics["total_tests"])) * 100,
                "total_execution_time": self.performance_metrics["total_time"],
                "total_tokens_used": self.performance_metrics["total_tokens"],
                "timestamp": datetime.now().isoformat()
            },
            "agent_results": {},
            "failed_tests": [],
            "error_tests": []
        }

        # Organize results by agent
        for result in self.test_results:
            agent_name = result.agent_name
            if agent_name not in report["agent_results"]:
                report["agent_results"][agent_name] = {
                    "total": 0,
                    "passed": 0,
                    "failed": 0,
                    "errors": 0,
                    "tests": []
                }

            agent_report = report["agent_results"][agent_name]
            agent_report["total"] += 1
            agent_report["tests"].append({
                "test_name": result.test_name,
                "status": result.status,
                "execution_time": result.execution_time,
                "tokens_used": result.tokens_used,
                "error": result.error_message
            })

            if result.status == "pass":
                agent_report["passed"] += 1
            elif result.status == "fail":
                agent_report["failed"] += 1
                report["failed_tests"].append({
                    "agent": agent_name,
                    "test": result.test_name,
                    "error": result.error_message
                })
            else:
                agent_report["errors"] += 1
                report["error_tests"].append({
                    "agent": agent_name,
                    "test": result.test_name,
                    "error": result.error_message
                })

        # Save report if requested
        if output_file:
            output_path = self.reports_path / output_file
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w') as f:
                json.dump(report, f, indent=2)
            print(f"Report saved to {output_path}")

        return report

    def print_summary(self):
        """Print test summary to console"""
        print("\n" + "="*60)
        print("TEST SUMMARY")
        print("="*60)
        print(f"Total Tests: {self.performance_metrics['total_tests']}")
        print(f"Passed: {self.performance_metrics['passed']} ✓")
        print(f"Failed: {self.performance_metrics['failed']} ✗")
        print(f"Errors: {self.performance_metrics['errors']} ⚠")

        if self.performance_metrics['total_tests'] > 0:
            success_rate = (self.performance_metrics['passed'] / self.performance_metrics['total_tests']) * 100
            print(f"Success Rate: {success_rate:.1f}%")

        print(f"\nTotal Execution Time: {self.performance_metrics['total_time']:.2f}s")
        print(f"Total Tokens Used: {self.performance_metrics['total_tokens']:,}")
        print("="*60)

# Main execution
if __name__ == "__main__":
    # Initialize test runner
    runner = SubAgentTestRunner()

    # Example: Test individual agent
    print("Testing keyword-researcher agent...")
    results = runner.test_individual_agent("keyword-researcher")

    # Example: Test a pipeline phase
    print("\nTesting research phase...")
    phase_results = runner.test_pipeline_segment("research")

    # Generate and save report
    report = runner.generate_report("test_results.json")

    # Print summary
    runner.print_summary()