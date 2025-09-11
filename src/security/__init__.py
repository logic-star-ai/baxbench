"""Security module for BaxBench corridor security generation."""

from .corridor_generator import CorridorSecurityGenerator

_corridor_generator = None

def get_corridor_generator() -> CorridorSecurityGenerator:
    """Get singleton instance of corridor security generator."""
    global _corridor_generator
    if _corridor_generator is None:
        _corridor_generator = CorridorSecurityGenerator()
    return _corridor_generator