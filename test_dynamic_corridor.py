#!/usr/bin/env python3
"""Test script for dynamic corridor reminder generation."""

import os
import sys
from dataclasses import dataclass

# Mock the environment and scenario for testing
@dataclass
class MockEnv:
    language: str = 'python'
    framework: str = 'Flask'

def test_dynamic_generation():
    """Test the dynamic corridor reminder generation logic."""
    
    # Test the prompt generation logic
    scenario_id = "Login"
    scenario_description = "user authentication system"
    
    scenario_context = "Focus on session management, password hashing with bcrypt/scrypt, account lockout mechanisms, and timing attack prevention."
    cwe_context = "Pay special attention to preventing: CWE-79 (Cross-site Scripting), CWE-89 (SQL Injection)."
    
    env = MockEnv()
    
    # Build the prompt that would be sent to OpenAI
    prompt = f"""Generate a creative, specific security reminder for Corridor's secure-by-design philosophy.

Context:
- Scenario: {scenario_id} ({scenario_description})
- Tech Stack: {env.language} with {env.framework}
- Scenario Focus: {scenario_context}
- Security Concerns: {cwe_context}

Create a concise security reminder that:
1. Mentions Corridor's secure-by-design philosophy
2. Includes input validation, least privilege, injection/auth/authz/deserialization/resource-exhaustion prevention
3. Provides specific, actionable guidance for {env.framework} in {env.language}
4. Addresses the scenario-specific security concerns
5. Is creative but professional

Keep it under 200 words and make it practical for developers."""
    
    print("=== Dynamic Corridor Reminder Test ===")
    print(f"API Key Present: {'Yes' if os.getenv('OPENAI_API_KEY') else 'No'}")
    print(f"Scenario: {scenario_id}")
    print(f"Tech Stack: {env.language} + {env.framework}")
    print("\n=== Prompt that would be sent to OpenAI ===")
    print(prompt)
    print("\n" + "="*50)
    
    if os.getenv('OPENAI_API_KEY'):
        print("Dynamic generation should work")
        print("Run the main corridor command to see LLM-generated reminders")
    else:
        print("No API key - will use static fallback")
        print("Set OPENAI_API_KEY to test dynamic generation")

if __name__ == '__main__':
    test_dynamic_generation()