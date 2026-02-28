#!/usr/bin/env python3
"""Run automated compliance checks against a project directory."""

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

VALID_GATE_TYPES = ["security", "hipaa", "pre-deployment", "custom"]

SECRET_PATTERNS = [
    (r"sk-[a-zA-Z0-9]{20,}", "Anthropic/OpenAI API key pattern"),
    (r"AKIA[0-9A-Z]{16}", "AWS access key"),
    (r"ghp_[a-zA-Z0-9]{36}", "GitHub personal access token"),
    (r"gho_[a-zA-Z0-9]{36}", "GitHub OAuth token"),
    (r"glpat-[a-zA-Z0-9\-]{20,}", "GitLab personal access token"),
    (r"xoxb-[0-9]{10,}", "Slack bot token"),
    (r"xoxp-[0-9]{10,}", "Slack user token"),
]

IGNORE_DIRS = {
    ".git", "node_modules", "__pycache__", ".venv", "venv",
    ".tmp", ".claude", "dist", "build", ".next",
}

IGNORE_EXTENSIONS = {
    ".pyc", ".whl", ".egg", ".lock", ".png", ".jpg", ".jpeg",
    ".gif", ".ico", ".svg", ".woff", ".woff2", ".ttf", ".eot",
    ".zip", ".tar", ".gz", ".db", ".sqlite", ".sqlite3",
}


def make_check(check_id, description, result, blocking, detail=None):
    entry = {
        "id": check_id,
        "description": description,
        "result": result,
        "blocking": blocking,
    }
    if detail:
        entry["detail"] = detail
    return entry


def scan_for_secrets(project_path):
    """Scan source files for secret patterns."""
    findings = []
    for root, dirs, files in os.walk(project_path):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        for fname in files:
            fpath = Path(root) / fname
            if fpath.suffix in IGNORE_EXTENSIONS:
                continue
            try:
                text = fpath.read_text(encoding="utf-8", errors="ignore")
            except (PermissionError, OSError):
                continue
            for pattern, label in SECRET_PATTERNS:
                matches = re.findall(pattern, text)
                if matches:
                    rel = fpath.relative_to(project_path)
                    findings.append(f"{rel}: {label} ({len(matches)} match(es))")
    return findings


def check_env_gitignore(project_path):
    """Check that .env exists and is in .gitignore."""
    checks = []
    env_path = project_path / ".env"
    gitignore_path = project_path / ".gitignore"

    if env_path.exists():
        checks.append(make_check(
            "env-file-exists", ".env file present", "pass", False,
        ))
    else:
        checks.append(make_check(
            "env-file-exists", ".env file present", "not-applicable", False,
            "No .env file found — may not be needed for this project",
        ))

    if gitignore_path.exists():
        content = gitignore_path.read_text(encoding="utf-8", errors="ignore")
        if ".env" in content:
            checks.append(make_check(
                "env-in-gitignore", ".env listed in .gitignore", "pass", True,
            ))
        else:
            checks.append(make_check(
                "env-in-gitignore", ".env listed in .gitignore", "fail", True,
                ".gitignore exists but does not contain .env",
            ))
    else:
        checks.append(make_check(
            "env-in-gitignore", ".env listed in .gitignore", "fail", True,
            "No .gitignore file found",
        ))

    return checks


def check_env_in_git_history(project_path):
    """Check if .env was ever committed to git."""
    try:
        result = subprocess.run(
            ["git", "log", "--all", "--diff-filter=A", "--name-only", "--pretty=format:", "--", ".env"],
            cwd=str(project_path),
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode != 0:
            return make_check(
                "env-not-in-git-history", ".env not in git history",
                "not-applicable", True, "Not a git repository or git not available",
            )
        if ".env" in result.stdout.strip():
            return make_check(
                "env-not-in-git-history", ".env not in git history",
                "fail", True, ".env was committed to git history — secrets may be exposed",
            )
        return make_check(
            "env-not-in-git-history", ".env not in git history", "pass", True,
        )
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return make_check(
            "env-not-in-git-history", ".env not in git history",
            "not-applicable", True, "git not available",
        )


def check_secrets_scan(project_path):
    """Scan for hardcoded secrets in source files."""
    findings = scan_for_secrets(project_path)
    if findings:
        detail = "; ".join(findings[:5])
        if len(findings) > 5:
            detail += f" ... and {len(findings) - 5} more"
        return make_check(
            "no-hardcoded-secrets", "No hardcoded secrets in source",
            "fail", True, detail,
        )
    return make_check(
        "no-hardcoded-secrets", "No hardcoded secrets in source", "pass", True,
    )


def check_lockfile(project_path):
    """Check that a dependency lockfile exists."""
    lockfiles = [
        "package-lock.json", "yarn.lock", "pnpm-lock.yaml",
        "requirements.txt", "poetry.lock", "Pipfile.lock",
        "Cargo.lock", "go.sum",
    ]
    found = [f for f in lockfiles if (project_path / f).exists()]
    if found:
        return make_check(
            "lockfile-exists", "Dependency lockfile present",
            "pass", False, f"Found: {', '.join(found)}",
        )
    return make_check(
        "lockfile-exists", "Dependency lockfile present",
        "fail", False, "No lockfile found — dependencies are not pinned",
    )


def check_readme(project_path):
    """Check that README exists."""
    for name in ["README.md", "README.rst", "README.txt", "README"]:
        if (project_path / name).exists():
            return make_check("readme-exists", "README present", "pass", False)
    return make_check(
        "readme-exists", "README present", "fail", False,
        "No README found",
    )


def check_test_directory(project_path):
    """Check that a test directory exists."""
    test_dirs = ["tests", "test", "__tests__", "spec"]
    found = [d for d in test_dirs if (project_path / d).is_dir()]
    if found:
        return make_check(
            "test-dir-exists", "Test directory present",
            "pass", False, f"Found: {', '.join(found)}",
        )
    return make_check(
        "test-dir-exists", "Test directory present",
        "fail", False, "No test directory found",
    )


def check_todo_scan(project_path):
    """Advisory scan for TODO comments in source files."""
    count = 0
    examples = []
    for root, dirs, files in os.walk(project_path):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        for fname in files:
            fpath = Path(root) / fname
            if fpath.suffix in IGNORE_EXTENSIONS:
                continue
            try:
                for i, line in enumerate(fpath.open(encoding="utf-8", errors="ignore"), 1):
                    if "TODO:" in line or "FIXME:" in line or "HACK:" in line:
                        count += 1
                        if len(examples) < 3:
                            rel = fpath.relative_to(project_path)
                            examples.append(f"{rel}:{i}")
            except (PermissionError, OSError):
                continue
    if count == 0:
        return make_check("todo-scan", "No TODO/FIXME/HACK in source", "pass", False)
    detail = f"{count} found"
    if examples:
        detail += f" (e.g., {', '.join(examples)})"
    return make_check("todo-scan", "No TODO/FIXME/HACK in source", "fail", False, detail)


def check_phi_directory(project_path):
    """HIPAA: check that a PHI boundary directory exists."""
    for candidate in ["src/phi", "phi", "app/phi"]:
        if (project_path / candidate).is_dir():
            return make_check(
                "phi-directory", "PHI boundary directory exists",
                "pass", True, f"Found: {candidate}/",
            )
    return make_check(
        "phi-directory", "PHI boundary directory exists",
        "fail", True, "No phi/ directory found — PHI boundary is not enforced",
    )


def check_audit_log_schema(project_path):
    """HIPAA: check for audit log table in schema files."""
    patterns = ["audit_log", "phi_access", "access_log"]
    for root, dirs, files in os.walk(project_path):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        for fname in files:
            fpath = Path(root) / fname
            if fpath.suffix not in (".sql", ".ts", ".py", ".prisma", ".graphql"):
                continue
            try:
                text = fpath.read_text(encoding="utf-8", errors="ignore").lower()
                for p in patterns:
                    if p in text:
                        rel = fpath.relative_to(project_path)
                        return make_check(
                            "audit-log-schema", "Audit log table in schema",
                            "pass", True, f"Found '{p}' in {rel}",
                        )
            except (PermissionError, OSError):
                continue
    return make_check(
        "audit-log-schema", "Audit log table in schema",
        "fail", True, "No audit_log or phi_access table found in schema files",
    )


def check_baa_docs(project_path):
    """HIPAA: check for BAA documentation."""
    for root, dirs, files in os.walk(project_path):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        for fname in files:
            fpath = Path(root) / fname
            try:
                text = fpath.read_text(encoding="utf-8", errors="ignore").lower()
                if "baa" in text or "business associate agreement" in text or "hipaa" in text:
                    rel = fpath.relative_to(project_path)
                    return make_check(
                        "baa-documentation", "BAA/HIPAA documentation present",
                        "pass", False, f"Found reference in {rel}",
                    )
            except (PermissionError, OSError, UnicodeDecodeError):
                continue
    return make_check(
        "baa-documentation", "BAA/HIPAA documentation present",
        "fail", True, "No BAA or HIPAA documentation found",
    )


def run_checks(gate_type, project_path):
    """Run checks for the given gate type and return results."""
    checks = []

    # Security checks (all gate types)
    checks.extend(check_env_gitignore(project_path))
    checks.append(check_env_in_git_history(project_path))
    checks.append(check_secrets_scan(project_path))
    checks.append(check_lockfile(project_path))

    # HIPAA checks
    if gate_type == "hipaa":
        checks.append(check_phi_directory(project_path))
        checks.append(check_audit_log_schema(project_path))
        checks.append(check_baa_docs(project_path))

    # Pre-deployment checks
    if gate_type == "pre-deployment":
        checks.append(check_readme(project_path))
        checks.append(check_test_directory(project_path))
        checks.append(check_todo_scan(project_path))

    return checks


def summarize(checks):
    """Produce a summary from check results."""
    total = len(checks)
    by_result = {"pass": 0, "fail": 0, "not-applicable": 0, "unable-to-verify": 0}
    hard_failures = []
    advisory_failures = []

    for c in checks:
        by_result[c["result"]] = by_result.get(c["result"], 0) + 1
        if c["result"] == "fail":
            if c["blocking"]:
                hard_failures.append(c["id"])
            else:
                advisory_failures.append(c["id"])

    return {
        "total": total,
        "pass": by_result["pass"],
        "fail": by_result["fail"],
        "not_applicable": by_result["not-applicable"],
        "unable_to_verify": by_result["unable-to-verify"],
        "hard_failures": hard_failures,
        "advisory_failures": advisory_failures,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--gate-type", required=True, choices=VALID_GATE_TYPES,
        help="Type of gate to run",
    )
    parser.add_argument(
        "--project-path", required=True,
        help="Root directory of the project to check",
    )
    parser.add_argument(
        "--output", help="Output JSON file path (default: stdout)",
    )
    args = parser.parse_args()

    project_path = Path(args.project_path).resolve()
    if not project_path.is_dir():
        print(json.dumps({
            "success": False,
            "error": f"Project path does not exist: {project_path}",
        }), file=sys.stderr)
        sys.exit(1)

    checks = run_checks(args.gate_type, project_path)
    summary = summarize(checks)

    result = {
        "gate_type": args.gate_type,
        "project_path": str(project_path),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "checks": checks,
        "summary": summary,
    }

    output = json.dumps(result, indent=2)
    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"Output saved to {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
