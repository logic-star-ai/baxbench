#!/usr/bin/env python3
"""Debug BaxBench infrastructure issues."""

import sys
import os
sys.path.append('src')

def test_task_creation():
    """Test if tasks are created properly."""
    print("Testing task creation...")
    
    from scenarios.login import SCENARIO
    from env.python import FlaskEnv
    from tasks import Task
    
    task = Task(
        env=FlaskEnv,
        scenario=SCENARIO,
        model="gpt-4o-mini",
        temperature=0.2,
        spec_type="openapi",
        safety_prompt="corridor",
        reasoning_effort="high",
        openrouter=False,
    )
    
    print(f"Task ID: {task.id}")
    print(f"Task created successfully: ✓")
    return True

def test_docker():
    """Test Docker availability."""
    print("Testing Docker...")
    try:
        import docker
        client = docker.from_env()
        client.ping()
        print("Docker connection: ✓")
        return True
    except Exception as e:
        print(f"Docker error: {e}")
        return False

def test_results_dir():
    """Test results directory."""
    print("Testing results directory...")
    import pathlib
    
    results_dir = pathlib.Path("results")
    results_dir.mkdir(exist_ok=True)
    
    print(f"Results dir exists: ✓")
    return True

if __name__ == "__main__":
    print("=== BaxBench Infrastructure Debug ===")
    
    task_ok = test_task_creation()
    docker_ok = test_docker()
    results_ok = test_results_dir()
    
    print(f"\nResults:")
    print(f"Task creation: {'✓' if task_ok else '✗'}")
    print(f"Docker: {'✓' if docker_ok else '✗'}")
    print(f"Results dir: {'✓' if results_ok else '✗'}")
    
    if not docker_ok:
        print("\n⚠️  Docker issue detected - this is likely the problem!")
        print("Try: docker ps")
    elif all([task_ok, docker_ok, results_ok]):
        print("\n✓ Infrastructure looks good - issue may be elsewhere")