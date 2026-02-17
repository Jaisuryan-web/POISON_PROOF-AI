#!/usr/bin/env python3
"""
Utilities to summarize the PoisonProof-AI project and running Flask app.
"""
from __future__ import annotations

import os
import json
import platform
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

try:
    import tomllib  # Python 3.11+
except Exception:  # pragma: no cover
    tomllib = None  # type: ignore


def _read_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return None


def _load_pyproject(pyproject_path: Path) -> Dict[str, Any] | None:
    if not pyproject_path.exists() or tomllib is None:
        return None
    try:
        with pyproject_path.open("rb") as f:
            return tomllib.load(f)
    except Exception:
        return None


def _list_routes(app) -> List[Dict[str, Any]]:
    routes: List[Dict[str, Any]] = []
    try:
        for rule in app.url_map.iter_rules():
            if rule.endpoint == 'static':
                continue
            routes.append({
                "rule": str(rule),
                "endpoint": rule.endpoint,
                "methods": sorted(m for m in rule.methods if m not in {"HEAD", "OPTIONS"}),
            })
    except Exception:
        pass
    routes.sort(key=lambda r: r["rule"])  # stable ordering
    return routes


def _count_files(path: Path) -> int:
    if not path.exists():
        return 0
    count = 0
    for _, _, files in os.walk(path):
        count += len(files)
    return count


def build_project_summary(app=None, project_root: str | Path | None = None) -> Dict[str, Any]:
    root = Path(project_root) if project_root else Path(os.getcwd())

    pyproject = _load_pyproject(root / "pyproject.toml")

    metadata: Dict[str, Any] = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "platform": {
            "python": platform.python_version(),
            "system": platform.system(),
            "release": platform.release(),
        },
    }

    if pyproject:
        project = pyproject.get("project", {})
        metadata["project"] = {
            "name": project.get("name"),
            "version": project.get("version"),
            "description": project.get("description"),
            "requires_python": project.get("requires-python"),
            "scripts": project.get("scripts", {}),
        }
        metadata["dependencies"] = project.get("dependencies", [])
        opt = pyproject.get("project", {}).get("optional-dependencies", {})
        if opt:
            metadata["optional_dependencies"] = opt

    # Fallback: requirements.txt
    req_path = root / "requirements.txt"
    if req_path.exists():
        try:
            reqs = [line.strip() for line in req_path.read_text(encoding="utf-8").splitlines() if line.strip() and not line.strip().startswith("#")]
            metadata.setdefault("dependencies", reqs)
        except Exception:
            pass

    # Files and assets
    metadata["files"] = {
        "templates": _count_files(root / "templates"),
        "static": _count_files(root / "static"),
        "trained_models": _count_files(root / "trained_models"),
    }

    # Notebooks or docs
    for fname in ["README.md", "FEATURES.md", "DATASET_SUMMARY.md", "TRAINING_QUICKSTART.md"]:
        p = root / fname
        if p.exists():
            text = _read_text(p)
            if text:
                metadata.setdefault("docs", {})[fname] = {
                    "size": len(text),
                    "preview": text[:300]
                }

    # Flask app related
    if app is not None:
        try:
            cfg = app.config
            metadata["flask"] = {
                "env": cfg.get("ENV"),
                "debug": bool(cfg.get("DEBUG")),
                "upload_folder": cfg.get("UPLOAD_FOLDER"),
                "max_content_length": cfg.get("MAX_CONTENT_LENGTH"),
                "allowed_extensions": sorted(cfg.get("ALLOWED_EXTENSIONS", [])),
                "routes": _list_routes(app),
            }
        except Exception:
            pass

    return metadata


def format_summary_html(summary: Dict[str, Any]) -> str:
    def h2(title: str) -> str:
        return f"<h2 style='margin-top:1rem'>{title}</h2>"

    def pre(obj: Any) -> str:
        return f"<pre style='background:#0b1021;color:#e6edf3;padding:12px;border-radius:8px;overflow:auto'>{json.dumps(obj, indent=2)}</pre>"

    parts: List[str] = []
    parts.append("<html><head><meta charset='utf-8'><title>Project Summary</title>")
    parts.append("<style>body{font-family:Inter,Segoe UI,Arial,sans-serif;background:#0d1117;color:#e6edf3;padding:24px} a{color:#58a6ff}</style>")
    parts.append("</head><body>")
    parts.append("<h1>PoisonProof-AI — Project Summary</h1>")
    parts.append("<p>This summary describes the project's configuration, dependencies, routes and key assets.</p>")

    # Project
    if "project" in summary:
        parts.append(h2("Project"))
        parts.append(pre(summary["project"]))

    # Platform
    parts.append(h2("Platform"))
    parts.append(pre(summary.get("platform", {})))

    # Dependencies
    if "dependencies" in summary:
        parts.append(h2("Dependencies"))
        parts.append(pre(summary["dependencies"]))

    # Optional deps
    if "optional_dependencies" in summary:
        parts.append(h2("Optional Dependencies"))
        parts.append(pre(summary["optional_dependencies"]))

    # Flask
    if "flask" in summary:
        parts.append(h2("Flask"))
        parts.append(pre({k: v for k, v in summary["flask"].items() if k != "routes"}))
        parts.append("<h3>Routes</h3>")
        parts.append(pre(summary["flask"].get("routes", [])))

    # Files
    parts.append(h2("Files"))
    parts.append(pre(summary.get("files", {})))

    # Docs
    if "docs" in summary:
        parts.append(h2("Docs (previews)"))
        parts.append(pre(summary["docs"]))

    parts.append("</body></html>")
    return "".join(parts)
