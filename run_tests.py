#!/usr/bin/env python3
"""
Test execution script for the Tetris testing suite.

This script provides convenient commands to run different types of tests
and generate test reports for the Sprint 1 testing suite.

Usage:
    python run_tests.py                    # Run all tests
    python run_tests.py --unit             # Run unit tests only
    python run_tests.py --integration      # Run integration tests only
    python run_tests.py --regression       # Run regression tests only
    python run_tests.py --acceptance       # Run acceptance tests only
    python run_tests.py --coverage         # Run tests with coverage report
    python run_tests.py --verbose          # Run tests with verbose output
    python run_tests.py --help             # Show help message
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path


def get_project_root():
    """Get the project root directory."""
    return Path(__file__).parent.absolute()


def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {command}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, 
                              capture_output=False, text=True)
        print(f"\n✅ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ {description} failed with exit code {e.returncode}")
        return False


def check_dependencies():
    """Check if required dependencies are installed."""
    required_packages = ['pytest', 'pytest-cov']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing required packages: {', '.join(missing_packages)}")
        print("Install them with: pip install " + " ".join(missing_packages))
        return False
    
    return True


def run_unit_tests(verbose=False):
    """Run unit tests."""
    cmd = "python -m pytest tests/ -k 'not integration and not regression and not acceptance'"
    if verbose:
        cmd += " -v"
    
    return run_command(cmd, "Unit Tests")


def run_integration_tests(verbose=False):
    """Run integration tests."""
    cmd = "python -m pytest tests/integration/"
    if verbose:
        cmd += " -v"
    
    return run_command(cmd, "Integration Tests")


def run_regression_tests(verbose=False):
    """Run regression tests."""
    cmd = "python -m pytest tests/regression/"
    if verbose:
        cmd += " -v"
    
    return run_command(cmd, "Regression Tests")


def run_acceptance_tests(verbose=False):
    """Run acceptance tests."""
    cmd = "python -m pytest tests/acceptance/"
    if verbose:
        cmd += " -v"
    
    return run_command(cmd, "Acceptance Tests")


def run_all_tests(verbose=False):
    """Run all tests."""
    cmd = "python -m pytest tests/"
    if verbose:
        cmd += " -v"
    
    return run_command(cmd, "All Tests")


def run_tests_with_coverage(verbose=False):
    """Run tests with coverage report."""
    cmd = "python -m pytest tests/ --cov=src --cov-report=html --cov-report=term-missing"
    if verbose:
        cmd += " -v"
    
    success = run_command(cmd, "Tests with Coverage Report")
    
    if success:
        print("\n📊 Coverage report generated in htmlcov/index.html")
    
    return success


def run_specific_test_file(test_file, verbose=False):
    """Run a specific test file."""
    cmd = f"python -m pytest {test_file}"
    if verbose:
        cmd += " -v"
    
    return run_command(cmd, f"Specific Test: {test_file}")


def run_tests_by_marker(marker, verbose=False):
    """Run tests by pytest marker."""
    cmd = f"python -m pytest tests/ -m {marker}"
    if verbose:
        cmd += " -v"
    
    return run_command(cmd, f"Tests with marker: {marker}")


def generate_test_report():
    """Generate a comprehensive test report."""
    print("\n📋 Generating comprehensive test report...")
    
    # Run all tests with detailed output
    cmd = "python -m pytest tests/ --cov=src --cov-report=html --cov-report=term-missing -v --tb=short"
    success = run_command(cmd, "Comprehensive Test Report")
    
    if success:
        print("\n📊 Test reports generated:")
        print("  - HTML coverage report: htmlcov/index.html")
        print("  - Console coverage summary: (see output above)")
    
    return success


def main():
    """Main function to handle command line arguments and run tests."""
    parser = argparse.ArgumentParser(
        description="Tetris Testing Suite Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_tests.py                    # Run all tests
  python run_tests.py --unit             # Run unit tests only
  python run_tests.py --integration      # Run integration tests only
  python run_tests.py --regression       # Run regression tests only
  python run_tests.py --acceptance       # Run acceptance tests only
  python run_tests.py --coverage         # Run tests with coverage report
  python run_tests.py --verbose          # Run tests with verbose output
  python run_tests.py --file tests/test_board.py  # Run specific test file
  python run_tests.py --marker slow      # Run tests with 'slow' marker
        """
    )
    
    # Test type options
    parser.add_argument('--unit', action='store_true', 
                       help='Run unit tests only')
    parser.add_argument('--integration', action='store_true', 
                       help='Run integration tests only')
    parser.add_argument('--regression', action='store_true', 
                       help='Run regression tests only')
    parser.add_argument('--acceptance', action='store_true', 
                       help='Run acceptance tests only')
    
    # Output options
    parser.add_argument('--verbose', '-v', action='store_true', 
                       help='Run tests with verbose output')
    parser.add_argument('--coverage', '-c', action='store_true', 
                       help='Run tests with coverage report')
    
    # Specific test options
    parser.add_argument('--file', '-f', type=str, 
                       help='Run specific test file')
    parser.add_argument('--marker', '-m', type=str, 
                       help='Run tests with specific marker')
    
    # Report options
    parser.add_argument('--report', action='store_true', 
                       help='Generate comprehensive test report')
    
    # Check dependencies
    parser.add_argument('--check-deps', action='store_true', 
                       help='Check if required dependencies are installed')
    
    args = parser.parse_args()
    
    # Change to project root directory
    project_root = get_project_root()
    os.chdir(project_root)
    print(f"Working directory: {project_root}")
    
    # Check dependencies if requested
    if args.check_deps:
        if check_dependencies():
            print("✅ All required dependencies are installed!")
        else:
            sys.exit(1)
        return
    
    # Check dependencies before running tests
    if not check_dependencies():
        print("\n💡 Tip: Use 'python run_tests.py --check-deps' to check dependencies")
        sys.exit(1)
    
    # Determine which tests to run
    success = True
    
    if args.report:
        success = generate_test_report()
    elif args.file:
        success = run_specific_test_file(args.file, args.verbose)
    elif args.marker:
        success = run_tests_by_marker(args.marker, args.verbose)
    elif args.coverage:
        success = run_tests_with_coverage(args.verbose)
    elif args.unit:
        success = run_unit_tests(args.verbose)
    elif args.integration:
        success = run_integration_tests(args.verbose)
    elif args.regression:
        success = run_regression_tests(args.verbose)
    elif args.acceptance:
        success = run_acceptance_tests(args.verbose)
    else:
        # Default: run all tests
        success = run_all_tests(args.verbose)
    
    # Print summary
    print(f"\n{'='*60}")
    if success:
        print("🎉 All tests completed successfully!")
        print("✅ Sprint 1 testing suite validation passed!")
    else:
        print("❌ Some tests failed!")
        print("🔍 Check the output above for details.")
    print(f"{'='*60}")
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
