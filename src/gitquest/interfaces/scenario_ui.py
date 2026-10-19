"""Terminal presentation for data-driven security scenarios."""

from rich.panel import Panel
from rich.table import Table

from gitquest.application.scenario_runner import ScenarioResult
from gitquest.domain.scenario import ScenarioManifest
from gitquest.interfaces.terminal_ui import console


def render_scenario_list(scenarios: tuple[ScenarioManifest, ...]) -> None:
    table = Table(title="GitQuest Security Scenarios", header_style="bold cyan")
    table.add_column("ID", style="bold")
    table.add_column("Scenario")
    table.add_column("Profile")
    table.add_column("Difficulty")
    for scenario in scenarios:
        table.add_row(scenario.id, scenario.title, scenario.profile, scenario.difficulty)
    console.print(table)


def render_scenario_started(manifest: ScenarioManifest, workspace: str) -> None:
    console.print(
        Panel(
            manifest.summary,
            title=f"Scenario Started: {manifest.title}",
            border_style="yellow",
        )
    )
    console.print(f"\n[bold cyan]Workspace:[/bold cyan] {workspace}")
    console.print(f"[bold cyan]Open it:[/bold cyan] cd {workspace}\n")
    console.print("[bold]Objectives[/bold]")
    for objective in manifest.objectives:
        console.print(f"  • [{objective.points} points] {objective.description}")
    console.print(f"\nWhen finished, run: [bold]gitquest scenario verify {manifest.id}[/bold]")


def render_scenario_result(result: ScenarioResult, report_paths: tuple[str, str]) -> None:
    table = Table(title=f"{result.title}: {result.score}/100", header_style="bold cyan")
    table.add_column("Objective")
    table.add_column("Status")
    table.add_column("Points", justify="right")
    for objective in result.objectives:
        status = "[green]PASS[/green]" if objective.passed else "[yellow]NEEDS WORK[/yellow]"
        table.add_row(
            objective.title,
            status,
            f"{objective.awarded_points}/{objective.points}",
        )
        if not objective.passed:
            for check in objective.checks:
                if not check.passed:
                    table.add_row(f"  ↳ {check.message}", "", "")
    console.print(table)

    if result.passed:
        console.print("\n[bold green]Incident contained. Scenario complete.[/bold green]")
    else:
        console.print("\n[bold yellow]The incident still has unresolved findings.[/bold yellow]")
    console.print(f"Markdown report: {report_paths[0]}")
    console.print(f"JSON evidence: {report_paths[1]}")
