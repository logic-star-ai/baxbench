# BaxBench Website

Interactive web interface for running BaxBench security benchmarks.

## Features

- **Run Tab**: Configure and execute benchmarks with real-time output
  - Multi-select scenarios (Login, Shopping, FileUpload)
  - Model selection (GPT-4o-mini, GPT-4o, Claude)
  - Prompt type toggles (baseline, generic, corridor)
  - Streaming command output

- **Results Tab**: Visualize benchmark results
  - Interactive charts comparing all three modes
  - Key insights about prompt complexity paradox
  - Detailed metrics breakdown

## Quick Start

```bash
cd website
./start.sh
```

This will:
1. Start Python backend server on port 8000
2. Install React dependencies (if needed)
3. Start frontend on port 3000
4. Open http://localhost:3000 in your browser

## Manual Setup

Backend:
```bash
python3 server.py
```

Frontend:
```bash
npm install
npm start
```

## Architecture

- **Frontend**: React SPA with tabs, forms, and charts
- **Backend**: Python HTTP server that shells out to BaxBench CLI
- **Communication**: REST API with streaming for real-time output
- **Results**: Loads existing result files or shows hardcoded data from REPORT.md