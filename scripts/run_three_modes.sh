#!/bin/bash
# Run benchmarks in three modes for assignment submission

# Function to run command with timeout
run_with_timeout() {
    timeout 300 "$@"  # 5 minute timeout
    if [ $? -eq 124 ]; then
        echo "Command timed out after 5 minutes: $*"
        return 1
    fi
}

SCENARIOS="Calculator ShoppingCartService Login"
MODEL="gpt-4o"
SAMPLES=1

echo "=== Running Three-Mode Benchmark Suite ==="
echo "Scenarios: $SCENARIOS"
echo "Model: $MODEL"
echo "Samples: $SAMPLES"

# 1. BASELINE (no security reminder)
echo ""
echo "=== BASELINE MODE ==="
pipenv run python src/main.py --models $MODEL --mode generate --scenarios $SCENARIOS --n_samples $SAMPLES --safety_prompt none --force
pipenv run python src/main.py --models $MODEL --mode test --scenarios $SCENARIOS --n_samples $SAMPLES --safety_prompt none
pipenv run python src/main.py --models $MODEL --mode evaluate --scenarios $SCENARIOS --n_samples $SAMPLES --safety_prompt none > results_baseline.txt

# 2. GENERIC MODE
echo ""
echo "=== GENERIC MODE ==="
pipenv run python src/main.py --generic --models $MODEL --mode generate --scenarios $SCENARIOS --n_samples $SAMPLES --force
pipenv run python src/main.py --generic --models $MODEL --mode test --scenarios $SCENARIOS --n_samples $SAMPLES
pipenv run python src/main.py --generic --models $MODEL --mode evaluate --scenarios $SCENARIOS --n_samples $SAMPLES > results_generic.txt

# 3. CORRIDOR MODE
echo ""
echo "=== CORRIDOR MODE ==="
pipenv run python src/main.py --corridor --models $MODEL --mode generate --scenarios $SCENARIOS --n_samples $SAMPLES --force
pipenv run python src/main.py --corridor --models $MODEL --mode test --scenarios $SCENARIOS --n_samples $SAMPLES
pipenv run python src/main.py --corridor --models $MODEL --mode evaluate --scenarios $SCENARIOS --n_samples $SAMPLES > results_corridor.txt

echo ""
echo "=== BENCHMARK COMPLETE ==="
echo "Results saved to:"
echo "- results_baseline.txt"
echo "- results_generic.txt" 
echo "- results_corridor.txt"