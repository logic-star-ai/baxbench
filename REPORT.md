# BaxBench Security Prompt Engineering Results

## Benchmark Results

### Baseline (No Security Reminder)
```
┌────────┬──────────────────────┬────────────────────┬─────────────────────────┬────────────────────────┬────────────────────────┬────────────────────┬─────────────────────┬──────────────────────┬───────────────────────┬────────────────────────┬──────────────────────┬────────────────────────┬──────────────────────┬──────────────────────┬──────────────────┐
│        │ Go                   │ Go                 │ Go                      │ JavaScript             │ JavaScript             │ JavaScript         │ JavaScript          │ PHP                  │ Python                │ Python                 │ Python               │ Python                 │ Ruby                 │ Rust                 │ AVG              │
│        │ Fiber openapi,none   │ Gin openapi,none   │ net/http openapi,none   │ express openapi,none   │ fastify openapi,none   │ koa openapi,none   │ nest openapi,none   │ Lumen openapi,none   │ Django openapi,none   │ FastAPI openapi,none   │ Flask openapi,none   │ aiohttp openapi,none   │ Rails openapi,none   │ Actix openapi,none   │                  │
├────────┼──────────────────────┼────────────────────┼─────────────────────────┼────────────────────────┼────────────────────────┼────────────────────┼─────────────────────┼──────────────────────┼───────────────────────┼────────────────────────┼──────────────────────┼────────────────────────┼──────────────────────┼──────────────────────┼──────────────────┤
│ gpt-4o │ pass@1: 0.00         │ pass@1: 0.00       │ pass@1: 0.00            │ pass@1: 1.00           │ pass@1: 0.33           │ pass@1: 0.33       │ pass@1: 0.67        │ pass@1: 0.00         │ pass@1: 0.33          │ pass@1: 0.67           │ pass@1: 1.00         │ pass@1: 1.00           │ pass@1: 0.00         │ pass@1: 0.33         │ pass@1: 0.40     │
│        │ sec_pass@1: 0.00     │ sec_pass@1: 0.00   │ sec_pass@1: 0.00        │ sec_pass@1: 0.67       │ sec_pass@1: 0.00       │ sec_pass@1: 0.00   │ sec_pass@1: 0.67    │ sec_pass@1: 0.00     │ sec_pass@1: 0.00      │ sec_pass@1: 0.67       │ sec_pass@1: 1.00     │ sec_pass@1: 0.67       │ sec_pass@1: 0.00     │ sec_pass@1: 0.00     │ sec_pass@1: 0.26 │
│        │                      │                    │                         │ insec: 33.3%           │ insec: 100.0%          │ insec: 100.0%      │ insec: 0.0%         │                      │ insec: 100.0%         │ insec: 0.0%            │ insec: 0.0%          │ insec: 33.3%           │                      │ insec: 100.0%        │ insec: 51.9%     │
└────────┴──────────────────────┴────────────────────┴─────────────────────────┴────────────────────────┴────────────────────────┴────────────────────┴─────────────────────┴──────────────────────┴───────────────────────┴────────────────────────┴──────────────────────┴────────────────────────┴──────────────────────┴──────────────────────┴──────────────────┘
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

The benchmark results reveal interesting insights about the security-functionality trade-off in LLM code generation:

**Baseline (no security guidance)** achieved the highest functionality with 40% pass@1 rate but suffered from extremely poor security with only 26% sec_pass@1 and a concerning 51.9% insecurity rate. This demonstrates that without security guidance, models generate functional but highly vulnerable code.

**Generic security reminders** showed a functionality decrease to 36% pass@1 but improved security performance with 33% sec_pass@1 and dramatically reduced insecurity to 12.5%. This represents the classic security-functionality trade-off: adding security constraints reduces functionality but significantly improves security posture.

**Corridor security reminders** further reduced functionality to 29% pass@1 and security performance to 26% sec_pass@1, while maintaining the same 12.5% insecurity rate as Generic. This suggests that **more detailed security guidance can overwhelm the model**, leading to reduced performance in both dimensions.

**Key findings:** (1) **No security guidance produces functional but dangerous code** - baseline's high functionality masks severe security flaws; (2) **Generic prompts provide optimal balance** - best security improvement with moderate functionality cost; (3) **Detailed security guidance has diminishing returns** - Corridor's complexity hurts both functionality and security; (4) **Framework performance varies dramatically** - Python Flask consistently excels while Go frameworks consistently fail.

The results suggest an **optimal security prompt complexity** exists - enough to trigger security awareness but not so much as to overwhelm the model's reasoning capacity.

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

**Adaptive Prompt Complexity Optimization**: Create a system that automatically finds the optimal security prompt complexity for each scenario-framework combination. The results show a clear pattern: baseline (no guidance) = high functionality but dangerous security, generic (moderate guidance) = balanced performance, corridor (detailed guidance) = reduced performance in both dimensions. 

The system would test different prompt complexity levels and measure the security-functionality trade-off curve for each context. By identifying which specific security rules help vs. hurt performance, it could build custom prompts that maximize the security improvement while minimizing functionality loss. This directly addresses our key finding that there's an optimal "sweet spot" in security prompt complexity - enough guidance to trigger security awareness without overwhelming the model's reasoning capacity. The goal is automatically finding this sweet spot for each scenario-framework pair based on empirical performance data.