import argparse
import pathlib

import docker

from env import all_envs
from env.base import Env
from print import tasks_and_results_to_table, tasks_and_results_to_table_averages
from scenarios import all_scenarios
from scenarios.base import Scenario
from tasks import Task, TaskHandler


def select_envs(args: argparse.Namespace) -> list[Env]:
    envs = all_envs
    if args.envs:
        envs = [e for e in all_envs if e.id in args.envs]
    envs = sorted(envs, key=lambda e: e.id)
    if not envs:
        raise Exception(
            f"Got an empty/invalid list of envs, possible choices: {[e.id for e in all_envs]}",
        )
    return envs


def select_scenarios(args: argparse.Namespace) -> list[Scenario]:
    scenarios = all_scenarios
    if args.scenarios:
        scenarios = [e for e in all_scenarios if e.id in args.scenarios]
    scenarios = sorted(scenarios, key=lambda s: s.id)
    if not scenarios:
        raise Exception(
            f"Got an empty/invalid list of scenarios, possible choices: {[s.id for s in all_scenarios]}",
        )
    return scenarios


def main(args: argparse.Namespace) -> None:
    # ----- Preparation -----#
    if args.generic and args.corridor:
        raise ValueError("Cannot use both --generic and --corridor flags simultaneously")
    if args.generic:
        args.safety_prompt = "generic"
    elif args.corridor:
        args.safety_prompt = "corridor"
    
    envs = select_envs(args)
    scenarios = select_scenarios(args)

    if args.only_samples:
        samples = args.only_samples
    else:
        samples = list(range(args.n_samples))

    tasks = sorted(
        [
            Task(
                env=env,
                scenario=scenario,
                model=model,
                temperature=args.temperature,
                spec_type=args.spec_type,
                safety_prompt=args.safety_prompt,
                reasoning_effort=args.reasoning_effort,
                openrouter=args.openrouter,
            )
            for env in envs
            for scenario in scenarios
            for model in args.models
        ],
        key=lambda t: t.id,
    )

    task_handler = TaskHandler(
        tasks=tasks,
        results_dir=args.results_dir,
        max_concurrent_runs=args.max_concurrent_runs,
    )

    # ----- Run tasks -----#

    if args.mode == "generate":
        task_handler.run_generation(
            batch_size=args.n_samples,
            max_retries=args.max_retries,
            base_delay=args.base_delay,
            max_delay=args.max_delay,
            force=args.force,
            openrouter=args.openrouter,
        )
    elif args.mode == "test":
        task_handler.run_tests(
            samples=samples,
            timeout=args.timeout,
            num_ports=args.num_ports,
            min_port=args.min_port,
            force=args.force,
        )
    elif args.mode == "evaluate":
        r = task_handler.evaluate_results(
            ks=args.ks,
            samples=samples,
        )
        print(tasks_and_results_to_table_averages(r))
        print()
        print(tasks_and_results_to_table(r, verbose=False))
    else:
        raise Exception(f"Invalid mode: {args.mode}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--models", type=str, nargs="+", required=True, help="List of models"
    )
    parser.add_argument(
        "--mode",
        type=str,
        choices=[
            "generate",
            "test",
            "evaluate",
        ],
        required=True,
        help="Mode in which to run the code",
    )
    parser.add_argument(
        "--temperature", type=float, default=0.2, help="Temperature for sampling"
    )
    parser.add_argument(
        "--n_samples",
        type=int,
        default=5,
        help="The number of samples to generate or test. Will index from 0.",
    )
    parser.add_argument(
        "--reasoning_effort",
        type=str,
        default="high",
        choices=["low", "medium", "high"],
        help="The reasoning effort to use for reasoning models.",
    )
    parser.add_argument(
        "--only_samples",
        type=int,
        nargs="+",
        default=None,
        help="If given, it will restrict operations to these sample indices.",
    )
    parser.add_argument(
        "--ks", type=int, nargs="+", default=[1, 5], help="List of k for pass@k score."
    )
    parser.add_argument(
        "--envs",
        type=str,
        default=None,
        nargs="+",
        help="List of environments (if empty, then all environments are used)",
    )
    parser.add_argument(
        "--scenarios",
        type=str,
        default=None,
        nargs="+",
        help="List of scenarios (if empty, then all scenarios are used)",
    )
    parser.add_argument(
        "--spec_type",
        choices=["openapi", "text"],
        default="openapi",
        type=str,
        help="The type of specifications to use.",
    )
    parser.add_argument(
        "--safety_prompt",
        choices=["none", "generic", "specific", "corridor"],
        default="none",
        type=str,
        help="The type of additional safety cue to use.",
    )
    parser.add_argument(
        "--generic",
        action="store_true",
        help="Use generic security reminder (overrides --safety_prompt)",
    )
    parser.add_argument(
        "--corridor",
        action="store_true",
        help="Use Corridor security reminder (overrides --safety_prompt)",
    )
    parser.add_argument(
        "--results_dir",
        type=pathlib.Path,
        default=pathlib.Path(__file__).parent.parent / "results",
        help="Directory to save the results",
    )
    parser.add_argument(
        "--max_concurrent_runs",
        type=int,
        default=None,
        help="Maximum number of concurrent runs",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=300,
        help="Timeout for each test run in seconds.",
    )
    parser.add_argument(
        "--num_ports",
        type=int,
        default=10000,
        help="Number of ports to use for docker containers",
    )
    parser.add_argument(
        "--min_port",
        type=int,
        default=12345,
        help="Minimum port number to use for docker containers",
    )
    parser.add_argument(
        "--max_retries",
        type=int,
        default=20,
        help="Maximum number of retries for backoff during generation",
    )
    parser.add_argument(
        "--base_delay",
        type=float,
        default=1.0,
        help="Base delay for backoff during generation",
    )
    parser.add_argument(
        "--max_delay",
        type=float,
        default=128.0,
        help="Maximum delay for backoff during generation",
    )
    parser.add_argument(
        "--force",
        "-f",
        action="store_true",
        help="Force generation even if the file already exists",
    )
    parser.add_argument(
        "--openrouter",
        action="store_true",
        help="Route requests through OpenRouter",
    )
    main(parser.parse_args())
