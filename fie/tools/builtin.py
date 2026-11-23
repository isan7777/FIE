"""
Built-in Tools and Tool Registry for Frontier Intelligence Engine (FIE).
Provides sandboxed Python code execution, safe file management, and HTTP requests
with permission checks and capability detection.
"""

from pathlib import Path
from typing import Any, Callable, Dict, List, Optional
import subprocess
import json
import urllib.request
import urllib.error
import logging
from fie.config import FIEConfig

logger = logging.getLogger("fie.tools")

class ToolRegistry:
    """Central registry and execution manager for FIE tools."""

    def __init__(self, config: Optional[FIEConfig] = None) -> None:
        self.config = config or FIEConfig()
        self._tools: Dict[str, Dict[str, Any]] = {}
        self._register_default_tools()

    def register_tool(
        self,
        name: str,
        description: str,
        parameters: Dict[str, Any],
        handler: Callable[..., Any]
    ) -> None:
        self._tools[name] = {
            "name": name,
            "description": description,
            "parameters": parameters,
            "handler": handler
        }

    def list_declarations(self) -> List[Dict[str, Any]]:
        """Returns OpenAPI/Gemini compatible tool declarations."""
        declarations = []
        for name, meta in self._tools.items():
            declarations.append({
                "name": name,
                "description": meta["description"],
                "parameters": meta["parameters"]
            })
        return declarations

    def execute(self, name: str, **kwargs: Any) -> Dict[str, Any]:
        """Executes a registered tool with error encapsulation."""
        if name not in self._tools:
            return {"status": "error", "message": f"Tool '{name}' is not registered."}

        handler = self._tools[name]["handler"]
        try:
            result = handler(**kwargs)
            return {"status": "success", "result": result}
        except Exception as e:
            logger.error(f"Error executing tool '{name}': {e}", exc_info=True)
            return {"status": "error", "message": str(e)}

    # ---------------- Default Tool Implementations ---------------- #

    def _register_default_tools(self) -> None:
        # 1. Execute Python Code
        self.register_tool(
            name="execute_python_code",
            description="Executes a Python script in a secure subprocess with timeout.",
            parameters={
                "type": "object",
                "properties": {
                    "code": {"type": "string", "description": "Complete Python code to execute."},
                    "timeout_seconds": {"type": "integer", "description": "Execution timeout in seconds.", "default": 10}
                },
                "required": ["code"]
            },
            handler=self._tool_execute_code
        )

        # 2. Read File
        self.register_tool(
            name="read_file",
            description="Reads contents of a local file safely.",
            parameters={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Relative or workspace path to the file."}
                },
                "required": ["path"]
            },
            handler=self._tool_read_file
        )

        # 3. Write File
        self.register_tool(
            name="write_file",
            description="Writes content to a local workspace file safely.",
            parameters={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Relative or workspace path to file."},
                    "content": {"type": "string", "description": "File text content."},
                    "overwrite": {"type": "boolean", "description": "Whether to overwrite existing file.", "default": False}
                },
                "required": ["path", "content"]
            },
            handler=self._tool_write_file
        )

        # 4. List Directory
        self.register_tool(
            name="list_directory",
            description="Lists files and subdirectories within a safe workspace path.",
            parameters={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Target folder path.", "default": "."}
                }
            },
            handler=self._tool_list_directory
        )

        # 5. HTTP Request
        self.register_tool(
            name="http_request",
            description="Performs an external HTTP GET/POST request with timeout safety.",
            parameters={
                "type": "object",
                "properties": {
                    "url": {"type": "string", "description": "Target HTTP/HTTPS URL."},
                    "method": {"type": "string", "enum": ["GET", "POST"], "default": "GET"},
                    "timeout": {"type": "integer", "default": 10}
                },
                "required": ["url"]
            },
            handler=self._tool_http_request
        )

    def _tool_execute_code(self, code: str, timeout_seconds: int = 10) -> Dict[str, Any]:
        perms = self.config.get_tool_permission("code_execution")
        if perms and not perms.get("enabled", True):
            raise PermissionError("Code execution is disabled by tool-permissions.yaml.")

        timeout = min(timeout_seconds, perms.get("timeout_seconds", 15))
        try:
            res = subprocess.run(
                ["python", "-c", code],
                capture_output=True,
                text=True,
                timeout=timeout
            )
            return {
                "exit_code": res.returncode,
                "stdout": res.stdout[:16384],
                "stderr": res.stderr[:16384]
            }
        except subprocess.TimeoutExpired:
            return {
                "exit_code": -1,
                "stdout": "",
                "stderr": f"Execution timed out after {timeout} seconds."
            }
        except Exception as e:
            return {"exit_code": -1, "stdout": "", "stderr": str(e)}

    def _is_safe_path(self, target_path: Path) -> bool:
        """Protects against path traversal attacks."""
        resolved = target_path.resolve()
        base = self.config.base_dir.resolve()
        try:
            resolved.relative_to(base)
            return True
        except ValueError:
            return False

    def _tool_read_file(self, path: str) -> str:
        target = (self.config.base_dir / path).resolve()
        if not self._is_safe_path(target):
            raise PermissionError(f"Access denied: path '{path}' escapes workspace boundary.")
        if not target.exists() or not target.is_file():
            raise FileNotFoundError(f"File '{path}' does not exist.")
        with open(target, "r", encoding="utf-8", errors="replace") as f:
            return f.read()

    def _tool_write_file(self, path: str, content: str, overwrite: bool = False) -> str:
        target = (self.config.base_dir / path).resolve()
        if not self._is_safe_path(target):
            raise PermissionError(f"Access denied: path '{path}' escapes workspace boundary.")
        if target.exists() and not overwrite:
            raise FileExistsError(f"File '{path}' already exists and overwrite=False.")
        target.parent.mkdir(parents=True, exist_ok=True)
        with open(target, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Successfully wrote {len(content)} characters to '{path}'."

    def _tool_list_directory(self, path: str = ".") -> List[str]:
        target = (self.config.base_dir / path).resolve()
        if not self._is_safe_path(target):
            raise PermissionError(f"Access denied: path '{path}' escapes workspace boundary.")
        if not target.exists() or not target.is_dir():
            raise NotADirectoryError(f"Directory '{path}' not found.")
        entries = []
        for item in target.iterdir():
            prefix = "[DIR] " if item.is_dir() else "[FILE] "
            entries.append(f"{prefix}{item.name}")
        return sorted(entries)

    def _tool_http_request(self, url: str, method: str = "GET", timeout: int = 10) -> Dict[str, Any]:
        perms = self.config.get_tool_permission("http_client")
        blocked_hosts = perms.get("blocked_hostnames", ["localhost", "127.0.0.1", "169.254.169.254"])
        for host in blocked_hosts:
            if host in url:
                raise PermissionError(f"HTTP request to internal/private host '{host}' is prohibited.")

        req = urllib.request.Request(url, method=method.upper())
        req.add_header("User-Agent", "Frontier-Intelligence-Engine/1.0")
        try:
            with urllib.request.urlopen(req, timeout=timeout) as response:
                status = response.status
                body = response.read(65536).decode("utf-8", errors="replace")
                return {"status_code": status, "body": body}
        except urllib.error.HTTPError as e:
            return {"status_code": e.code, "body": e.read(4096).decode("utf-8", errors="replace")}
        except Exception as e:
            return {"status_code": -1, "body": str(e)}
