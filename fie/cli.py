"""
Command-Line Interface (CLI) for Frontier Intelligence Engine (FIE).
Provides direct terminal access for task execution, prompt inspection,
benchmark testing, and memory management.
"""

import argparse
import sys
import json
import logging
from typing import List, Optional

from fie.config import FIEConfig
from fie.core.loader import ModularPromptLoader
from fie.core.orchestrator import MasterOrchestrator
from fie.evaluation.runner import BenchmarkRunner
from fie.memory.sqlite_memory import SQLiteMemory

def setup_logging(verbose: bool = False) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S"
    )

def handle_run(args: argparse.Namespace) -> None:
    print(f"\n[FIE ENGINE] Initializing Task Workflow...")
    print(f"Task: {args.task}")
    print(f"Model Profile: {args.model_profile}\n")

    orchestrator = MasterOrchestrator()
    result = orchestrator.execute_workflow(
        task_prompt=args.task,
        session_id=args.session_id,
        model_tier=args.model_profile
    )

    print("=" * 60)
    print(f"Workflow Complete | Status: {result['final_status']}")
    print(f"Task Type: {result['task_type'].upper()} | Complexity: {result['complexity']}/10")
    print(f"Pipeline Executed: {' -> '.join([s.upper() for s in result['pipeline']])}")
    print("=" * 60)

    for step in result["steps"]:
        print(f"\n--- STEP {step['step']}: [{step['agent'].upper()}] ---")
        verif = step["verification"]
        print(f"Verification Status: {verif['status']} (Grade: {verif.get('grade', 'N/A')})")
        if verif.get("issues"):
            print(f"Issues: {verif['issues']}")
        if verif.get("warnings"):
            print(f"Warnings: {verif['warnings']}")
        print("\nDeliverable Preview:")
        preview = step["output"].strip()
        if len(preview) > 500:
            preview = preview[:500] + "\n... [truncated]"
        print(preview)
        print("-" * 60)

def handle_inspect_prompt(args: argparse.Namespace) -> None:
    loader = ModularPromptLoader()
    prompt = loader.compile_system_instruction(
        task_type=args.task_type,
        model_profile_tier=args.model_profile,
        active_agent=args.agent
    )
    print("=" * 60)
    print(f"FIE COMPILED MASTER SYSTEM INSTRUCTION")
    print(f"Task Type: {args.task_type} | Agent: {args.agent or 'default'} | Profile: {args.model_profile}")
    print(f"Estimated Tokens: {loader.adaptive_engine.estimate_token_count(prompt)}")
    print("=" * 60)
    print(prompt)

def handle_benchmark(args: argparse.Namespace) -> None:
    print("\n[FIE BENCHMARK] Executing Internal Quality & Performance Suites...")
    runner = BenchmarkRunner()

    if args.category == "coding":
        res = runner.run_coding_suite()
        print(f"\nCoding Suite Score: {res['correctness_score']}% ({res['passed_cases']}/{res['total_cases']} Passed)")
        for d in res["details"]:
            status_symbol = "[PASS]" if d["passed"] else "[FAIL]"
            print(f"  {status_symbol} {d['id']}: {d['name']} ({d['status']})")
    elif args.category == "memory":
        res = runner.run_memory_adherence_suite()
        print(f"\nMemory Suite Score: {res['correctness_score']}% ({res['passed_cases']}/{res['total_cases']} Passed)")
        for d in res["details"]:
            status_symbol = "[PASS]" if d["passed"] else "[FAIL]"
            print(f"  {status_symbol} {d['test']}")
    else:
        full = runner.run_full_benchmark()
        print("\n" + "=" * 60)
        print(f"FIE BENCHMARK COMPOSITE REPORT")
        print(f"Overall Score : {full['final_score']}%")
        print(f"Quality Grade : {full['grade']}")
        print("-" * 60)
        print(f"Correctness   : {full['metrics']['correctness']}%")
        print(f"Completeness  : {full['metrics']['completeness']}%")
        print(f"Adherence     : {full['metrics']['adherence']}%")
        print(f"Efficiency    : {full['metrics']['efficiency']}%")
        print("=" * 60)
        for suite in full["suites"]:
            print(f"\nSuite: {suite['category']} -> {suite['correctness_score']}% Passed ({suite['passed_cases']}/{suite['total_cases']})")
            for d in suite["details"]:
                name = d.get("name") or d.get("test", "test")
                symbol = "[PASS]" if d["passed"] else "[FAIL]"
                print(f"   {symbol} {name}")

def handle_memory(args: argparse.Namespace) -> None:
    mem = SQLiteMemory()
    if args.action == "list":
        sessions = mem.list_sessions()
        print(f"\nTotal Sessions in Memory: {len(sessions)}")
        for s in sessions:
            print(f"- Session ID: {s['session_id']} | Project: {s['project_name']} | Profile: {s['model_profile']}")
    elif args.action == "clear":
        target = args.session_id or "default"
        mem.clear_session(target)
        print(f"\nSession '{target}' cleared from SQLite memory.")

def main(argv: Optional[List[str]] = None) -> None:
    parser = argparse.ArgumentParser(
        prog="fie",
        description="Frontier Intelligence Engine (FIE) CLI - Universal AI Framework"
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose debug logging.")
    subparsers = parser.add_subparsers(dest="subcommand", required=True)

    # Subcommand: run
    run_parser = subparsers.add_parser("run", help="Orchestrate a task using FIE multi-agent pipeline.")
    run_parser.add_argument("--task", required=True, type=str, help="The task or goal to execute.")
    run_parser.add_argument("--model-profile", default="medium", choices=["small", "medium", "large"], help="Target model tier.")
    run_parser.add_argument("--session-id", default=None, type=str, help="Optional session identifier for memory continuity.")

    # Subcommand: inspect-prompt
    inspect_parser = subparsers.add_parser("inspect-prompt", help="Display compiled Master System Instruction.")
    inspect_parser.add_argument("--task-type", default="coding", choices=["coding", "debugging", "research", "architecture", "analysis", "design", "writing", "general"], help="Task classification.")
    inspect_parser.add_argument("--model-profile", default="medium", choices=["small", "medium", "large"], help="Target model profile.")
    inspect_parser.add_argument("--agent", default=None, type=str, help="Specific agent role to load.")

    # Subcommand: benchmark
    bench_parser = subparsers.add_parser("benchmark", help="Execute internal benchmark evaluation.")
    bench_parser.add_argument("--category", default="all", choices=["all", "coding", "memory"], help="Benchmark suite to run.")

    # Subcommand: memory
    mem_parser = subparsers.add_parser("memory", help="Manage external SQLite memory.")
    mem_parser.add_argument("--action", required=True, choices=["list", "clear"], help="Memory action.")
    mem_parser.add_argument("--session-id", default=None, type=str, help="Session identifier for action.")

    args = parser.parse_args(argv)
    setup_logging(args.verbose)

    if args.subcommand == "run":
        handle_run(args)
    elif args.subcommand == "inspect-prompt":
        handle_inspect_prompt(args)
    elif args.subcommand == "benchmark":
        handle_benchmark(args)
    elif args.subcommand == "memory":
        handle_memory(args)

if __name__ == "__main__":
    main()
