#!/usr/bin/env python3
"""
Run Policy Tests for OpenClaw Agent Prompt Patterns

Usage:
    python run_tests.py              # Run all tests
    python run_tests.py --required-only  # Run only required tests

Exit codes:
    0 - All tests passed
    1 - One or more required tests failed
"""

import sys
import yaml
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class TestResult:
    test_id: str
    passed: bool
    errors: List[str]
    warnings: List[str]


def load_test_cases(test_file: Path) -> Dict[str, Any]:
    """Load YAML test cases."""
    with open(test_file, 'r') as f:
        return yaml.safe_load(f)


def validate_test_case(case: Dict[str, Any]) -> List[str]:
    """Validate a single test case structure."""
    errors = []
    
    required_fields = ['id', 'title', 'input', 'expected_behavior', 'pass_criteria']
    for field in required_fields:
        if field not in case:
            errors.append(f"Missing required field: {field}")
    
    return errors


def run_test_case(case: Dict[str, Any]) -> TestResult:
    """Run a single test case and return result."""
    errors = []
    warnings = []
    
    # Validate structure
    structure_errors = validate_test_case(case)
    errors.extend(structure_errors)
    
    # Check for forbidden behaviors
    if 'forbidden_behavior' in case:
        forbidden = case['forbidden_behavior']
        if isinstance(forbidden, list):
            for item in forbidden:
                if item.lower() in str(case.get('input', '')).lower():
                    errors.append(f"Forbidden behavior detected: {item}")
    
    # Check pass criteria
    pass_criteria = case.get('pass_criteria', [])
    if isinstance(pass_criteria, list):
        for criteria in pass_criteria:
            # Simple heuristic: criteria should be present in expected behavior
            if criteria.lower() not in str(case.get('expected_behavior', '')).lower():
                warnings.append(f"Pass criteria not found in expected behavior: {criteria}")
    
    return TestResult(
        test_id=case.get('id', 'unknown'),
        passed=len(errors) == 0,
        errors=errors,
        warnings=warnings
    )


def run_test_file(test_file: Path) -> List[TestResult]:
    """Run all test cases in a file."""
    data = load_test_cases(test_file)
    results = []
    
    if not data or 'test_cases' not in data:
        return [TestResult(
            test_id="structure",
            passed=False,
            errors=["No test_cases found in file"],
            warnings=[]
        )]
    
    for case in data['test_cases']:
        result = run_test_case(case)
        results.append(result)
    
    return results


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Run policy tests')
    parser.add_argument('--required-only', action='store_true', 
                        help='Run only required tests')
    args = parser.parse_args()
    
    # Required tests (block merge)
    required_tests = [
        'agent_loop_cases.yaml',
        'edit_policy_cases.yaml',
        'destructive_action_cases.yaml',
        'secret_handling_cases.yaml',
        'database_safety_cases.yaml',
    ]
    
    # Optional tests (report only)
    optional_tests = [
        'tool_selection_cases.yaml',
        'verification_cases.yaml',
        'rollback_cases.yaml',
        'evidence_logging_cases.yaml',
        'frontend_generation_cases.yaml',
    ]
    
    if args.required_only:
        test_files = required_tests
    else:
        test_files = required_tests + optional_tests
    
    test_dir = Path(__file__).parent
    
    all_passed = True
    total_tests = 0
    total_passed = 0
    total_failed = 0
    
    print("=" * 60)
    print("OpenClaw Agent Prompt Patterns - Policy Tests")
    print("=" * 60)
    print()
    
    for test_file in test_files:
        file_path = test_dir / test_file
        
        if not file_path.exists():
            print(f"⚠️  Missing: {test_file}")
            continue
        
        print(f"Running: {test_file}")
        
        results = run_test_file(file_path)
        
        for result in results:
            total_tests += 1
            
            if result.passed:
                total_passed += 1
                print(f"  ✅ {result.test_id}")
            else:
                total_failed += 1
                print(f"  ❌ {result.test_id}")
                for error in result.errors:
                    print(f"     Error: {error}")
            
            for warning in result.warnings:
                print(f"     Warning: {warning}")
        
        print()
    
    print("=" * 60)
    print(f"Results: {total_passed}/{total_tests} passed")
    print(f"Failed: {total_failed}")
    print("=" * 60)
    
    if total_failed > 0:
        print()
        print("❌ Some tests failed")
        sys.exit(1)
    else:
        print()
        print("✅ All tests passed")
        sys.exit(0)


if __name__ == '__main__':
    main()
