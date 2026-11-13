#!/usr/bin/env python3
"""Validate the capability-first compatibility contract without dependencies."""

from __future__ import annotations

import json
import argparse
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / ".tikaz" / "compatibility.json"
COLLECTION = ROOT / "distribution" / "manifest.json"
REQUIRED_MODELS = {"gpt-6-astra", "gpt-6.1-sol", "gpt-6-luna", "gpt-6-sol"}
REQUIRED_CAPABILITIES = {"responses_api", "agents_sdk", "mcp", "structured_output", "requested_actual_separation"}
EXPECTED_SUITES = {"context-economy", "frontend-design", "video-intelligence", "engineering", "knowledge-research", "presentation", "visual-content"}


def _load_json(path: Path, errors: list[str]) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"cannot read {path}: {exc}")
        return {}
    if not isinstance(value, dict):
        errors.append(f"{path}: expected a JSON object")
        return {}
    return value


def validate_source(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    manifest_path = root / ".tikaz" / "compatibility.json"
    if not manifest_path.is_file():
        return [f"missing {manifest_path.relative_to(root)}"]
    value = _load_json(manifest_path, errors)
    for field in ("schema_version", "collection", "collection_version", "generated_from", "generated_for_suite", "supported_hosts", "integration_targets", "model_profiles", "capabilities", "validation_commands", "checked_on", "sources"):
        if field not in value:
            errors.append(f"missing top-level field: {field}")
    if value.get("schema_version") != "1.0":
        errors.append("schema_version must be 1.0")
    errors.extend(f"missing model profile: {model}" for model in sorted(REQUIRED_MODELS - set(value.get("model_profiles", {}))))
    errors.extend(f"missing capability: {capability}" for capability in sorted(REQUIRED_CAPABILITIES - set(value.get("capabilities", {}))))
    for model, profile in value.get("model_profiles", {}).items():
        if profile.get("actual_model") != "UNVERIFIED":
            errors.append(f"{model}: actual_model must remain UNVERIFIED in a portable manifest")
        if not profile.get("capabilities"):
            errors.append(f"{model}: capabilities must be non-empty")
        if not profile.get("role_recommendation"):
            errors.append(f"{model}: role_recommendation must be non-empty")
        if not profile.get("source_urls"):
            errors.append(f"{model}: source_urls must contain checked official evidence")
    if value.get("generated_from") != "distribution/manifest.json" and not str(value.get("generated_from", "")).startswith("TIKAZ-AI-Skills/suites/"):
        errors.append("generated_from must reference the canonical manifest or a suite path")
    if any("Codex Skill" not in str(host) for host in value.get("supported_hosts", [])):
        errors.append("supported_hosts must describe Skill hosts only; API/SDK/MCP belong under integration_targets")
    for target in ("responses_api", "agents_sdk", "mcp"):
        entry = value.get("integration_targets", {}).get(target, {})
        if not str(entry.get("support", "")).startswith("integration guidance only;"):
            errors.append(f"{target} must be marked as an integration target, not native Skill runtime support")
        if not str(entry.get("source", "")).startswith("https://"):
            errors.append(f"{target} must cite an official HTTPS source")
    if not value.get("checked_on") or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(value.get("checked_on"))):
        errors.append("checked_on must be an ISO date")
    if not value.get("sources") or any(not str(url).startswith("https://") for url in value.get("sources", [])):
        errors.append("sources must contain official HTTPS evidence URLs")
    collection = _load_json(root / "distribution" / "manifest.json", errors)
    if value.get("collection_version") != collection.get("version"):
        errors.append("collection_version must match distribution/manifest.json version")
    if set(collection.get("suites", {})) != EXPECTED_SUITES:
        errors.append("compatibility manifest expects the seven published suites")
    return errors


# Backward-compatible test and embedding entry point for the source manifest.
validate = validate_source


def validate_distribution(root: Path) -> list[str]:
    errors: list[str] = []
    compatibility_path = root / ".tikaz" / "compatibility.json"
    value = _load_json(compatibility_path, errors)
    metadata_path = root / "DISTRIBUTION.yml"
    if not metadata_path.is_file():
        return errors + ["missing DISTRIBUTION.yml"]
    metadata = metadata_path.read_text(encoding="utf-8")
    def field(name: str) -> str | None:
        match = re.search(rf"(?m)^{re.escape(name)}:\s*(\S.*?)\s*$", metadata)
        return match.group(1) if match else None
    suite = field("suite")
    canonical = field("canonical")
    commit = field("canonical_commit")
    version = field("version")
    if not suite or suite not in EXPECTED_SUITES:
        errors.append("DISTRIBUTION.yml suite is missing or unsupported")
    if value.get("schema_version") != "1.0":
        errors.append("exported compatibility schema_version must be 1.0")
    if value.get("generated_for_suite") != suite:
        errors.append("compatibility generated_for_suite does not match DISTRIBUTION.yml suite")
    if value.get("generated_from") != f"TIKAZ-AI-Skills/suites/{suite}":
        errors.append("compatibility generated_from does not match DISTRIBUTION.yml suite")
    if value.get("collection") != "TIKAZ-AI-Skills":
        errors.append("compatibility collection name is unexpected")
    if value.get("checked_on") is None or not value.get("sources"):
        errors.append("compatibility manifest must include checked_on and official sources")
    if not isinstance(value.get("model_profiles"), dict) or REQUIRED_MODELS - set(value.get("model_profiles", {})):
        errors.append("compatibility manifest is missing required model profiles")
    if not isinstance(value.get("capabilities"), dict) or REQUIRED_CAPABILITIES - set(value.get("capabilities", {})):
        errors.append("compatibility manifest is missing required capability entries")
    for model, profile in value.get("model_profiles", {}).items():
        if profile.get("actual_model") != "UNVERIFIED":
            errors.append(f"{model}: actual_model must remain UNVERIFIED")
        if not profile.get("source_urls") or any(not str(url).startswith("https://") for url in profile.get("source_urls", [])):
            errors.append(f"{model}: source_urls must contain official HTTPS evidence")
    for target in ("responses_api", "agents_sdk", "mcp"):
        entry = value.get("integration_targets", {}).get(target, {})
        if not str(entry.get("support", "")).startswith("integration guidance only;"):
            errors.append(f"{target} must be described as an integration target")
        if not str(entry.get("source", "")).startswith("https://"):
            errors.append(f"{target} is missing its official source URL")
    if not canonical or canonical != "https://github.com/TIKAZI/TIKAZ-AI-Skills":
        errors.append("DISTRIBUTION.yml canonical URL is missing or unexpected")
    if not commit or not re.fullmatch(r"[0-9a-f]{40}", commit):
        errors.append("DISTRIBUTION.yml canonical_commit must be a 40-character Git SHA")
    if not version or version != value.get("collection_version"):
        errors.append("DISTRIBUTION.yml version does not match compatibility collection_version")
    version_file = root / "VERSION"
    if not version_file.is_file() or version_file.read_text(encoding="utf-8").strip() != version:
        errors.append("VERSION does not match DISTRIBUTION.yml version")
    pyproject = root / "pyproject.toml"
    if pyproject.is_file():
        content = pyproject.read_text(encoding="utf-8")
        section = re.search(r"(?ms)^\[project\]\s*(.*?)(?=^\[|\Z)", content)
        package_version = re.search(r'(?m)^version\s*=\s*["\']([^"\']+)["\']\s*$', section.group(1)) if section else None
        if not package_version or package_version.group(1) != version:
            errors.append("pyproject.toml project.version does not match VERSION/DISTRIBUTION.yml")
    return errors


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--distribution-root", type=Path)
    args = parser.parse_args()
    problems = validate_distribution(args.distribution_root.resolve()) if args.distribution_root else validate_source()
    if problems:
        for problem in problems:
            print(f"ERROR: {problem}")
        raise SystemExit(1)
    print("PASS: capability-first compatibility manifest is valid")

