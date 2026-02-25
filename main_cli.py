#!/usr/bin/env python3
"""
CLI for Web Risk Intelligence System
Uses refactored engine.analyze_domain()
"""
import json
import typer
from app.core.engine import analyze_domain

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
    try:
        result = analyze_domain(domain)
        
        if json_output:
            print(json.dumps(result, indent=2))
        else:
            # Human-readable output
            print(f"\n🔍 Domain Risk Assessment: {result['domain']}")
            print(f"{'='*50}")
            print(f"Risk Score: {result['score']}/100")
            print(f"Risk Level: {result['risk_level']}")
            print(f"\n📊 Details:")
            print(f"  Domain Age: {result['domain_age_days']} days")
            print(f"  SSL Valid: {'✓' if result['ssl_valid'] else '✗'}")
            print(f"  SSL Expires: {result['ssl_expires_in_days']} days")
            print(f"\n⚠️  Risk Indicators:")
            for reason in result['reasons']:
                print(f"  • {reason}")
            print()
            
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
