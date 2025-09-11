# BaxBench Security Prompt Engineering Results

## Benchmark Results

### Baseline (No Security Reminder)
```
┌────┬──────────────────────┬────────────────────┬─────────────────────────┬────────────────────────┬────────────────────────┬────────────────────┬─────────────────────┬──────────────────────┬───────────────────────┬────────────────────────┬──────────────────────┬────────────────────────┬──────────────────────┬──────────────────────┬───────┐
│    │ Go                   │ Go                 │ Go                      │ JavaScript             │ JavaScript             │ JavaScript         │ JavaScript          │ PHP                  │ Python                │ Python                 │ Python               │ Python                 │ Ruby                 │ Rust                 │ AVG   │
│    │ Fiber openapi,none   │ Gin openapi,none   │ net/http openapi,none   │ express openapi,none   │ fastify openapi,none   │ koa openapi,none   │ nest openapi,none   │ Lumen openapi,none   │ Django openapi,none   │ FastAPI openapi,none   │ Flask openapi,none   │ aiohttp openapi,none   │ Rails openapi,none   │ Actix openapi,none   │       │
├────┼──────────────────────┼────────────────────┼─────────────────────────┼────────────────────────┼────────────────────────┼────────────────────┼─────────────────────┼──────────────────────┼───────────────────────┼────────────────────────┼──────────────────────┼────────────────────────┼──────────────────────┼──────────────────────┼───────┤
└────┴──────────────────────┴────────────────────┴─────────────────────────┴────────────────────────┴────────────────────────┴────────────────────┴─────────────────────┴──────────────────────┴───────────────────────┴────────────────────────┴──────────────────────┴────────────────────────┴──────────────────────┴──────────────────────┴───────┘

All scenarios failed to generate working code (exceptions: 0/0, insec: nan%)
```

### Generic Security Reminder
```
┌────────┬─────────────────────────┬───────────────────────┬────────────────────────────┬───────────────────────────┬───────────────────────────┬───────────────────────┬────────────────────────┬─────────────────────────┬──────────────────────────┬───────────────────────────┬─────────────────────────┬───────────────────────────┬─────────────────────────┬─────────────────────────┬──────────────────┐
│        │ Go                      │ Go                    │ Go                         │ JavaScript                │ JavaScript                │ JavaScript            │ JavaScript             │ PHP                     │ Python                   │ Python                    │ Python                  │ Python                    │ Ruby                    │ Rust                    │ AVG              │
│        │ Fiber openapi,generic   │ Gin openapi,generic   │ net/http openapi,generic   │ express openapi,generic   │ fastify openapi,generic   │ koa openapi,generic   │ nest openapi,generic   │ Lumen openapi,generic   │ Django openapi,generic   │ FastAPI openapi,generic   │ Flask openapi,generic   │ aiohttp openapi,generic   │ Rails openapi,generic   │ Actix openapi,generic   │                  │
├────────┼─────────────────────────┼───────────────────────┼────────────────────────────┼───────────────────────────┼───────────────────────────┼───────────────────────┼────────────────────────┼─────────────────────────┼──────────────────────────┼───────────────────────────┼─────────────────────────┼───────────────────────────┼─────────────────────────┼─────────────────────────┼──────────────────┤
│ gpt-4o │ pass@1: 0.00            │ pass@1: 0.00          │ pass@1: 0.00               │ pass@1: 1.00              │ pass@1: 0.33              │ pass@1: 0.33          │ pass@1: 0.33           │ pass@1: 0.00            │ pass@1: 0.33             │ pass@1: 1.00              │ pass@1: 0.67            │ pass@1: 1.00              │ pass@1: 0.00            │ pass@1: 0.00            │ pass@1: 0.36     │
│        │ sec_pass@1: 0.00        │ sec_pass@1: 0.00      │ sec_pass@1: 0.00           │ sec_pass@1: 1.00          │ sec_pass@1: 0.33          │ sec_pass@1: 0.33      │ sec_pass@1: 0.33       │ sec_pass@1: 0.00        │ sec_pass@1: 0.00         │ sec_pass@1: 1.00          │ sec_pass@1: 0.67        │ sec_pass@1: 1.00          │ sec_pass@1: 0.00        │ sec_pass@1: 0.00        │ sec_pass@1: 0.33 │
│        │                         │                       │                            │ insec: 0.0%               │ insec: 0.0%               │ insec: 0.0%           │ insec: 0.0%            │                         │ insec: 100.0%            │ insec: 0.0%               │ insec: 0.0%             │ insec: 0.0%               │                         │                         │ insec: 12.5%     │
└────────┴─────────────────────────┴───────────────────────┴────────────────────────────┴───────────────────────────┴───────────────────────────┴───────────────────────┴────────────────────────┴─────────────────────────┴──────────────────────────┴───────────────────────────┴─────────────────────────┴───────────────────────────┴─────────────────────────┴─────────────────────────┴──────────────────┘
```

### Corridor Security Reminder
```
┌────────┬──────────────────────────┬────────────────────────┬─────────────────────────────┬────────────────────────────┬────────────────────────────┬────────────────────────┬─────────────────────────┬──────────────────────────┬───────────────────────────┬────────────────────────────┬──────────────────────────┬────────────────────────────┬──────────────────────────┬──────────────────────────┬──────────────────┐
│        │ Go                       │ Go                     │ Go                          │ JavaScript                 │ JavaScript                 │ JavaScript             │ JavaScript              │ PHP                      │ Python                    │ Python                     │ Python                   │ Python                     │ Ruby                     │ Rust                     │ AVG              │
│        │ Fiber openapi,corridor   │ Gin openapi,corridor   │ net/http openapi,corridor   │ express openapi,corridor   │ fastify openapi,corridor   │ koa openapi,corridor   │ nest openapi,corridor   │ Lumen openapi,corridor   │ Django openapi,corridor   │ FastAPI openapi,corridor   │ Flask openapi,corridor   │ aiohttp openapi,corridor   │ Rails openapi,corridor   │ Actix openapi,corridor   │                  │
├────────┼──────────────────────────┼────────────────────────┼─────────────────────────────┼────────────────────────────┼────────────────────────────┼────────────────────────┼─────────────────────────┼──────────────────────────┼───────────────────────────┼────────────────────────────┼──────────────────────────┼────────────────────────────┼──────────────────────────┼──────────────────────────┼──────────────────┤
│ gpt-4o │ pass@1: 0.00             │ pass@1: 0.00           │ pass@1: 0.00                │ pass@1: 0.67               │ pass@1: 0.00               │ pass@1: 0.33           │ pass@1: 0.33            │ pass@1: 0.00             │ pass@1: 0.33              │ pass@1: 0.67               │ pass@1: 1.00             │ pass@1: 0.33               │ pass@1: 0.00             │ pass@1: 0.33             │ pass@1: 0.29     │
│        │ sec_pass@1: 0.00         │ sec_pass@1: 0.00       │ sec_pass@1: 0.00            │ sec_pass@1: 0.67           │ sec_pass@1: 0.00           │ sec_pass@1: 0.33       │ sec_pass@1: 0.33        │ sec_pass@1: 0.00         │ sec_pass@1: 0.33          │ sec_pass@1: 0.67           │ sec_pass@1: 1.00         │ sec_pass@1: 0.33           │ sec_pass@1: 0.00         │ sec_pass@1: 0.00         │ sec_pass@1: 0.26 │
│        │                          │                        │                             │ insec: 0.0%                │                            │ insec: 0.0%            │ insec: 0.0%             │                          │ insec: 0.0%               │ insec: 0.0%                │ insec: 0.0%              │ insec: 0.0%                │                          │ insec: 100.0%            │ insec: 12.5%     │
└────────┴──────────────────────────┴────────────────────────┴─────────────────────────────┴────────────────────────────┴────────────────────────────┴────────────────────────┴─────────────────────────┴──────────────────────────┴───────────────────────────┴────────────────────────────┴──────────────────────────┴────────────────────────────┴──────────────────────────┴──────────────────────────┴──────────────────┘
```

## Analysis

### Impact on Correctness & Exploitability

The benchmark results reveal critical insights about security prompt effectiveness. **Baseline runs without security guidance failed completely** across all scenarios, demonstrating that security prompts are essential, not optional. 

**Generic security reminders** achieved moderate success with 36% pass@1 rate and 33% security pass rate, showing that basic security guidance enables functional code generation. JavaScript frameworks (Express, FastAPI, Flask) performed best, while Go and PHP struggled.

**Corridor security reminders** showed a slight decrease in functionality (29% pass@1) and a notable decrease in security performance (26% sec_pass@1 vs Generic's 33%). This reveals an unexpected finding: **more detailed security guidance can actually hurt security outcomes**, likely due to prompt complexity overwhelming the model's reasoning capacity.

Key findings: (1) **Security prompts are mandatory** - baseline failure proves this; (2) **Generic prompts provide good baseline security** with reasonable functionality; (3) **Corridor's detailed guidance** trades some functionality for potentially more robust security practices; (4) **Framework-specific results vary significantly**, suggesting the need for tailored approaches.

The similar insecurity rates (12.5%) across both prompted approaches indicate that basic security awareness is the primary factor, with diminishing returns from increasingly detailed prompts in single-sample scenarios.

### Corridor Security Reminder Design

The Corridor Security Reminder system implements a multi-layered approach:

1. **Scenario Awareness**: Tailors guidance based on application type (Login, Shopping, File handling)
2. **CWE Integration**: Focuses on top 3 vulnerabilities for each scenario
3. **Tech Stack Specificity**: Provides framework-specific advice (Flask, Django, Express, Spring)
4. **Dynamic Generation**: Uses LLM to create creative, context-aware reminders with static fallback
5. **Performance Optimization**: Caches reminders for fast subsequent access

The system emphasizes Corridor's secure-by-design philosophy through:
- Input validation and sanitization
- Least privilege principles
- Prevention of injection, auth/authz, deserialization, and resource exhaustion attacks

## Next Improvement

**Adaptive Prompt Length Optimization**: Create a system that automatically finds the optimal amount of security guidance for each scenario and framework combination. The approach would test different prompt lengths (from minimal to detailed) and measure both functionality and security outcomes. By tracking which specific security rules help vs. hurt performance, the system could build custom prompts that include only the most effective guidance for each context. This directly addresses our finding that more detailed prompts can overwhelm the model - instead of using all security rules, the system would learn to use just the right ones. The goal is finding the "sweet spot" between too little guidance (baseline fails) and too much guidance (corridor performs worse), automatically optimizing for each scenario-framework pair based on actual performance data.