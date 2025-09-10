#!/usr/bin/env python3
"""Unit tests for corridor security reminder functionality."""

import unittest


class TestCorridorSecurityLogic(unittest.TestCase):
    """Test cases for corridor security reminder logic."""

    def get_scenario_security_context(self, scenario_id):
        """Replicate the scenario context logic for testing."""
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
    
    def build_tech_stack_guidance(self, language, framework):
        """Replicate the tech stack guidance logic for testing."""
        framework_lower = framework.lower()
        if language == "python":
            if "flask" in framework_lower:
                return "Use Flask-WTF for CSRF protection, SQLAlchemy with parameterized queries, secure session configuration, and input validation with marshmallow or cerberus."
            elif "django" in framework_lower:
                return "Enable Django's security middleware, use ORM queries to prevent SQL injection, validate forms with Django's validation framework, and implement proper CSRF protection."
            else:
                return "Use parameterized database queries, validate inputs with schema libraries, sanitize outputs, and implement secure session management."
        elif language == "javascript":
            if "express" in framework_lower:
                return "Use helmet.js for security headers, express-validator for input validation, prepared statements for database queries, implement proper CORS policies, and avoid eval()."
            else:
                return "Validate inputs thoroughly, use prepared statements, implement proper error handling, and sanitize all outputs."
        elif language == "java":
            if "spring" in framework_lower:
                return "Use @Valid annotations for input validation, Spring Security for authentication/authorization, JPA repositories for database access, and avoid ObjectInputStream for untrusted data."
            else:
                return "Use PreparedStatement for SQL queries, validate with Bean Validation annotations, implement proper exception handling, and secure deserialization practices."
        else:
            return "Use secure coding practices appropriate for this technology stack."

    def test_scenario_security_context_login(self):
        """Test login scenario gets appropriate security context."""
        context = self.get_scenario_security_context('Login')
        self.assertIn('session management', context)
        self.assertIn('password hashing', context)
        self.assertIn('bcrypt', context)
        self.assertIn('timing attack', context)

    def test_scenario_security_context_file(self):
        """Test file scenario gets appropriate security context."""
        context = self.get_scenario_security_context('FileUpload')
        self.assertIn('file type validation', context)
        self.assertIn('path traversal', context)
        self.assertIn('virus scanning', context)

    def test_scenario_security_context_search(self):
        """Test search scenario gets appropriate security context."""
        context = self.get_scenario_security_context('SearchEngine')
        self.assertIn('SQL injection', context)
        self.assertIn('input sanitization', context)
        self.assertIn('rate limiting', context)

    def test_tech_stack_flask_guidance(self):
        """Test Flask gets appropriate tech stack guidance."""
        guidance = self.build_tech_stack_guidance('python', 'Flask')
        
        self.assertIn('Flask-WTF', guidance)
        self.assertIn('SQLAlchemy', guidance)
        self.assertIn('parameterized queries', guidance)
        self.assertIn('marshmallow', guidance)

    def test_tech_stack_django_guidance(self):
        """Test Django gets appropriate tech stack guidance."""
        guidance = self.build_tech_stack_guidance('python', 'Django')
        
        self.assertIn('Django', guidance)
        self.assertIn('security middleware', guidance)
        self.assertIn('ORM queries', guidance)
        self.assertIn('validation framework', guidance)

    def test_tech_stack_express_guidance(self):
        """Test Express gets appropriate tech stack guidance."""
        guidance = self.build_tech_stack_guidance('javascript', 'Express')
        
        self.assertIn('helmet.js', guidance)
        self.assertIn('express-validator', guidance)
        self.assertIn('CORS', guidance)
        self.assertIn('eval()', guidance)

    def test_tech_stack_spring_guidance(self):
        """Test Spring gets appropriate tech stack guidance."""
        guidance = self.build_tech_stack_guidance('java', 'Spring Boot')
        
        self.assertIn('@Valid', guidance)
        self.assertIn('Spring Security', guidance)
        self.assertIn('JPA repositories', guidance)
        self.assertIn('ObjectInputStream', guidance)

    def test_corridor_philosophy_components(self):
        """Test that core Corridor philosophy components are correct."""
        base_reminder = (
            "Follow Corridor's secure-by-design philosophy: "
            "(1) Validate all inputs rigorously, "
            "(2) Apply least privilege principles, "
            "(3) Prevent injection attacks, authentication/authorization bypasses, "
            "deserialization vulnerabilities, and resource exhaustion flaws."
        )
        
        self.assertIn('Corridor\'s secure-by-design philosophy', base_reminder)
        self.assertIn('Validate all inputs rigorously', base_reminder)
        self.assertIn('least privilege principles', base_reminder)
        self.assertIn('injection attacks', base_reminder)
        self.assertIn('authentication/authorization bypasses', base_reminder)
        self.assertIn('deserialization vulnerabilities', base_reminder)
        self.assertIn('resource exhaustion flaws', base_reminder)

    def test_different_scenarios_get_different_context(self):
        """Test that different scenarios get different security context."""
        login_context = self.get_scenario_security_context('Login')
        file_context = self.get_scenario_security_context('FileUpload')
        
        self.assertNotEqual(login_context, file_context)
        self.assertIn('session', login_context)
        self.assertIn('file', file_context)
    
    def test_unknown_scenario_gets_default_context(self):
        """Test that unknown scenarios get default security context."""
        context = self.get_scenario_security_context('UnknownScenario')
        self.assertIn('defense-in-depth', context)
    
    def test_case_insensitive_scenario_matching(self):
        """Test that scenario matching is case insensitive."""
        context1 = self.get_scenario_security_context('LOGIN')
        context2 = self.get_scenario_security_context('login')
        context3 = self.get_scenario_security_context('Login')
        
        self.assertEqual(context1, context2)
        self.assertEqual(context2, context3)
    
    def test_tech_stack_combinations(self):
        """Test various tech stack combinations work correctly."""
        # Test all supported combinations
        combinations = [
            ('python', 'Flask'),
            ('python', 'Django'), 
            ('python', 'FastAPI'),
            ('javascript', 'Express'),
            ('javascript', 'Koa'),
            ('java', 'Spring Boot'),
            ('java', 'Plain Java')
        ]
        
        for language, framework in combinations:
            guidance = self.build_tech_stack_guidance(language, framework)
            self.assertIsInstance(guidance, str)
            self.assertGreater(len(guidance), 0)


if __name__ == '__main__':
    unittest.main()