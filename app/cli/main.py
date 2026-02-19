"""
CLI Interface - Primary user interface.
Uses Typer for clean command-line experience.
"""

import sys
import json
import logging
from pathlib import Path
from typing import Optional
import typer
from rich.console import Console
from rich.table import Table

from app.core.config_loader import ConfigLoader
from app.services.analyzer_service import AnalyzerService
from app.core.models import RiskResult

app = typer.Typer(help="Web Risk Intelligence System - Domain Threat Assessment")
console = Console()


def setup_logging(verbose: bool) -> None:
    """Configure logging based on verbosity."""
    level = logging.DEBUG if verbose else logging.WARNING
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


@app.command()
def analyze(
    domain: str = typer.Argument(..., help="Domain to analyze"),
    json_output: bool = typer.Option(False, "--json", help="Output results as JSON"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose logging"),
    config_path: Optional[Path] = typer.Option(
        None, "--config", "-c", help="Custom configuration file path"
    ),
) -> None:
    """
    Analyze a domain for risk indicators.

    Returns exit codes:
    - 0: Low or Medium risk
    - 1: High or Critical risk
    - 2: Error occurred
    """
    setup_logging(verbose)

    try:
        # Load configuration
        config = ConfigLoader.load(config_path)

        # Initialize service
        service = AnalyzerService(config)

        # Analyze domain
        result = service.analyze_domain(domain)

        # Output results
        if json_output:
            _output_json(result)
        else:
            _output_human(result)

        # Exit with appropriate code
        exit_code = _determine_exit_code(result)
        sys.exit(exit_code)

    except ValueError as e:
        if not json_output:
            console.print(f"[red]Error:[/red] {e}")
        else:
            print(json.dumps({"error": str(e)}))
        sys.exit(2)

    except Exception as e:
        if verbose:
            console.print_exception()
        else:
            if not json_output:
                console.print(f"[red]Unexpected error:[/red] {e}")
            else:
                print(json.dumps({"error": "Internal error occurred"}))
        sys.exit(2)


def _output_human(result: RiskResult) -> None:
    """Output human-readable results."""
    # Determine color based on classification
    color_map = {
        "Low": "green",
        "Medium": "yellow",
        "High": "red",
        "Critical": "bold red",
    }
    color = color_map.get(result.classification, "white")

    # Header
    console.print(f"\n[bold]Domain Risk Assessment: {result.domain}[/bold]\n")

    # Score and classification
    console.print(
        f"Risk Score: [{color}]{result.score}/100[/{color}] "
        f"([{color}]{result.classification.upper()}[/{color}])\n"
    )

    # Triggered rules
    if result.triggered_rules:
        triggered = [rule for rule in result.triggered_rules if rule.triggered]
        if triggered:
            console.print("[bold]Risk Indicators:[/bold]")
            for rule in triggered:
                console.print(f"  • {rule.justification} [dim](+{rule.weight})[/dim]")
            console.print()

    # Intelligence summary
    intel = result.intelligence
    table = Table(title="Intelligence Summary", show_header=True)
    table.add_column("Signal", style="cyan")
    table.add_column("Value", style="white")

    if intel.age_days is not None:
        table.add_row("Domain Age", f"{intel.age_days} days")
    table.add_row("MX Records", "✓" if intel.has_mx else "✗")
    table.add_row("SPF Records", "✓" if intel.has_spf else "✗")
    table.add_row("Valid SSL", "✓" if intel.ssl_valid else "✗")
    if intel.is_self_signed:
        table.add_row("Self-Signed SSL", "Yes")
    if intel.risky_tld:
        table.add_row("Risky TLD", "Yes")
    if intel.is_punycode:
        table.add_row("Punycode", "Yes")

    console.print(table)
    console.print()

    # Errors
    if intel.errors:
        console.print("[yellow]Collection Warnings:[/yellow]")
        for error in intel.errors:
            console.print(f"  • {error}")
        console.print()


def _output_json(result: RiskResult) -> None:
    """Output JSON results."""
    output = {
        "domain": result.domain,
        "score": result.score,
        "classification": result.classification,
        "triggered_rules": [
            {
                "rule": rule.rule_name,
                "triggered": rule.triggered,
                "weight": rule.weight,
                "justification": rule.justification,
            }
            for rule in result.triggered_rules
            if rule.triggered
        ],
        "intelligence": {
            "age_days": result.intelligence.age_days,
            "has_mx": result.intelligence.has_mx,
            "has_spf": result.intelligence.has_spf,
            "ssl_valid": result.intelligence.ssl_valid,
            "is_self_signed": result.intelligence.is_self_signed,
            "triggered_keywords": result.intelligence.triggered_keywords,
            "risky_tld": result.intelligence.risky_tld,
            "is_punycode": result.intelligence.is_punycode,
            "errors": result.intelligence.errors,
        },
    }
    print(json.dumps(output, indent=2))


def _determine_exit_code(result: RiskResult) -> int:
    """Determine exit code based on risk classification."""
    if result.classification in ["High", "Critical"]:
        return 1
    return 0


if __name__ == "__main__":
    app()
