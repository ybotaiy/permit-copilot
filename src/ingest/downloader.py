"""Download KB documents listed in the manifest."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

import requests
import yaml
from requests.adapters import HTTPAdapter
from rich.console import Console
from urllib3.util.retry import Retry

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MANIFEST = ROOT / "kb" / "manifest.yaml"
DEFAULT_OUTPUT_DIR = ROOT / "kb" / "raw"

console = Console()


def _session() -> requests.Session:
    session = requests.Session()
    retries = Retry(total=3, backoff_factor=1, status_forcelist=[502, 503, 504])
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    session.headers["User-Agent"] = "permit-copilot/0.1"
    return session


def download_manifest(
    manifest_path: Path = DEFAULT_MANIFEST,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    *,
    force: bool = False,
) -> None:
    """Download every document in *manifest_path* into *output_dir*."""
    manifest = yaml.safe_load(manifest_path.read_text())
    docs = manifest["documents"]
    output_dir.mkdir(parents=True, exist_ok=True)

    session = _session()
    index: list[dict] = []

    for doc in docs:
        doc_id = doc["id"]
        fmt = doc["format"]
        filename = f"{doc_id}.{fmt}"
        dest = output_dir / filename

        if dest.exists() and not force:
            console.print(f"[dim]skip[/dim]  {filename} (exists)")
            index.append(_meta(doc, dest))
            continue

        console.print(f"[bold cyan]fetch[/bold cyan] {filename}")
        try:
            resp = session.get(doc["url"], timeout=30)
            resp.raise_for_status()
        except requests.RequestException as exc:
            console.print(f"[red]error[/red] {filename}: {exc}")
            continue

        dest.write_bytes(resp.content)
        index.append(_meta(doc, dest))
        console.print(f"[green]saved[/green] {filename} ({len(resp.content)} bytes)")

    index_path = output_dir / "index.json"
    index_path.write_text(json.dumps(index, indent=2) + "\n")
    console.print(f"\n[bold]Wrote {len(index)} entries to {index_path}[/bold]")


def _meta(doc: dict, dest: Path) -> dict:
    return {
        "id": doc["id"],
        "title": doc["title"],
        "url": doc["url"],
        "format": doc["format"],
        "source": doc["source"],
        "local_path": str(dest),
        "downloaded_at": datetime.now(UTC).isoformat(),
    }
