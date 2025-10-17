#!/usr/bin/env python3
"""
Test runner for SimpleLang algorithm implementations.

This script runs all algorithm tests (Dijkstra, A*, N-Queens) and provides
a summary of results.
"""

import unittest
import sys
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def run_algorithm_tests():
    """Run all algorithm tests and display results."""
    print("=" * 70)
    print("SimpleLang Algorithm Tests")
    print("=" * 70)
    print()

    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all algorithm tests
    test_modules = [
        'tests.algorithms.test_dijkstra',
        'tests.algorithms.test_astar',
        'tests.algorithms.test_nqueens',
    ]

    for module in test_modules:
        try:
            tests = loader.loadTestsFromName(module)
            suite.addTests(tests)
        except Exception as e:
            print(f"Error loading tests from {module}: {e}")
            return 1

    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print()
    print("=" * 70)
    print("Summary")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print()

    if result.wasSuccessful():
        print("All tests passed! ✓")
        return 0
    else:
        print("Some tests failed. ✗")
        return 1


if __name__ == '__main__':
    sys.exit(run_algorithm_tests())
