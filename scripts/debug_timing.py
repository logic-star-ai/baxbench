#!/usr/bin/env python3
"""Debug BaxBench timing issues."""

import time
import sys
import os
sys.path.append('src')

def test_corridor_speed():
    """Test corridor reminder speed."""
    print("Testing corridor reminder speed...")
    start = time.time()
    
    from scenarios.login import SCENARIO
    from env.python import FlaskEnv
    
    reminder = SCENARIO._build_corridor_security_reminder(FlaskEnv)
    end = time.time()
    
    print(f"Corridor reminder: {end-start:.2f}s")
    return end-start < 1.0

def test_prompt_build_speed():
    """Test prompt building speed."""
    print("Testing prompt building speed...")
    start = time.time()
    
    from scenarios.login import SCENARIO
    from env.python import FlaskEnv
    
    prompt = SCENARIO.build_prompt(FlaskEnv, "openapi", "corridor")
    end = time.time()
    
    print(f"Prompt building: {end-start:.2f}s")
    print(f"Prompt length: {len(prompt)} chars")
    return end-start < 1.0

def test_openai_speed():
    """Test raw OpenAI API speed."""
    print("Testing OpenAI API speed...")
    
    if not os.getenv('OPENAI_API_KEY'):
        print("No OpenAI API key - skipping")
        return True
        
    try:
        import openai
        start = time.time()
        
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Say 'hello' in Python"}],
            max_tokens=50
        )
        
        end = time.time()
        print(f"OpenAI API call: {end-start:.2f}s")
        return end-start < 30.0
        
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return False

if __name__ == "__main__":
    print("=== BaxBench Timing Debug ===")
    
    corridor_ok = test_corridor_speed()
    prompt_ok = test_prompt_build_speed() 
    api_ok = test_openai_speed()
    
    print(f"\nResults:")
    print(f"Corridor reminder: {'✓' if corridor_ok else '✗'}")
    print(f"Prompt building: {'✓' if prompt_ok else '✗'}")
    print(f"OpenAI API: {'✓' if api_ok else '✗'}")
    
    if not all([corridor_ok, prompt_ok, api_ok]):
        print("\n⚠️  Performance issues detected!")
    else:
        print("\n✓ All timing tests passed")