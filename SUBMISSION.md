# BaxBench Security Prompt Engineering - Corridor Submission

## Files Included

1. **corridor-baxbench-submission.patch** - Git patch file with all code changes
2. **results.tar.gz** - Tarball containing benchmark results for baseline, generic, and corridor modes
3. **REPORT.md** - Analysis report with benchmark results and insights
4. **website.tar.gz** - Complete React website with Python backend

## Quick Start

```bash
# Apply the patch
git apply corridor-baxbench-submission.patch

# Extract results
tar -xzf results.tar.gz

# Extract and run website
tar -xzf website.tar.gz
cd website
./start.sh
```

## Key Features Implemented

- --generic and --corridor CLI flags with mutual exclusivity
- Dynamic corridor security reminder system with LLM integration
- Performance caching (9.3s → 0.27s)
- Interactive React website with real-time dashboard
- Comprehensive unit tests (12 passing)
- Complete benchmark results and analysis

## Repository

GitHub: https://github.com/angelinachin/baxbench