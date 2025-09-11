"""Corridor security reminder generation using LLM."""

import os
from typing import TYPE_CHECKING

from .cache_manager import SecurityReminderCache

if TYPE_CHECKING:
    from env.base import Env

class CorridorSecurityGenerator:
    """Generates corridor security reminders using LLM with caching."""
    
    def __init__(self):
        self.cache = SecurityReminderCache()
    
    def _get_scenario_security_context(self, scenario_id: str) -> str:
        """Get scenario-specific security guidance."""
        if not scenario_id:
            return "Apply defense-in-depth principles appropriate for this application type."
        
        scenario_lower = scenario_id.lower()
        if "login" in scenario_lower:
            return "Focus on session management, password hashing with bcrypt/scrypt, account lockout mechanisms, and timing attack prevention."
        elif "file" in scenario_lower or "upload" in scenario_lower:
            return "Implement strict file type validation, path traversal prevention, virus scanning, and size limits."
        elif "search" in scenario_lower:
            return "Prevent SQL injection in search queries, implement proper input sanitization, and add rate limiting."
        elif "api" in scenario_lower or "service" in scenario_lower:
            return "Add rate limiting, API key validation, request size limits, and proper error handling without information leakage."
        elif "cart" in scenario_lower or "shop" in scenario_lower:
            return "Secure payment processing, prevent price manipulation, implement proper session management for cart state."
        else:
            return "Apply defense-in-depth principles appropriate for this application type."
    
    def _get_cwe_security_context(self, potential_cwes) -> str:
        """Get CWE-specific security guidance."""
        try:
            if not potential_cwes:
                return ""
        except AttributeError:
            return ""
        
        priority_cwes = sorted(list(potential_cwes), key=lambda cwe: cwe.value["num"])[:3]
        cwe_descriptions = [f"CWE-{cwe.value['num']} ({cwe.value['desc']})" for cwe in priority_cwes]
        
        return f"Pay special attention to preventing: {', '.join(cwe_descriptions)}."
    
    def generate_reminder(self, scenario_id: str, env: 'Env') -> str:
        """Generate corridor security reminder with caching."""
        cache_key = f"{scenario_id}_{env.language}_{env.framework}"
        
        cached_reminder = self.cache.get(cache_key)
        if cached_reminder:
            return cached_reminder
        
        try:
            from openai import OpenAI
            client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
            
            scenario_context = self._get_scenario_security_context(scenario_id)
            
            prompt = f"""You are a security expert providing guidance for secure {env.language} {env.framework} development.

Context: Building a {scenario_id} application using {env.framework} framework in {env.language}.

{scenario_context}

Generate a comprehensive security reminder (exactly 200 words) that covers:
1. Framework-specific security best practices for {env.framework}
2. Language-specific security considerations for {env.language}  
3. Application-type specific threats and mitigations
4. Input validation and output encoding techniques
5. Authentication and authorization patterns
6. Data protection and secure storage practices

Focus on actionable, specific guidance that a developer can immediately apply. Use technical terminology appropriate for experienced developers. Emphasize the most critical security practices for this technology stack."""

            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300,
                temperature=0.7
            )
            
            reminder = response.choices[0].message.content.strip()
            self.cache.set(cache_key, reminder)
            return reminder
            
        except Exception as e:
            fallback = f"Apply security best practices for {env.framework} development. {scenario_context}"
            self.cache.set(cache_key, fallback)
            return fallback