#!/usr/bin/env python3
"""
SubAgent Testing Harness - Test Orchestrator
Automated testing orchestration for the 41-agent pipeline
"""

import json
import time
import asyncio
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import sys

# Import local modules
from test_runner import SubAgentTestRunner, TestResult
from validator import SchemaValidator, OutputValidator, PipelineValidator, PerformanceValidator

@dataclass
class TestConfig:
    """Configuration for test execution"""
    parallel_execution: bool = True
    max_workers: int = 4
    timeout_per_agent: int = 30  # seconds
    retry_on_failure: bool = True
    max_retries: int = 2
    verbose: bool = True
    save_reports: bool = True
    test_mode: str = "comprehensive"  # quick, standard, comprehensive


class TestOrchestrator:
    """Orchestrate comprehensive testing of the entire pipeline"""

    def __init__(self, config: TestConfig = None):
        """Initialize test orchestrator"""
        self.config = config or TestConfig()
        self.base_path = Path(__file__).parent.parent

        # Initialize components
        self.test_runner = SubAgentTestRunner(str(self.base_path))
        self.output_validator = OutputValidator()
        self.pipeline_validator = PipelineValidator()
        self.performance_validator = PerformanceValidator()

        # Test execution tracking
        self.execution_log = []
        self.test_statistics = {
            "start_time": None,
            "end_time": None,
            "total_agents_tested": 0,
            "total_tests_run": 0,
            "phases_completed": [],
            "failed_agents": [],
            "performance_metrics": {}
        }

        # Agent registry (all 41 agents)
        self.all_agents = self._load_agent_registry()

    def _load_agent_registry(self) -> Dict[str, List[str]]:
        """Load complete agent registry by phase"""
        return {
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

    def run_all_tests(self) -> Dict:
        """
        Run comprehensive tests on all 41 agents

        Returns:
            Comprehensive test report
        """
        self.test_statistics["start_time"] = datetime.now()

        if self.config.verbose:
            print("\n" + "="*70)
            print(" SUBAGENT TESTING HARNESS - COMPREHENSIVE TEST RUN")
            print("="*70)
            print(f"Mode: {self.config.test_mode}")
            print(f"Parallel Execution: {self.config.parallel_execution}")
            print(f"Total Agents to Test: 41")
            print("-"*70)

        results = {}

        # Test each phase
        for phase, agents in self.all_agents.items():
            if self.config.verbose:
                print(f"\n▶ Testing Phase: {phase.upper()} ({len(agents)} agents)")
                print("-"*50)

            phase_results = self._test_phase(phase, agents)
            results[phase] = phase_results
            self.test_statistics["phases_completed"].append(phase)

            # Update statistics
            for agent_result in phase_results.values():
                if agent_result.get("status") == "failed":
                    self.test_statistics["failed_agents"].append(agent_result.get("agent"))

        self.test_statistics["end_time"] = datetime.now()

        # Generate final report
        final_report = self._generate_comprehensive_report(results)

        # Save report if configured
        if self.config.save_reports:
            self._save_report(final_report)

        # Print summary
        self._print_test_summary(final_report)

        return final_report

    def _test_phase(self, phase: str, agents: List[str]) -> Dict:
        """Test all agents in a phase"""
        phase_results = {}

        if self.config.parallel_execution and len(agents) > 1:
            # Parallel execution
            with ThreadPoolExecutor(max_workers=min(self.config.max_workers, len(agents))) as executor:
                future_to_agent = {
                    executor.submit(self._test_single_agent, agent): agent
                    for agent in agents
                }

                for future in as_completed(future_to_agent):
                    agent = future_to_agent[future]
                    try:
                        result = future.result(timeout=self.config.timeout_per_agent)
                        phase_results[agent] = result
                    except Exception as e:
                        phase_results[agent] = {
                            "agent": agent,
                            "status": "error",
                            "error": str(e)
                        }
                        if self.config.verbose:
                            print(f"  ✗ {agent}: ERROR - {e}")
        else:
            # Sequential execution
            for agent in agents:
                phase_results[agent] = self._test_single_agent(agent)

        return phase_results

    def _test_single_agent(self, agent_name: str) -> Dict:
        """Test a single agent with all fixtures"""
        agent_report = {
            "agent": agent_name,
            "status": "pending",
            "tests_run": 0,
            "tests_passed": 0,
            "tests_failed": 0,
            "execution_time": 0,
            "test_details": []
        }

        start_time = time.time()

        try:
            # Run tests using test runner
            test_results = self.test_runner.test_individual_agent(agent_name)

            # Process results
            for result in test_results:
                agent_report["tests_run"] += 1

                if result.status == "pass":
                    agent_report["tests_passed"] += 1
                else:
                    agent_report["tests_failed"] += 1

                    # Retry if configured
                    if self.config.retry_on_failure:
                        retry_result = self._retry_test(agent_name, result)
                        if retry_result and retry_result.status == "pass":
                            agent_report["tests_passed"] += 1
                            agent_report["tests_failed"] -= 1
                            result = retry_result

                # Validate output quality
                if result.actual_output:
                    quality_valid, quality_report = self.output_validator.validate_output(
                        agent_name,
                        result.actual_output
                    )

                    agent_report["test_details"].append({
                        "test_name": result.test_name,
                        "status": result.status,
                        "quality_score": quality_report.get("score", 0),
                        "execution_time": result.execution_time
                    })

            # Update statistics
            self.test_statistics["total_agents_tested"] += 1
            self.test_statistics["total_tests_run"] += agent_report["tests_run"]

            # Determine overall status
            if agent_report["tests_failed"] == 0:
                agent_report["status"] = "passed"
                status_symbol = "✓"
            else:
                agent_report["status"] = "failed"
                status_symbol = "✗"

            agent_report["execution_time"] = time.time() - start_time

            # Log execution
            self.execution_log.append({
                "timestamp": datetime.now().isoformat(),
                "phase": self._get_phase_for_agent(agent_name),
                "agent": agent_name,
                "status": agent_report["status"],
                "tests": f"{agent_report['tests_passed']}/{agent_report['tests_run']}"
            })

            if self.config.verbose:
                print(f"  {status_symbol} {agent_name}: {agent_report['tests_passed']}/{agent_report['tests_run']} tests passed ({agent_report['execution_time']:.2f}s)")

        except Exception as e:
            agent_report["status"] = "error"
            agent_report["error"] = str(e)
            if self.config.verbose:
                print(f"  ✗ {agent_name}: ERROR - {e}")

        return agent_report

    def _retry_test(self, agent_name: str, failed_result: TestResult) -> Optional[TestResult]:
        """Retry a failed test"""
        for attempt in range(self.config.max_retries):
            if self.config.verbose:
                print(f"    ↻ Retrying {agent_name}:{failed_result.test_name} (attempt {attempt + 1})")

            # Re-run the specific test
            retry_results = self.test_runner.test_individual_agent(
                agent_name,
                failed_result.test_name
            )

            if retry_results and retry_results[0].status == "pass":
                return retry_results[0]

        return None

    def _get_phase_for_agent(self, agent_name: str) -> str:
        """Get the phase an agent belongs to"""
        for phase, agents in self.all_agents.items():
            if agent_name in agents:
                return phase
        return "unknown"

    def test_workflow(self, workflow_type: str) -> Dict:
        """
        Test a specific workflow (quick-news, blog-post, tutorial)

        Args:
            workflow_type: Type of workflow to test

        Returns:
            Workflow test report
        """
        if self.config.verbose:
            print(f"\n▶ Testing Workflow: {workflow_type}")

        workflow_report = {
            "workflow": workflow_type,
            "status": "pending",
            "phases_tested": [],
            "pipeline_validation": {},
            "performance_validation": {},
            "results": {}
        }

        # Run workflow test
        test_results = self.test_runner.test_full_pipeline(workflow_type)

        # Validate pipeline flow
        is_valid, pipeline_report = self.pipeline_validator.validate_pipeline_flow(
            self.execution_log
        )
        workflow_report["pipeline_validation"] = pipeline_report

        # Validate performance
        performance_metrics = {
            "execution_time": sum(r.execution_time for r in test_results),
            "total_tokens": sum(r.tokens_used for r in test_results),
            "success_rate": len([r for r in test_results if r.status == "pass"]) / max(1, len(test_results))
        }

        meets_benchmarks, perf_report = self.performance_validator.validate_performance(
            performance_metrics
        )
        workflow_report["performance_validation"] = perf_report

        # Determine overall status
        if is_valid and meets_benchmarks:
            workflow_report["status"] = "passed"
        else:
            workflow_report["status"] = "failed"

        return workflow_report

    def run_regression_suite(self) -> Dict:
        """Run regression tests on critical agents"""
        critical_agents = [
            "spec-writer",
            "body-writer",
            "grammar-checker",
            "content-atomizer"
        ]

        if self.config.verbose:
            print("\n▶ Running Regression Suite")
            print(f"  Testing {len(critical_agents)} critical agents")

        regression_results = {}

        for agent in critical_agents:
            result = self._test_single_agent(agent)
            regression_results[agent] = result

        return regression_results

    def benchmark_performance(self) -> Dict:
        """Run performance benchmarks"""
        benchmark_report = {
            "timestamp": datetime.now().isoformat(),
            "agent_benchmarks": {},
            "phase_benchmarks": {},
            "overall_metrics": {}
        }

        if self.config.verbose:
            print("\n▶ Running Performance Benchmarks")

        # Benchmark each agent
        sample_agents = ["keyword-researcher", "body-writer", "grammar-checker"]

        for agent in sample_agents:
            start = time.time()
            result = self._test_single_agent(agent)
            execution_time = time.time() - start

            benchmark_report["agent_benchmarks"][agent] = {
                "execution_time": execution_time,
                "tests_run": result.get("tests_run", 0),
                "avg_time_per_test": execution_time / max(1, result.get("tests_run", 1))
            }

        # Calculate overall metrics
        total_time = sum(b["execution_time"] for b in benchmark_report["agent_benchmarks"].values())
        total_tests = sum(b["tests_run"] for b in benchmark_report["agent_benchmarks"].values())

        benchmark_report["overall_metrics"] = {
            "total_execution_time": total_time,
            "total_tests": total_tests,
            "avg_time_per_test": total_time / max(1, total_tests),
            "estimated_full_suite_time": (total_time / len(sample_agents)) * 41
        }

        return benchmark_report

    def _generate_comprehensive_report(self, results: Dict) -> Dict:
        """Generate comprehensive test report"""
        total_agents = sum(len(agents) for agents in self.all_agents.values())
        total_passed = 0
        total_failed = 0

        for phase_results in results.values():
            for agent_result in phase_results.values():
                if agent_result.get("status") == "passed":
                    total_passed += 1
                else:
                    total_failed += 1

        execution_time = (
            self.test_statistics["end_time"] - self.test_statistics["start_time"]
        ).total_seconds() if self.test_statistics["end_time"] else 0

        report = {
            "test_run": {
                "timestamp": self.test_statistics["start_time"].isoformat() if self.test_statistics["start_time"] else None,
                "mode": self.config.test_mode,
                "execution_time": execution_time,
                "parallel_execution": self.config.parallel_execution
            },
            "summary": {
                "total_agents": total_agents,
                "agents_tested": self.test_statistics["total_agents_tested"],
                "agents_passed": total_passed,
                "agents_failed": total_failed,
                "total_tests_run": self.test_statistics["total_tests_run"],
                "success_rate": (total_passed / max(1, total_agents)) * 100,
                "phases_completed": self.test_statistics["phases_completed"]
            },
            "phase_results": results,
            "failed_agents": self.test_statistics["failed_agents"],
            "execution_log": self.execution_log[-100:],  # Last 100 entries
            "recommendations": self._generate_recommendations(results)
        }

        return report

    def _generate_recommendations(self, results: Dict) -> List[str]:
        """Generate recommendations based on test results"""
        recommendations = []

        # Check for consistently failing agents
        failing_agents = []
        for phase_results in results.values():
            for agent, result in phase_results.items():
                if result.get("status") == "failed":
                    failing_agents.append(agent)

        if failing_agents:
            recommendations.append(f"Review and fix failing agents: {', '.join(failing_agents[:5])}")

        # Check for performance issues
        slow_agents = []
        for phase_results in results.values():
            for agent, result in phase_results.items():
                if result.get("execution_time", 0) > 10:
                    slow_agents.append(agent)

        if slow_agents:
            recommendations.append(f"Optimize slow agents: {', '.join(slow_agents[:3])}")

        # Check test coverage
        untested = set(sum(self.all_agents.values(), [])) - set(self.test_statistics.get("total_agents_tested", []))
        if untested:
            recommendations.append(f"Add test fixtures for: {', '.join(list(untested)[:5])}")

        if not recommendations:
            recommendations.append("All systems operational. Continue monitoring performance.")

        return recommendations

    def _save_report(self, report: Dict):
        """Save test report to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"test_report_{timestamp}.json"
        filepath = self.base_path / "reports" / filename

        filepath.parent.mkdir(exist_ok=True)

        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2, default=str)

        if self.config.verbose:
            print(f"\n📄 Report saved to: {filepath}")

    def _print_test_summary(self, report: Dict):
        """Print test summary to console"""
        summary = report["summary"]

        print("\n" + "="*70)
        print(" TEST EXECUTION COMPLETE")
        print("="*70)
        print(f"Total Agents Tested: {summary['agents_tested']}/{summary['total_agents']}")
        print(f"Agents Passed: {summary['agents_passed']} ✓")
        print(f"Agents Failed: {summary['agents_failed']} ✗")
        print(f"Total Tests Run: {summary['total_tests_run']}")
        print(f"Success Rate: {summary['success_rate']:.1f}%")
        print(f"Execution Time: {report['test_run']['execution_time']:.2f}s")

        if report["failed_agents"]:
            print("\n⚠ Failed Agents:")
            for agent in report["failed_agents"][:10]:
                print(f"  - {agent}")

        print("\n📋 Recommendations:")
        for i, rec in enumerate(report["recommendations"][:5], 1):
            print(f"  {i}. {rec}")

        print("="*70)


def main():
    """Main execution function"""
    import argparse

    parser = argparse.ArgumentParser(description="SubAgent Testing Harness")
    parser.add_argument("--mode", choices=["quick", "standard", "comprehensive"],
                       default="standard", help="Test mode")
    parser.add_argument("--parallel", action="store_true", help="Enable parallel execution")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--workflow", help="Test specific workflow")
    parser.add_argument("--regression", action="store_true", help="Run regression suite")
    parser.add_argument("--benchmark", action="store_true", help="Run performance benchmarks")

    args = parser.parse_args()

    # Configure test orchestrator
    config = TestConfig(
        test_mode=args.mode,
        parallel_execution=args.parallel,
        verbose=args.verbose or True,
        save_reports=True
    )

    orchestrator = TestOrchestrator(config)

    # Run appropriate tests
    if args.regression:
        print("Running regression suite...")
        orchestrator.run_regression_suite()
    elif args.benchmark:
        print("Running performance benchmarks...")
        report = orchestrator.benchmark_performance()
        print(json.dumps(report, indent=2, default=str))
    elif args.workflow:
        print(f"Testing workflow: {args.workflow}")
        orchestrator.test_workflow(args.workflow)
    else:
        # Run comprehensive tests
        orchestrator.run_all_tests()


if __name__ == "__main__":
    main()