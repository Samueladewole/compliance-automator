"""Local CLI entry point for the compliance automator.

Usage:
    python -m agent.cli "your regulator-style query here"

Runs the query through the local agent pipeline against the synthetic
data shipped in /data/synthetic, with retrieval over the regulatory
corpus in /data/regulations. Emits a structured evidence pack to stdout.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import click


@click.command()
@click.argument("query", type=str)
@click.option(
    "--region",
    default="eu-central-1",
    help="AWS region for Bedrock invocations.",
)
@click.option(
    "--model",
    default="anthropic.claude-sonnet-4-6-20251022",
    help="Pinned Bedrock model ID for the reasoning step.",
)
@click.option(
    "--data-dir",
    default="data",
    type=click.Path(exists=True, file_okay=False, path_type=Path),
    help="Path to the data directory (regulations + synthetic events).",
)
@click.option(
    "--out",
    default=None,
    type=click.Path(dir_okay=False, path_type=Path),
    help="Output path for the evidence pack JSON. Defaults to stdout.",
)
def main(query: str, region: str, model: str, data_dir: Path, out: Path | None) -> None:
    """Run a regulator-style query through the compliance automator."""
    click.echo(f"[compliance-automator] query: {query!r}", err=True)
    click.echo(f"[compliance-automator] region={region} model={model}", err=True)

    # Placeholder pipeline — the real implementation lives in agent.pipeline.
    # The scaffold here returns a valid-shape evidence pack so the
    # end-to-end CLI path is exercisable before the build phase populates
    # the real agent logic.
    evidence_pack = {
        "query": query,
        "status": "scaffold",
        "summary": (
            "This is the repository scaffold. The full agent is not yet "
            "implemented — see README.md status section. Run `git log` "
            "and follow creativeminds.dev/blog for the build progress."
        ),
        "model": model,
        "region": region,
        "regulatory_mapping": {
            "ndpa_2023": "pending",
            "cbn_csat": "pending",
            "nis2_article_21": "pending",
            "nist_sp_800_53": "pending",
        },
        "citations": [],
        "next_steps": [
            "Implement agent.pipeline.compliance_pipeline",
            "Wire Strands + AgentCore",
            "Connect to deployed Knowledge Base",
            "Run the eval harness in eval/run_eval.py",
        ],
    }

    output = json.dumps(evidence_pack, indent=2)
    if out:
        out.write_text(output)
        click.echo(f"[compliance-automator] evidence pack written to {out}", err=True)
    else:
        click.echo(output)


if __name__ == "__main__":
    sys.exit(main())
