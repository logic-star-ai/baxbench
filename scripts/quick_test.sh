#!/bin/bash
# Quick test with minimal parameters

echo "=== Quick BaxBench Test ==="
echo "Testing with 1 sample to isolate timing issues"

# Test corridor flag with minimal settings
time pipenv run python src/main.py \
  --corridor \
  --models gpt-4o-mini \
  --mode generate \
  --scenarios Login \
  --envs Python-Flask \
  --n_samples 1 \
  --force \
  --timeout 60