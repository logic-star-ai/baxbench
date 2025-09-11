#!/bin/bash
# Corridor security prompt runs

echo "Running corridor security benchmarks..."

# Generate
pipenv run python src/main.py --corridor --models gpt-4o-mini --mode generate --scenarios Login FileSearch ShoppingCart --envs Python-Flask --n_samples 5

# Test
pipenv run python src/main.py --corridor --models gpt-4o-mini --mode test --scenarios Login FileSearch ShoppingCart --envs Python-Flask --n_samples 5

# Evaluate  
pipenv run python src/main.py --corridor --models gpt-4o-mini --mode evaluate --scenarios Login FileSearch ShoppingCart --envs Python-Flask --n_samples 5