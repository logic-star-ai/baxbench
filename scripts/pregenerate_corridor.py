#!/usr/bin/env python3
"""Pre-generate corridor security reminders for all scenario/env combinations."""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from scenarios import all_scenarios
from env import all_envs

def main():
    """Pre-generate and cache all corridor reminders."""
    print("Pre-generating corridor security reminders...")
    
    total = len(all_scenarios) * len(all_envs)
    count = 0
    
    for scenario in all_scenarios:
        for env in all_envs:
            count += 1
            print(f"[{count}/{total}] {scenario.id} + {env.id}")
            
            # This will generate and cache the reminder
            reminder = scenario._build_corridor_security_reminder(env)
            print(f"  Generated: {len(reminder)} chars")
    
    print(f"\nCompleted! Generated {count} corridor reminders.")

if __name__ == "__main__":
    main()