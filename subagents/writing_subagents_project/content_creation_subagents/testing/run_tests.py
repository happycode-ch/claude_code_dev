#!/usr/bin/env python3
"""
SubAgent Testing Harness - Main Test Execution Script
Run comprehensive tests on the 41-agent pipeline
"""

import sys
import os
import json
from pathlib import Path
from datetime import datetime

# Add harness directory to path
sys.path.insert(0, str(Path(__file__).parent / "harness"))

from test_orchestrator import TestOrchestrator, TestConfig
from fixtures_loader import FixturesLoader

def main():
    """Main test execution function"""
    print("\n" + "="*70)
    print(" INTELLIDOC SUBAGENT TESTING HARNESS v2.0")
    print("="*70)
    print(f"Test Run: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-"*70)

    # Load and check fixtures
    print("\n📊 Loading Test Fixtures...")
    loader = FixturesLoader()
    coverage_report = loader.get_coverage_report()

    print(f"✓ Loaded fixtures for {coverage_report['agents_with_fixtures']} agents")
    print(f"✓ Total test cases: {coverage_report['total_test_cases']}")
    print(f"✓ Overall coverage: {coverage_report['overall_coverage']:.1f}%")

    # Configure test execution
    config = TestConfig(
        test_mode="comprehensive",
        parallel_execution=True,
        max_workers=4,
        verbose=True,
        save_reports=True,
        retry_on_failure=True
    )

    # Initialize orchestrator
    print("\n🚀 Initializing Test Orchestrator...")
    orchestrator = TestOrchestrator(config)

    # Run tests based on command line arguments
    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "coverage":
            # Show coverage report
            loader.print_coverage_summary()

        elif command == "validate":
            # Validate fixtures
            print("\n🔍 Validating Fixtures...")
            validation = loader.validate_fixtures()
            print(f"✓ Valid fixtures: {validation['valid_fixtures']}")
            if validation['invalid_fixtures'] > 0:
                print(f"✗ Invalid fixtures: {validation['invalid_fixtures']}")
                for error in validation['errors'][:5]:
                    print(f"  - {error}")

        elif command == "quick":
            # Quick test run
            print("\n⚡ Running Quick Tests...")
            config.test_mode = "quick"
            orchestrator.run_regression_suite()

        elif command == "benchmark":
            # Performance benchmarks
            print("\n📈 Running Performance Benchmarks...")
            report = orchestrator.benchmark_performance()
            print(json.dumps(report, indent=2, default=str))

        elif command == "workflow":
            # Test specific workflow
            if len(sys.argv) > 2:
                workflow = sys.argv[2]
                print(f"\n🔄 Testing Workflow: {workflow}")
                orchestrator.test_workflow(workflow)
            else:
                print("Available workflows: quick-news, blog-post, tutorial")

        elif command == "agent":
            # Test specific agent
            if len(sys.argv) > 2:
                agent = sys.argv[2]
                print(f"\n🤖 Testing Agent: {agent}")
                result = orchestrator._test_single_agent(agent)
                print(json.dumps(result, indent=2, default=str))
            else:
                print("Please specify an agent name")

        elif command == "phase":
            # Test specific phase
            if len(sys.argv) > 2:
                phase = sys.argv[2]
                print(f"\n📦 Testing Phase: {phase}")
                agents = orchestrator.all_agents.get(phase, [])
                if agents:
                    results = orchestrator._test_phase(phase, agents)
                    print(f"Tested {len(results)} agents in {phase} phase")
                else:
                    print(f"Unknown phase: {phase}")
                    print("Available phases:", list(orchestrator.all_agents.keys()))
            else:
                print("Available phases:", list(orchestrator.all_agents.keys()))

        else:
            print(f"Unknown command: {command}")
            print_usage()

    else:
        # Run comprehensive tests
        print("\n🎯 Running Comprehensive Test Suite...")
        print("This will test all 41 agents with all fixtures")
        print("Estimated time: 15-30 minutes")

        try:
            report = orchestrator.run_all_tests()

            # Save detailed report
            report_path = Path(__file__).parent / "reports" / f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            report_path.parent.mkdir(exist_ok=True)

            with open(report_path, 'w') as f:
                json.dump(report, f, indent=2, default=str)

            print(f"\n📄 Detailed report saved to: {report_path}")

        except KeyboardInterrupt:
            print("\n\n⚠️  Test run interrupted by user")
        except Exception as e:
            print(f"\n\n❌ Test run failed: {e}")
            import traceback
            traceback.print_exc()


def print_usage():
    """Print usage information"""
    print("\nUsage: python run_tests.py [command] [args]")
    print("\nCommands:")
    print("  coverage      - Show fixture coverage report")
    print("  validate      - Validate all fixtures")
    print("  quick         - Run quick regression tests")
    print("  benchmark     - Run performance benchmarks")
    print("  workflow NAME - Test specific workflow (quick-news, blog-post, tutorial)")
    print("  agent NAME    - Test specific agent")
    print("  phase NAME    - Test all agents in phase")
    print("  (no command)  - Run comprehensive test suite")
    print("\nExamples:")
    print("  python run_tests.py coverage")
    print("  python run_tests.py workflow blog-post")
    print("  python run_tests.py agent keyword-researcher")
    print("  python run_tests.py phase research")


if __name__ == "__main__":
    main()