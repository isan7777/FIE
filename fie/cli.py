"""
Command-Line Interface (CLI) for Frontier Intelligence Engine (FIE).
Provides direct terminal access for task execution, prompt inspection,
deliverable verification, module inventory, benchmark testing, and memory management.
"""

import argparse
import sys
import json
import logging
from pathlib import Path
from typing import List, Optional

from fie.config import FIEConfig
from fie.core.loader import ModularPromptLoader
from fie.core.orchestrator import MasterOrchestrator
from fie.evaluation.runner import BenchmarkRunner
from fie.memory.sqlite_memory import SQLiteMemory
from fie.verification.engine import VerificationEngine

def setup_logging(verbose: bool = False) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S"
    )

def handle_run(args: argparse.Namespace) -> None:
    print("\n[FIE ENGINE] Initializing Task Workflow...")
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
    print(
        f"Task Type: {result['task_type'].upper()} | "
        f"Domain: {result.get('engineering_domain') or 'general'} | "
        f"Complexity: {result['complexity']}/10"
    )
    print(f"Pipeline Executed: {' -> '.join([s.upper() for s in result['pipeline']])}")
    print("=" * 60)

    for step in result["steps"]:
        print(f"\n--- STEP {step['step']}: [{step['agent'].upper()}] (Attempts: {step.get('attempts', 1)}) ---")
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
        active_agent=args.agent,
        domain_hint=args.domain,
        include_template=args.template
    )
    print("=" * 60)
    print("FIE COMPILED MASTER SYSTEM INSTRUCTION")
    print(
        f"Task Type: {args.task_type} | Agent: {args.agent or 'default'} | "
        f"Domain: {args.domain or 'auto'} | Profile: {args.model_profile}"
    )
    print(f"Estimated Tokens: {loader.adaptive_engine.estimate_token_count(prompt)}")
    print("=" * 60)
    print(prompt)

def handle_verify(args: argparse.Namespace) -> None:
    verifier = VerificationEngine()
    content = ""
    source_label = "inline"

    if args.file:
        target_path = Path(args.file)
        if not target_path.exists():
            print(f"[ERROR] File not found: {target_path}", file=sys.stderr)
            sys.exit(1)
        content = target_path.read_text(encoding="utf-8", errors="replace")
        source_label = str(target_path)
    elif args.code:
        content = args.code
    else:
        print("[ERROR] Must supply either --file or --code for verification.", file=sys.stderr)
        sys.exit(1)

    res = verifier.verify_deliverable(content)
    if args.json:
        print(json.dumps(res, indent=2))
        return

    print("=" * 60)
    print("FIE SELF-VERIFICATION REPORT")
    print(f"Source           : {source_label}")
    print(f"Deliverable Type : {res.get('deliverable_type', 'unknown')}")
    print(f"Status           : {res['status']}")
    print(f"Quality Grade    : {res['grade']}")
    print("=" * 60)
    if res.get("issues"):
        print("\nIssues Detected:")
        for iss in res["issues"]:
            print(f"  [ISSUE] {iss}")
    if res.get("warnings"):
        print("\nWarnings Detected:")
        for warn in res["warnings"]:
            print(f"  [WARN]  {warn}")
    if not res.get("issues") and not res.get("warnings"):
        print("\n[PASS] No issues or policy warnings detected.")

def handle_list_modules(args: argparse.Namespace) -> None:
    loader = ModularPromptLoader()
    inventory = loader.list_available_modules()
    if args.json:
        print(json.dumps(inventory, indent=2))
        return

    print("=" * 60)
    print("FIE MODULAR KNOWLEDGE & AGENT INVENTORY")
    print("=" * 60)
    total = 0
    for category, items in inventory.items():
        total += len(items)
        print(f"\n[{category.upper()}] ({len(items)} modules):")
        for item in items:
            print(f"  - {item}")
    print("\n" + "=" * 60)
    print(f"Total Registered Modules: {total}")

def handle_benchmark(args: argparse.Namespace) -> None:
    runner = BenchmarkRunner()

    if args.category == "coding":
        res = runner.run_coding_suite()
    elif args.category == "reasoning":
        res = runner.run_reasoning_suite()
    elif args.category == "memory":
        res = runner.run_memory_adherence_suite()
    elif args.category == "tools":
        res = runner.run_tools_execution_suite()
    else:
        res = runner.run_full_benchmark()

    if args.json:
        print(json.dumps(res, indent=2))
        return

    print("\n[FIE BENCHMARK] Executing Internal Quality & Performance Suites...")
    if args.category in ("coding", "reasoning", "memory", "tools"):
        print(f"\n{res['category']} Suite Score: {res['correctness_score']}% ({res['passed_cases']}/{res['total_cases']} Passed)")
        for d in res["details"]:
            status_symbol = "[PASS]" if d["passed"] else "[FAIL]"
            label = f"{d['id']}: {d['name']} ({d['status']})" if "id" in d else d.get("test", "test")
            print(f"  {status_symbol} {label}")
    else:
        print("\n" + "=" * 60)
        print("FIE BENCHMARK COMPOSITE REPORT")
        print(f"Overall Score : {res['final_score']}%")
        print(f"Quality Grade : {res['grade']}")
        print("-" * 60)
        print(f"Correctness   : {res['metrics']['correctness']}%")
        print(f"Completeness  : {res['metrics']['completeness']}%")
        print(f"Adherence     : {res['metrics']['adherence']}%")
        print(f"Efficiency    : {res['metrics']['efficiency']}%")
        print("=" * 60)
        for suite in res["suites"]:
            print(f"\nSuite: {suite['category']} -> {suite['correctness_score']}% Passed ({suite['passed_cases']}/{suite['total_cases']})")
            for d in suite["details"]:
                name = d.get("name") or d.get("test", "test")
                symbol = "[PASS]" if d["passed"] else "[FAIL]"
                print(f"   {symbol} {name}")

def handle_memory(args: argparse.Namespace) -> None:
    mem = SQLiteMemory()
    target = args.session_id or "default"

    if args.action == "list":
        sessions = mem.list_sessions()
        print(f"\nTotal Sessions in Memory: {len(sessions)}")
        for s in sessions:
            print(f"- Session ID: {s['session_id']} | Project: {s['project_name']} | Profile: {s['model_profile']}")
    elif args.action == "facts":
        facts = mem.get_all_facts(target)
        print(f"\nProject Facts for Session '{target}' ({len(facts)}):")
        for f in facts:
            print(f"- [{f['category']}] {f['fact_key']}: {f['fact_value']}")
    elif args.action == "tasks":
        tasks = mem.get_tasks_for_session(target)
        print(f"\nTasks for Session '{target}' ({len(tasks)}):")
        for t in tasks:
            print(f"- {t['task_id']} | Agent: {t['assigned_agent']} | Status: {t['status']} | Verif: {t['verification_status']}")
    elif args.action == "stats":
        stats = mem.get_memory_stats()
        print("\nSQLite Memory Engine Statistics:")
        for table, cnt in stats.items():
            print(f"- {table}: {cnt} records")
    elif args.action == "set-fact":
        if not args.key or not args.value:
            print("[ERROR] --key and --value are required for set-fact.", file=sys.stderr)
            sys.exit(1)
        mem.create_or_get_session(target)
        mem.set_fact(target, args.category or "ARCHITECTURE", args.key, args.value)
        print(f"\nFact '{args.key}' recorded in session '{target}'.")
    elif args.action == "export":
        data = mem.export_session(target)
        print(json.dumps(data, indent=2, default=str))
    elif args.action == "clear":
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
    inspect_parser.add_argument("--task-type", default="coding", choices=["coding", "debugging", "research", "architecture", "analysis", "design", "testing", "writing", "security", "general"], help="Task classification.")
    inspect_parser.add_argument("--model-profile", default="medium", choices=["small", "medium", "large"], help="Target model profile.")
    inspect_parser.add_argument("--agent", default=None, type=str, help="Specific agent role to load.")
    inspect_parser.add_argument("--domain", default=None, type=str, help="Engineering playbook domain hint (e.g., backend, frontend, database, security, ai-llm-engineering).")
    inspect_parser.add_argument("--template", default=None, type=str, help="Optional deliverable template to embed (e.g., code-template, research-template, project-report).")

    # Subcommand: verify
    verify_parser = subparsers.add_parser("verify", help="Verify a file or code snippet against FIE quality and security rubrics.")
    verify_parser.add_argument("--file", default=None, type=str, help="Path to file to verify.")
    verify_parser.add_argument("--code", default=None, type=str, help="Inline code or markdown text to verify.")
    verify_parser.add_argument("--json", action="store_true", help="Output verification result as JSON.")

    # Subcommand: list-modules
    list_parser = subparsers.add_parser("list-modules", help="List all available FIE modular knowledge and agent files.")
    list_parser.add_argument("--json", action="store_true", help="Output inventory as JSON.")

    # Subcommand: benchmark
    bench_parser = subparsers.add_parser("benchmark", help="Execute internal benchmark evaluation.")
    bench_parser.add_argument("--category", default="all", choices=["all", "coding", "reasoning", "memory", "tools"], help="Benchmark suite to run.")
    bench_parser.add_argument("--json", action="store_true", help="Output benchmark results as JSON.")

    # Subcommand: memory
    mem_parser = subparsers.add_parser("memory", help="Manage external SQLite memory.")
    mem_parser.add_argument("--action", required=True, choices=["list", "facts", "tasks", "stats", "set-fact", "export", "clear"], help="Memory action.")
    mem_parser.add_argument("--session-id", default=None, type=str, help="Session identifier for action.")
    mem_parser.add_argument("--category", default="ARCHITECTURE", type=str, help="Fact category for set-fact.")
    mem_parser.add_argument("--key", default=None, type=str, help="Fact key for set-fact.")
    mem_parser.add_argument("--value", default=None, type=str, help="Fact value for set-fact.")

    args = parser.parse_args(argv)
    setup_logging(args.verbose)

    if args.subcommand == "run":
        handle_run(args)
    elif args.subcommand == "inspect-prompt":
        handle_inspect_prompt(args)
    elif args.subcommand == "verify":
        handle_verify(args)
    elif args.subcommand == "list-modules":
        handle_list_modules(args)
    elif args.subcommand == "benchmark":
        handle_benchmark(args)
    elif args.subcommand == "memory":
        handle_memory(args)

if __name__ == "__main__":
    main()
