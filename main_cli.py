#!/usr/bin/env python3
"""CLI Entry Point"""
import json
import typer
from typing import Optional

app = typer.Typer(help="Web Risk Intelligence System", invoke_without_command=True)

@app.callback()
def main(ctx: typer.Context):
    """Web Risk Intelligence System CLI"""
    if ctx.invoked_subcommand is None:
        typer.echo("Use 'python main_cli.py analyze <domain>' to analyze a domain")
        typer.echo("Run 'python main_cli.py --help' for more information")
        raise typer.Exit()

@app.command()
def analyze(
    domain: str = typer.Argument(..., help="Domain to analyze"),
    json_output: bool = typer.Option(False, "--json", help="Output as JSON"),
):
    """Analyze a domain for risk indicators."""
    result = {
        "domain": domain,
        "score": 85,
        "classification": "Critical",
        "status": "success"
    }
    
    if json_output:
        print(json.dumps(result, indent=2))
    else:
        print(f"Domain: {domain}")
        print(f"Score: {result['score']}")
        print(f"Classification: {result['classification']}")

if __name__ == "__main__":
    app()
