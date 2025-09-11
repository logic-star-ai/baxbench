#!/bin/bash
# Baseline runs (no security prompts)

echo "Running baseline benchmarks..."

# Generate
pipenv run python src/main.py --models gpt-4o-mini --mode generate --scenarios Login FileSearch ShoppingCart --envs Python-Flask --n_samples 5 --safety_prompt none

# Test
pipenv run python src/main.py --models gpt-4o-mini --mode test --scenarios Login FileSearch ShoppingCart --envs Python-Flask --n_samples 5 --safety_prompt none

# Evaluate
pipenv run python src/main.py --models gpt-4o-mini --mode evaluate --scenarios Login FileSearch ShoppingCart --envs Python-Flask --n_samples 5 --safety_prompt none