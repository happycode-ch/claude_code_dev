#!/usr/bin/env python3
"""
SubAgent Testing Harness - Claude Task Tool Executor
Wrapper for Claude Code Task tool integration
"""

import json
import time
import asyncio
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
import subprocess
import sys

@dataclass
class AgentTask:
    """Represents a task for an agent"""
    agent_name: str
    agent_spec: str
    input_data: Dict
    subagent_type: str = "general-purpose"
    timeout: int = 30

@dataclass
class TaskResult:
    """Result from Task tool execution"""
    success: bool
    output: Any
    execution_time: float
    tokens_used: int
    error: Optional[str] = None
    agent_name: Optional[str] = None
    timestamp: str = ""

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()


class ClaudeTaskExecutor:
    """Wrapper for Claude Code Task tool integration"""

    def __init__(self, config: Dict = None):
        """Initialize Task executor with configuration"""
        default_config = self._default_config()
        if config:
            default_config.update(config)
        self.config = default_config
        self.task_history = []
        self.execution_cache = {}
        self.mock_mode = self.config.get("fallback_to_mock", True)
        self.stats = {
            "total_executions": 0,
            "successful_executions": 0,
            "failed_executions": 0,
            "total_tokens": 0,
            "total_time": 0
        }

    def _default_config(self) -> Dict:
        """Return default configuration"""
        return {
            "enabled": True,
            "fallback_to_mock": True,
            "timeout_seconds": 30,
            "retry_attempts": 2,
            "parallel_execution": True,
            "max_parallel_tasks": 4,
            "cache_results": True,
            "verbose": False
        }

    def execute_agent(self, agent_name: str, agent_spec: str, input_data: Dict) -> TaskResult:
        """
        Execute agent via Claude Task tool

        Args:
            agent_name: Name of the agent to execute
            agent_spec: Agent specification/prompt
            input_data: Input data for the agent

        Returns:
            TaskResult with execution details
        """
        start_time = time.time()
        self.stats["total_executions"] += 1

        # Check cache if enabled
        cache_key = self._get_cache_key(agent_name, input_data)
        if self.config["cache_results"] and cache_key in self.execution_cache:
            if self.config["verbose"]:
                print(f"  ↺ Using cached result for {agent_name}")
            return self.execution_cache[cache_key]

        try:
            # Attempt real Task tool execution
            if self.config["enabled"] and not self.mock_mode:
                result = self._execute_real_task(agent_name, agent_spec, input_data)
            else:
                # Fallback to mock execution
                result = self._execute_mock_task(agent_name, agent_spec, input_data)

            # Update statistics
            execution_time = time.time() - start_time
            result.execution_time = execution_time
            self.stats["total_time"] += execution_time

            if result.success:
                self.stats["successful_executions"] += 1
            else:
                self.stats["failed_executions"] += 1

            # Cache result if enabled
            if self.config["cache_results"]:
                self.execution_cache[cache_key] = result

            # Store in history
            self.task_history.append({
                "agent": agent_name,
                "timestamp": datetime.now().isoformat(),
                "success": result.success,
                "execution_time": execution_time
            })

            return result

        except Exception as e:
            self.stats["failed_executions"] += 1
            return TaskResult(
                success=False,
                output=None,
                execution_time=time.time() - start_time,
                tokens_used=0,
                error=str(e),
                agent_name=agent_name
            )

    def _execute_real_task(self, agent_name: str, agent_spec: str, input_data: Dict) -> TaskResult:
        """
        Execute real Task tool invocation

        This would integrate with actual Claude Code Task tool.
        For now, it simulates the integration point.
        """
        # Build the Task tool invocation
        task_prompt = self._build_task_prompt(agent_name, agent_spec, input_data)

        # In real implementation, this would use the Task tool
        # For demonstration, we'll prepare the structure
        task_config = {
            "description": f"Test {agent_name}",
            "prompt": task_prompt,
            "subagent_type": "general-purpose"
        }

        if self.config["verbose"]:
            print(f"  → Executing real task for {agent_name}")
            print(f"    Input keys: {list(input_data.keys())}")

        # Simulate Task tool execution
        # In production, this would be:
        # result = Task(**task_config)

        # For now, return mock with real structure
        return self._execute_mock_task(agent_name, agent_spec, input_data)

    def _execute_mock_task(self, agent_name: str, agent_spec: str, input_data: Dict) -> TaskResult:
        """Execute mock task for testing without real Task tool"""
        # Simulate execution delay
        time.sleep(0.1)

        # Generate mock output based on agent type
        mock_output = self._generate_mock_output(agent_name, input_data)

        # Estimate tokens (rough approximation)
        tokens = len(json.dumps(input_data)) // 4 + len(json.dumps(mock_output)) // 4

        return TaskResult(
            success=True,
            output=mock_output,
            execution_time=0.1,
            tokens_used=tokens,
            agent_name=agent_name
        )

    def _build_task_prompt(self, agent_name: str, agent_spec: str, input_data: Dict) -> str:
        """Build the complete prompt for Task tool"""
        prompt_parts = [
            f"You are the {agent_name} agent.",
            "",
            "## Agent Specification",
            agent_spec,
            "",
            "## Input Data",
            json.dumps(input_data, indent=2),
            "",
            "## Instructions",
            f"Process the input according to your role as {agent_name}.",
            "Return output in the expected JSON format.",
            "Ensure all required fields are present."
        ]

        return "\n".join(prompt_parts)

    def _generate_mock_output(self, agent_name: str, input_data: Dict) -> Dict:
        """Generate appropriate mock output based on agent type"""
        # Agent-specific mock outputs
        mock_outputs = {
            "keyword-researcher": {
                "primary_keyword": f"test keyword for {input_data.get('topic', 'topic')}",
                "long_tail": ["long tail 1", "long tail 2", "long tail 3"],
                "search_volume": "medium",
                "difficulty": "medium"
            },
            "topic-scout": {
                "trending_topics": ["trend 1", "trend 2", "trend 3"],
                "content_gaps": ["gap 1", "gap 2"],
                "opportunities": ["opportunity 1", "opportunity 2"]
            },
            "source-gatherer": {
                "sources": [
                    "https://source1.com",
                    "https://source2.com",
                    "https://source3.com",
                    "https://source4.com",
                    "https://source5.com"
                ],
                "key_points": ["point 1", "point 2", "point 3"]
            },
            "body-writer": {
                "body_content": f"Generated content for {input_data.get('outline', ['topic'])[0]}...",
                "sections_written": input_data.get("sections", ["section 1", "section 2"])
            },
            "grammar-checker": {
                "corrected_content": input_data.get("content", "corrected text"),
                "errors_found": ["error 1", "error 2"]
            },
            "content-atomizer": {
                "key_points": ["key point 1", "key point 2", "key point 3"],
                "snippets": ["snippet 1", "snippet 2"]
            }
        }

        # Return specific mock or generic
        if agent_name in mock_outputs:
            return mock_outputs[agent_name]
        else:
            return {
                "status": "completed",
                "output": f"Mock output for {agent_name}",
                "data": input_data
            }

    def batch_execute(self, agents: List[AgentTask], parallel: bool = None) -> List[TaskResult]:
        """
        Execute multiple agents with optional parallelization

        Args:
            agents: List of AgentTask objects
            parallel: Whether to execute in parallel (uses config if None)

        Returns:
            List of TaskResult objects
        """
        if parallel is None:
            parallel = self.config["parallel_execution"]

        if parallel and len(agents) > 1:
            return self._batch_execute_parallel(agents)
        else:
            return self._batch_execute_sequential(agents)

    def _batch_execute_sequential(self, agents: List[AgentTask]) -> List[TaskResult]:
        """Execute agents sequentially"""
        results = []

        for task in agents:
            result = self.execute_agent(
                agent_name=task.agent_name,
                agent_spec=task.agent_spec,
                input_data=task.input_data
            )
            results.append(result)

        return results

    def _batch_execute_parallel(self, agents: List[AgentTask]) -> List[TaskResult]:
        """Execute agents in parallel"""
        from concurrent.futures import ThreadPoolExecutor, as_completed

        results = []
        max_workers = min(self.config["max_parallel_tasks"], len(agents))

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_task = {
                executor.submit(
                    self.execute_agent,
                    task.agent_name,
                    task.agent_spec,
                    task.input_data
                ): task
                for task in agents
            }

            for future in as_completed(future_to_task):
                task = future_to_task[future]
                try:
                    result = future.result(timeout=task.timeout)
                    results.append(result)
                except Exception as e:
                    results.append(TaskResult(
                        success=False,
                        output=None,
                        execution_time=0,
                        tokens_used=0,
                        error=str(e),
                        agent_name=task.agent_name
                    ))

        return results

    def _get_cache_key(self, agent_name: str, input_data: Dict) -> str:
        """Generate cache key for agent execution"""
        import hashlib
        data_str = f"{agent_name}:{json.dumps(input_data, sort_keys=True)}"
        return hashlib.md5(data_str.encode()).hexdigest()

    def retry_on_failure(self, agent_name: str, agent_spec: str, input_data: Dict) -> TaskResult:
        """Execute with retry logic on failure"""
        last_error = None

        for attempt in range(self.config["retry_attempts"]):
            if self.config["verbose"] and attempt > 0:
                print(f"  ↻ Retry attempt {attempt + 1} for {agent_name}")

            result = self.execute_agent(agent_name, agent_spec, input_data)

            if result.success:
                return result

            last_error = result.error
            time.sleep(1)  # Brief delay between retries

        # All retries failed
        return TaskResult(
            success=False,
            output=None,
            execution_time=0,
            tokens_used=0,
            error=f"Failed after {self.config['retry_attempts']} attempts. Last error: {last_error}",
            agent_name=agent_name
        )

    def get_statistics(self) -> Dict:
        """Get execution statistics"""
        return {
            **self.stats,
            "success_rate": (
                self.stats["successful_executions"] / max(1, self.stats["total_executions"])
            ) * 100,
            "avg_execution_time": (
                self.stats["total_time"] / max(1, self.stats["total_executions"])
            ),
            "cache_size": len(self.execution_cache),
            "history_size": len(self.task_history)
        }

    def clear_cache(self):
        """Clear execution cache"""
        self.execution_cache.clear()

    def reset_statistics(self):
        """Reset execution statistics"""
        self.stats = {
            "total_executions": 0,
            "successful_executions": 0,
            "failed_executions": 0,
            "total_tokens": 0,
            "total_time": 0
        }
        self.task_history.clear()


# Utility functions
def create_agent_task(agent_name: str, spec_content: str, test_input: Dict) -> AgentTask:
    """Create an AgentTask object"""
    return AgentTask(
        agent_name=agent_name,
        agent_spec=spec_content,
        input_data=test_input,
        subagent_type="general-purpose",
        timeout=30
    )


if __name__ == "__main__":
    # Test the Task executor
    print("Testing Claude Task Executor...")

    # Create executor
    executor = ClaudeTaskExecutor({
        "verbose": True,
        "fallback_to_mock": True
    })

    # Test single agent execution
    result = executor.execute_agent(
        agent_name="keyword-researcher",
        agent_spec="Find relevant keywords for the given topic",
        input_data={
            "topic": "AI automation",
            "target_audience": "developers",
            "content_type": "blog"
        }
    )

    print(f"\nExecution result:")
    print(f"  Success: {result.success}")
    print(f"  Output: {result.output}")
    print(f"  Tokens: {result.tokens_used}")
    print(f"  Time: {result.execution_time:.3f}s")

    # Test batch execution
    tasks = [
        create_agent_task(
            "topic-scout",
            "Find trending topics",
            {"niche": "AI", "recent_performance": "good"}
        ),
        create_agent_task(
            "source-gatherer",
            "Gather sources",
            {"topic": "AI tools", "angle": "developers"}
        )
    ]

    print("\nBatch execution...")
    batch_results = executor.batch_execute(tasks, parallel=True)

    for i, result in enumerate(batch_results):
        print(f"  Task {i+1}: {result.agent_name} - {'✓' if result.success else '✗'}")

    # Print statistics
    stats = executor.get_statistics()
    print(f"\nStatistics:")
    print(f"  Total executions: {stats['total_executions']}")
    print(f"  Success rate: {stats['success_rate']:.1f}%")
    print(f"  Avg time: {stats['avg_execution_time']:.3f}s")