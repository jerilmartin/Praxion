"""
Scanning Module – thin wrappers around Checkov and Trivy CLI tools.   (OBJ-2)
"""
from __future__ import annotations
import asyncio
import json
import shutil
from pathlib import Path


async def run_checkov(target_dir: Path) -> dict:
    """
    Run `checkov -d <target_dir> -o json --quiet` and return parsed JSON.
    Requires checkov to be installed in the Python environment.
    """
    if not shutil.which("checkov"):
        raise EnvironmentError("checkov not found on PATH. Install with: pip install checkov")

    proc = await asyncio.create_subprocess_exec(
        "checkov", "-d", str(target_dir), "-o", "json", "--quiet",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    # Checkov exits non-zero when findings exist; that is expected
    return json.loads(stdout or "{}")


async def run_trivy(target_dir: Path) -> dict:
    """
    Run `trivy config <target_dir> --format json` and return parsed JSON.
    Requires trivy binary on PATH (install via package manager or Docker).
    """
    if not shutil.which("trivy"):
        raise EnvironmentError("trivy not found on PATH. See https://trivy.dev/docs/")

    proc = await asyncio.create_subprocess_exec(
        "trivy", "config", str(target_dir), "--format", "json",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, _ = await proc.communicate()
    return json.loads(stdout or "{}")
