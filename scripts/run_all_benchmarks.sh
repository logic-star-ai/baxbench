#!/bin/bash
# Complete benchmark suite for assignment submission

set -e  # Exit on error

echo "=== BaxBench Complete Benchmark Suite ==="
echo "This will run baseline, generic, and corridor benchmarks"
echo "Estimated time: 2-3 hours"
echo ""

# Pre-generate corridor reminders for speed
echo "Pre-generating corridor reminders..."
pipenv run python scripts/pregenerate_corridor.py

echo ""
echo "=== Running Baseline Benchmarks ==="
./scripts/run_baseline.sh

echo ""
echo "=== Running Generic Security Benchmarks ==="  
./scripts/run_generic.sh

echo ""
echo "=== Running Corridor Security Benchmarks ==="
./scripts/run_corridor.sh

echo ""
echo "=== Benchmark Suite Complete ==="
echo "Results saved to results/ directory"
echo "Run evaluation commands to generate tables for REPORT.md"