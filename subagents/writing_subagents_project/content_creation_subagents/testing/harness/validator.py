#!/usr/bin/env python3
"""
SubAgent Testing Harness - Validation Framework
Comprehensive validation system for agent inputs and outputs
"""

import json
import re
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from pathlib import Path

class SchemaValidator:
    """JSON Schema validator for agent inputs and outputs"""

    def __init__(self, schema: Dict):
        """Initialize with a JSON schema"""
        self.schema = schema

    def validate(self, data: Any) -> Tuple[bool, List[str]]:
        """
        Validate data against schema

        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        is_valid = self._validate_value(data, self.schema, errors, "root")
        return is_valid, errors

    def _validate_value(self, value: Any, schema: Dict, errors: List[str], path: str) -> bool:
        """Recursively validate a value against a schema"""
        # Type validation
        if "type" in schema:
            if not self._check_type(value, schema["type"]):
                errors.append(f"{path}: Expected type {schema['type']}, got {type(value).__name__}")
                return False

        # Handle different types
        schema_type = schema.get("type")

        if schema_type == "object":
            return self._validate_object(value, schema, errors, path)
        elif schema_type == "array":
            return self._validate_array(value, schema, errors, path)
        elif schema_type == "string":
            return self._validate_string(value, schema, errors, path)
        elif schema_type == "number":
            return self._validate_number(value, schema, errors, path)
        elif schema_type == "boolean":
            return self._validate_boolean(value, schema, errors, path)

        # Enum validation
        if "enum" in schema:
            if value not in schema["enum"]:
                errors.append(f"{path}: Value '{value}' not in allowed values {schema['enum']}")
                return False

        return len(errors) == 0

    def _check_type(self, value: Any, expected_type: str) -> bool:
        """Check if value matches expected type"""
        type_mapping = {
            "object": dict,
            "array": list,
            "string": str,
            "number": (int, float),
            "boolean": bool,
            "null": type(None)
        }
        expected = type_mapping.get(expected_type)
        if expected:
            return isinstance(value, expected)
        return False

    def _validate_object(self, value: Dict, schema: Dict, errors: List[str], path: str) -> bool:
        """Validate object type"""
        if not isinstance(value, dict):
            errors.append(f"{path}: Expected object, got {type(value).__name__}")
            return False

        # Check required properties
        for required_prop in schema.get("required", []):
            if required_prop not in value:
                errors.append(f"{path}.{required_prop}: Required property missing")

        # Validate properties
        properties = schema.get("properties", {})
        for prop_name, prop_value in value.items():
            if prop_name in properties:
                prop_schema = properties[prop_name]
                self._validate_value(prop_value, prop_schema, errors, f"{path}.{prop_name}")

        # Check additionalProperties
        if "additionalProperties" in schema and schema["additionalProperties"] is False:
            extra_props = set(value.keys()) - set(properties.keys())
            if extra_props:
                errors.append(f"{path}: Unexpected properties: {extra_props}")

        return len(errors) == 0

    def _validate_array(self, value: List, schema: Dict, errors: List[str], path: str) -> bool:
        """Validate array type"""
        if not isinstance(value, list):
            errors.append(f"{path}: Expected array, got {type(value).__name__}")
            return False

        # Check length constraints
        if "minItems" in schema and len(value) < schema["minItems"]:
            errors.append(f"{path}: Array has {len(value)} items, minimum is {schema['minItems']}")

        if "maxItems" in schema and len(value) > schema["maxItems"]:
            errors.append(f"{path}: Array has {len(value)} items, maximum is {schema['maxItems']}")

        # Validate items
        if "items" in schema:
            item_schema = schema["items"]
            for i, item in enumerate(value):
                self._validate_value(item, item_schema, errors, f"{path}[{i}]")

        return len(errors) == 0

    def _validate_string(self, value: str, schema: Dict, errors: List[str], path: str) -> bool:
        """Validate string type"""
        if not isinstance(value, str):
            errors.append(f"{path}: Expected string, got {type(value).__name__}")
            return False

        # Check length constraints
        if "minLength" in schema and len(value) < schema["minLength"]:
            errors.append(f"{path}: String length {len(value)} is less than minimum {schema['minLength']}")

        if "maxLength" in schema and len(value) > schema["maxLength"]:
            errors.append(f"{path}: String length {len(value)} exceeds maximum {schema['maxLength']}")

        # Check pattern
        if "pattern" in schema:
            pattern = schema["pattern"]
            if not re.match(pattern, value):
                errors.append(f"{path}: String doesn't match pattern {pattern}")

        return len(errors) == 0

    def _validate_number(self, value: Any, schema: Dict, errors: List[str], path: str) -> bool:
        """Validate number type"""
        if not isinstance(value, (int, float)):
            errors.append(f"{path}: Expected number, got {type(value).__name__}")
            return False

        # Check range constraints
        if "minimum" in schema and value < schema["minimum"]:
            errors.append(f"{path}: Value {value} is less than minimum {schema['minimum']}")

        if "maximum" in schema and value > schema["maximum"]:
            errors.append(f"{path}: Value {value} exceeds maximum {schema['maximum']}")

        return len(errors) == 0

    def _validate_boolean(self, value: Any, schema: Dict, errors: List[str], path: str) -> bool:
        """Validate boolean type"""
        if not isinstance(value, bool):
            errors.append(f"{path}: Expected boolean, got {type(value).__name__}")
            return False
        return True


class OutputValidator:
    """Validate agent outputs for quality and completeness"""

    def __init__(self):
        """Initialize output validator"""
        self.quality_checks = {
            "content_length": self._check_content_length,
            "required_fields": self._check_required_fields,
            "format_consistency": self._check_format_consistency,
            "semantic_validity": self._check_semantic_validity
        }

    def validate_output(self, agent_name: str, output: Any, requirements: Dict = None) -> Tuple[bool, Dict]:
        """
        Validate agent output for quality

        Args:
            agent_name: Name of the agent
            output: Agent's output
            requirements: Optional specific requirements

        Returns:
            Tuple of (is_valid, validation_report)
        """
        report = {
            "agent": agent_name,
            "timestamp": datetime.now().isoformat(),
            "checks": {},
            "is_valid": True,
            "score": 100
        }

        # Run quality checks
        for check_name, check_func in self.quality_checks.items():
            check_result = check_func(output, requirements)
            report["checks"][check_name] = check_result

            if not check_result["passed"]:
                report["is_valid"] = False
                report["score"] -= check_result.get("penalty", 25)

        # Agent-specific validation
        agent_validation = self._agent_specific_validation(agent_name, output)
        report["checks"]["agent_specific"] = agent_validation

        if not agent_validation["passed"]:
            report["is_valid"] = False
            report["score"] -= agent_validation.get("penalty", 30)

        report["score"] = max(0, report["score"])
        return report["is_valid"], report

    def _check_content_length(self, output: Any, requirements: Dict = None) -> Dict:
        """Check if content meets length requirements"""
        result = {"passed": True, "details": {}}

        if isinstance(output, str):
            length = len(output)
            min_length = requirements.get("min_length", 0) if requirements else 0
            max_length = requirements.get("max_length", float("inf")) if requirements else float("inf")

            if length < min_length:
                result["passed"] = False
                result["details"]["error"] = f"Content too short: {length} < {min_length}"
                result["penalty"] = 20
            elif length > max_length:
                result["passed"] = False
                result["details"]["error"] = f"Content too long: {length} > {max_length}"
                result["penalty"] = 10

            result["details"]["length"] = length

        return result

    def _check_required_fields(self, output: Any, requirements: Dict = None) -> Dict:
        """Check if all required fields are present"""
        result = {"passed": True, "details": {}}

        if isinstance(output, dict) and requirements:
            required_fields = requirements.get("required_fields", [])
            missing_fields = []

            for field in required_fields:
                if field not in output or output[field] is None:
                    missing_fields.append(field)

            if missing_fields:
                result["passed"] = False
                result["details"]["missing_fields"] = missing_fields
                result["penalty"] = 30

        return result

    def _check_format_consistency(self, output: Any, requirements: Dict = None) -> Dict:
        """Check format consistency"""
        result = {"passed": True, "details": {}}

        # Check for consistent formatting in arrays
        if isinstance(output, dict):
            for key, value in output.items():
                if isinstance(value, list) and len(value) > 0:
                    first_type = type(value[0])
                    if not all(isinstance(item, first_type) for item in value):
                        result["passed"] = False
                        result["details"][f"{key}_inconsistent"] = "Mixed types in array"
                        result["penalty"] = 15

        return result

    def _check_semantic_validity(self, output: Any, requirements: Dict = None) -> Dict:
        """Check semantic validity of output"""
        result = {"passed": True, "details": {}}

        # Check for empty or meaningless content
        if isinstance(output, str):
            if len(output.strip()) == 0:
                result["passed"] = False
                result["details"]["error"] = "Empty content"
                result["penalty"] = 50
            elif len(set(output.split())) < 10:  # Too repetitive
                result["passed"] = False
                result["details"]["error"] = "Content appears repetitive or meaningless"
                result["penalty"] = 40

        elif isinstance(output, dict):
            # Check for empty values in critical fields
            for key, value in output.items():
                if isinstance(value, str) and len(value.strip()) == 0:
                    result["passed"] = False
                    result["details"][f"{key}_empty"] = "Empty value"
                    result["penalty"] = 20
                    break

        return result

    def _agent_specific_validation(self, agent_name: str, output: Any) -> Dict:
        """Agent-specific validation rules"""
        result = {"passed": True, "details": {}}

        # Keyword researcher specific checks
        if agent_name == "keyword-researcher":
            if isinstance(output, dict):
                if "long_tail" in output and len(output["long_tail"]) < 3:
                    result["passed"] = False
                    result["details"]["error"] = "Insufficient long-tail keywords"
                    result["penalty"] = 25

        # Body writer specific checks
        elif agent_name == "body-writer":
            if isinstance(output, dict) and "body_content" in output:
                content = output["body_content"]
                if len(content.split()) < 100:
                    result["passed"] = False
                    result["details"]["error"] = "Body content too short"
                    result["penalty"] = 35

        # Source gatherer specific checks
        elif agent_name == "source-gatherer":
            if isinstance(output, dict) and "sources" in output:
                if len(output["sources"]) < 5:
                    result["passed"] = False
                    result["details"]["error"] = "Insufficient sources (minimum 5)"
                    result["penalty"] = 30

        return result


class PipelineValidator:
    """Validate complete pipeline execution"""

    def __init__(self):
        """Initialize pipeline validator"""
        self.phase_dependencies = {
            "strategy": ["research"],
            "content": ["research", "strategy"],
            "qa": ["content"],
            "distribution": ["content", "qa"],
            "performance": ["distribution"]
        }

    def validate_pipeline_flow(self, execution_log: List[Dict]) -> Tuple[bool, Dict]:
        """
        Validate that pipeline execution follows correct flow

        Args:
            execution_log: List of execution records

        Returns:
            Tuple of (is_valid, validation_report)
        """
        report = {
            "is_valid": True,
            "phases_executed": [],
            "dependency_violations": [],
            "timing_issues": [],
            "handoff_problems": []
        }

        # Extract phases from execution log
        phases_executed = []
        for record in execution_log:
            phase = record.get("phase")
            if phase and phase not in phases_executed:
                phases_executed.append(phase)
                report["phases_executed"].append(phase)

        # Check dependencies
        for i, phase in enumerate(phases_executed):
            required_phases = self.phase_dependencies.get(phase, [])
            for req_phase in required_phases:
                if req_phase not in phases_executed[:i]:
                    report["is_valid"] = False
                    report["dependency_violations"].append({
                        "phase": phase,
                        "missing_dependency": req_phase
                    })

        # Check timing and handoffs
        self._check_timing(execution_log, report)
        self._check_handoffs(execution_log, report)

        return report["is_valid"], report

    def _check_timing(self, execution_log: List[Dict], report: Dict):
        """Check for timing issues in pipeline execution"""
        prev_timestamp = None

        for record in execution_log:
            timestamp = record.get("timestamp")
            if timestamp:
                if prev_timestamp and timestamp < prev_timestamp:
                    report["timing_issues"].append({
                        "error": "Out of order execution",
                        "agent": record.get("agent")
                    })
                    report["is_valid"] = False
                prev_timestamp = timestamp

    def _check_handoffs(self, execution_log: List[Dict], report: Dict):
        """Check data handoffs between agents"""
        for i in range(len(execution_log) - 1):
            current = execution_log[i]
            next_record = execution_log[i + 1]

            # Check if output from current matches input to next
            current_output = current.get("output", {})
            next_input = next_record.get("input", {})

            # Basic check: ensure data is passed
            if current_output and not next_input:
                report["handoff_problems"].append({
                    "from": current.get("agent"),
                    "to": next_record.get("agent"),
                    "issue": "No input received"
                })


class PerformanceValidator:
    """Validate performance metrics"""

    def __init__(self, benchmarks: Dict = None):
        """Initialize with performance benchmarks"""
        self.benchmarks = benchmarks or {
            "max_execution_time": 60,  # seconds
            "max_tokens_per_agent": 2000,
            "max_total_tokens": 50000,
            "min_success_rate": 0.95
        }

    def validate_performance(self, metrics: Dict) -> Tuple[bool, Dict]:
        """
        Validate performance against benchmarks

        Args:
            metrics: Performance metrics dictionary

        Returns:
            Tuple of (meets_benchmarks, performance_report)
        """
        report = {
            "meets_benchmarks": True,
            "violations": [],
            "warnings": [],
            "metrics": metrics
        }

        # Check execution time
        if metrics.get("execution_time", 0) > self.benchmarks["max_execution_time"]:
            report["violations"].append({
                "metric": "execution_time",
                "value": metrics["execution_time"],
                "limit": self.benchmarks["max_execution_time"]
            })
            report["meets_benchmarks"] = False

        # Check token usage
        if metrics.get("total_tokens", 0) > self.benchmarks["max_total_tokens"]:
            report["violations"].append({
                "metric": "total_tokens",
                "value": metrics["total_tokens"],
                "limit": self.benchmarks["max_total_tokens"]
            })
            report["meets_benchmarks"] = False

        # Check success rate
        success_rate = metrics.get("success_rate", 0)
        if success_rate < self.benchmarks["min_success_rate"]:
            report["violations"].append({
                "metric": "success_rate",
                "value": success_rate,
                "limit": self.benchmarks["min_success_rate"]
            })
            report["meets_benchmarks"] = False

        # Add warnings for near-limit metrics
        if metrics.get("execution_time", 0) > self.benchmarks["max_execution_time"] * 0.8:
            report["warnings"].append({
                "metric": "execution_time",
                "message": "Approaching time limit"
            })

        return report["meets_benchmarks"], report


# Utility functions
def load_schemas(schema_path: Path) -> Dict:
    """Load validation schemas from file"""
    try:
        with open(schema_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading schemas: {e}")
        return {}


def validate_agent_io(agent_name: str, input_data: Any, output_data: Any, schemas: Dict) -> Dict:
    """
    Convenience function to validate both input and output

    Args:
        agent_name: Name of the agent
        input_data: Input to validate
        output_data: Output to validate
        schemas: Dictionary of validation schemas

    Returns:
        Validation report
    """
    report = {
        "agent": agent_name,
        "input_validation": {"valid": True, "errors": []},
        "output_validation": {"valid": True, "errors": []},
        "overall_valid": True
    }

    # Get agent schemas
    agent_schemas = schemas.get("agent_validation", {}).get(agent_name, {})

    # Validate input
    if "input_schema" in agent_schemas:
        validator = SchemaValidator(agent_schemas["input_schema"])
        is_valid, errors = validator.validate(input_data)
        report["input_validation"]["valid"] = is_valid
        report["input_validation"]["errors"] = errors
        if not is_valid:
            report["overall_valid"] = False

    # Validate output
    if "output_schema" in agent_schemas:
        validator = SchemaValidator(agent_schemas["output_schema"])
        is_valid, errors = validator.validate(output_data)
        report["output_validation"]["valid"] = is_valid
        report["output_validation"]["errors"] = errors
        if not is_valid:
            report["overall_valid"] = False

    return report