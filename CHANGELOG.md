# Changelog - Frontier Intelligence Engine (FIE)

All notable changes to the Frontier Intelligence Engine project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-11-24

### Added
- **Natural Language & Anti-Poetic / Anti-Brochure Invariant**:
  - Added `knowledge/natural-language-style.md` prohibiting overly poetic brochure prose and translationese (e.g., *"dipilih secara saksama"*, *"episentrum ... dan ketenangan jiwa"*, *"situs warisan peradaban"*, *"terbentang ... seluas ribuan hektar"*) across UI copywriting, web/app content, seed data, and documentation.
  - Added `POETIC_CLICHE_PATTERNS` and `check_natural_language_style()` in `VerificationEngine` (`fie/verification/engine.py`) with automated test coverage (`test_poetic_cliche_detection`).
  - Enforced the Natural Language Invariant in `core/identity.md`, `rules/AGENTS.md`, `agents/writer.md`, `agents/designer.md`, `agents/coder.md`, and all Antigravity FIE subagents.
- **Root Antigravity Skill & Plugin Packaging**:
  - Added comprehensive root `SKILL.md` with full Progressive Disclosure module links, 9 specialist subagent mappings, and CLI verification commands.
  - Added root `plugin.json`, `rules/AGENTS.md`, and `pyproject.toml` with console entry point `fie = "fie.cli:main"`.
- **New Engineering Playbook & Workflow SOP**:
  - Added `engineering/ai-llm-engineering.md` covering modular system instructions, token budgeting, structured outputs, RAG memory hygiene, and AI safety guardrails.
  - Added `workflows/code-review-security-audit.md` defining a 4-stage static analysis, AST inspection, and OWASP security audit pipeline.
- **Enhanced Modular Prompt Loader (`fie/core/loader.py`)**:
  - Connected `FIEConfig` custom profiles to `AdaptiveModelEngine`.
  - Added loaders for `workflows/`, `knowledge/`, `tools/`, `templates/`, `core/decision-engine.md`, and `core/adaptive-intelligence.md`.
  - Added `list_available_modules()` and automatic domain/workflow selection in `compile_system_instruction()`.
- **Unified Deliverable Verifier (`fie/verification/engine.py`)**:
  - Added `extract_python_code_blocks()`, `sanitize_emojis()`, and `verify_deliverable()` to inspect pure Python code, mixed Markdown containing fenced Python blocks, or prose deliverables.
  - Expanded security checks (`shell=True`, hardcoded API keys/secrets) and AST quality checks (docstring-only pass functions, silent bare `except: pass`).
- **Autonomous Self-Correction Loop & Sub-Domain Detection (`fie/core/orchestrator.py`)**:
  - Added `detect_engineering_domain()` to automatically select matching engineering playbooks from user prompts.
  - Implemented `_run_step_with_self_correction()` up to `max_self_correction_attempts` with automatic emoji sanitization and verification feedback injection.
- **Expanded SQLite Memory Engine (`fie/memory/sqlite_memory.py`)**:
  - Added `fie_messages` table (`record_message`, `get_messages`) for conversation turn tracking.
  - Added `redact_sensitive_text()` guard to automatically redact raw API keys, tokens, and passwords before persistence.
  - Added `get_all_facts()`, `export_session()`, and `get_memory_stats()`.
- **Reasoning Benchmark Suite & Expanded CLI (`fie/evaluation/runner.py`, `fie/cli.py`)**:
  - Implemented `run_reasoning_suite()` covering `R-01` (Dependency Graph & Cycle Detection), `R-02` (Cryptographic Key Rollover State Machine), and `R-03` (Multi-Source SemVer Contradiction Resolver).
  - Added CLI subcommands `verify` and `list-modules`, plus JSON output flags and expanded `memory` actions (`facts`, `tasks`, `stats`, `set-fact`, `export`).

## [1.0.1] - 2026-11-24

### Added
- **Zero Emoji / Sticker Invariant**:
  - Enforced strict prohibition against emojis, emoticons, and decorative stickers across all code, docstrings, identifiers, logs, terminal outputs, and technical documentation.
  - Added AST and text regex verification in `VerificationEngine` to automatically detect and flag emoji pollution under `[STYLE_POLICY]`.
  - Added test case `test_emoji_sticker_detection` in `tests/test_verification.py`.
- **CLI & Benchmark Sanitization**:
  - Replaced symbol indicators with clean, standard tags (`[PASS]`, `[FAIL]`).
  - Added `formatting.allow_emojis: false` in `config/settings.yaml`.

## [1.0.0] - 2026-11-24

### Added
- **Core Intelligence Engine**:
  - `core/SKILL.md`: Master skill definition and system prompt loader for AI agents.
  - `core/identity.md`: Definitive mission, persona boundaries, and execution directives.
  - `core/reasoning.md`: Multi-step deterministic reasoning without redundant loops.
  - `core/adaptive-intelligence.md`: Adaptive token budget and instruction depth tailored for Small, Medium, and Large models.
  - `core/decision-engine.md`: Algorithmic task routing, risk categorization, and agent delegation rules.
- **Specialized Multi-Agent Mesh**:
  - 9 purpose-built agents with explicit contracts (`agents/orchestrator.md`, `architect.md`, `coder.md`, `debugger.md`, `researcher.md`, `analyst.md`, `designer.md`, `tester.md`, `writer.md`).
- **Intelligence & Self-Verification Subsystems**:
  - Comprehensive problem-solving and deep analysis methodologies (`intelligence/`).
  - Automated self-correction feedback loop and verification rubrics.
- **Engineering Domains**:
  - Technical playbooks for Software Architecture, Frontend, Backend, Database, API Integration, Performance, Security, and Game Development.
- **Research Protocols**:
  - Structured methodologies for web research, primary source verification, fact-checking, and academic literature analysis without hallucinations.
- **Tool Integration & Permissions**:
  - Standardized interfaces for Google Search Grounding, Code Execution, File Management, Function Calling, and REST API Tools.
- **External Memory Engine (SQLite)**:
  - Persistent SQLite storage with tables for sessions, messages, project facts, tasks, and search indexing (`fie/memory/sqlite_memory.py`).
- **Standardized Workflows & Templates**:
  - End-to-end execution workflows for software projects, bug triage, research pipelines, and delivery reports.
- **Evaluation & Benchmark Suite**:
  - Standardized benchmark test suites across coding, reasoning, and research with quantitative scoring metrics.
- **Python Runtime Implementation (`fie/`)**:
  - Modular instruction loader (`fie/core/loader.py`).
  - Task orchestrator and sequential agent executor (`fie/core/orchestrator.py`).
  - Model adaptive profiler (`fie/core/adaptive.py`).
  - Tool runner and permission manager (`fie/tools/builtin.py`).
  - Automated verification engine (`fie/verification/engine.py`).
  - Gemini API client wrapper with fallback and offline simulation mode (`fie/api/gemini_client.py`).
  - CLI runner for terminal interaction (`fie/cli.py`).
