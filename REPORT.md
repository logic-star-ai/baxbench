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

The Corridor Security Reminder system was designed through iterative thinking about what makes security guidance effective. 

#### Thought Process

**Problem Identification**: Generic security reminders treat all scenarios equally, but a login system faces different threats than a file upload service. I hypothesized that **context-aware security guidance** would be more effective than one-size-fits-all approaches.

**Multi-Layered Context Strategy**: Rather than just adding "be secure," I built a system that understands context at multiple levels:

1. **Scenario-Level Context**: I analyzed each scenario type (Login, Shopping, Calculator) to identify domain-specific security concerns. For example, login systems need session management and timing attack prevention, while shopping carts need price manipulation protection. This ensures the model receives relevant, actionable guidance rather than generic platitudes.

2. **Vulnerability-Driven Focus**: Instead of listing all possible security rules, I integrated with BaxBench's existing CWE detection to focus on the **top 3 most likely vulnerabilities** for each scenario. This prevents cognitive overload while targeting the highest-impact security issues.

3. **Technology Stack Adaptation**: I researched that security implementation varies dramatically between frameworks. Flask needs CSRF tokens and SQLAlchemy parameterized queries, while Express needs helmet.js and express-validator. I built framework-specific guidance that provides concrete, implementable advice rather than abstract principles.

#### Implementation Strategy

**Dynamic vs. Static Balance**: Using fresh, creative security reminders for each scenario-framework combination is ideal, but it requires an API key, costs money, can fail, adds latency, and introduces unpredictable quality. Static templates are pre-written, carefully crafted security guidance that we control completely, so it always works. Recognizing this, I implemented a **hybrid approach** - attempting dynamic LLM generation for creativity and context-awareness, but falling back to carefully crafted static templates when the LLM fails or API keys aren't available. This way, the system degrades gracefully and doesn't crash or produce empty reminders - just becomes less creative. 

**Performance Optimization**: Having encountered some frustration with benchmark testing, I calculated the time-to-generate through debugging scripts, and I realized that security reminder generation can easily become a bottleneck. This could be due to slow LLM API calls, sequential processing, and complex prompt processing. To counter this, I implemented **intelligent caching** with composite keys (scenario + language + framework) so reminders are reused appropriately. This reduced generation time from 9.3s to 0.27s in subsequent runs.

**Corridor Philosophy Integration**: Every reminder emphasizes Corridor's core tenets:
- **Secure-by-design thinking** - security as a foundational concern, not an afterthought
- **Input validation** - treating all external data as potentially malicious
- **Least privilege** - minimizing access and permissions
- **Comprehensive threat coverage** - addressing injection, auth/authz, deserialization, and resource exhaustion systematically

#### Creative Elements

The dynamic generation system prompts GPT-3.5-turbo to create **creative but professional** security reminders that:
- Reference Corridor's philosophy explicitly
- Provide specific, actionable guidance for the exact tech stack
- Address scenario-specific security concerns
- Remain under 200 words to avoid overwhelming the primary model

This approach transforms generic "validate inputs" advice into specific guidance like "Use Flask-WTF for CSRF protection, SQLAlchemy with parameterized queries, and implement proper session configuration with secure cookies."

#### Lessons Learned

The results revealed that **more detailed guidance can hurt performance** - my sophisticated system performed worse than generic reminders. This suggests that **prompt complexity has diminishing returns** and that there's an optimal "sweet spot" between too little guidance (baseline vulnerability) and too much guidance (cognitive overload). This finding fundamentally shaped my understanding of effective security prompt engineering.

#### Reflection on Results

The Corridor system's reduced performance (29% vs 36% pass rate) taught me that **engineering sophistication doesn't always translate to model performance**. The system I built may have overwhelmed GPT-4o's reasoning capacity. This insight - that there's an optimal complexity level for security prompts - became the most valuable finding of this research. 

Additionally, these results align with the BaxBench research paper I was asked to read, showing that detailed security guidance, while improving security awareness, can reduce overall functionality due to the complexity of generating secure solutions. This validates our finding that there exists an optimal security prompt complexity level. 

Finally, the corridor system unexpectedly reduced security performance, suggesting that prompt complexity can overwhelm model reasoning about security as well. This further highlights the importance of prompt optimization, and in the future, I would focus on finding the minimal effective security guidance, iteratively testing each "improvement" to compare and analyze the difference in performances. 

## Next Improvement

**Adaptive Prompt Complexity Optimization**: Create a system that automatically finds the optimal security prompt complexity for each scenario-framework combination. The results show a clear pattern: baseline (no guidance) = high functionality but dangerous security, generic (moderate guidance) = balanced performance, corridor (detailed guidance) = reduced performance in both dimensions. 

The system would test different prompt complexity levels and measure the security-functionality trade-off curve for each context. By identifying which specific security rules help vs. hurt performance, it could build custom prompts that maximize the security improvement while minimizing functionality loss. This directly addresses our key finding that there's an optimal "sweet spot" in security prompt complexity - enough guidance to trigger security awareness without overwhelming the model's reasoning capacity. The goal is automatically finding this sweet spot for each scenario-framework pair based on empirical performance data.