"""Rich terminal rendering for GitQuest capability diagnostics."""

from rich.panel import Panel
from rich.table import Table

from gitquest.application.doctor import DoctorReport
from gitquest.interfaces.terminal_ui import console


def render_doctor_report(report: DoctorReport) -> None:
    """Render capability checks and profile readiness."""
    console.print()
    console.print(
        Panel(
            "Checks the free local tools GitQuest can use. Missing Standard or Full tools "
            "do not prevent the current Lite campaign from running.",
            title="GitQuest Doctor",
            border_style="cyan",
        )
    )

    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Component", style="bold")
    table.add_column("Profiles")
    table.add_column("Status")
    table.add_column("Details")

    for check in report.checks:
        status = (
            "[bold green]READY[/bold green]"
            if check.available
            else "[bold yellow]MISSING[/bold yellow]"
        )
        table.add_row(check.label, ", ".join(check.profiles), status, check.detail)

    console.print(table)
    console.print()

    profile_table = Table(title="Runtime Profiles", show_header=True, header_style="bold cyan")
    profile_table.add_column("Profile", style="bold")
    profile_table.add_column("Status")
    profile_table.add_column("Purpose")

    purposes = {
        "Lite": "Git forensics, repository missions, and local evidence",
        "Standard": "Lite plus secret, image, and dependency scanning",
        "Full": "Standard plus IaC, signing, and local Kubernetes",
    }

    for profile in ("Lite", "Standard", "Full"):
        ready = report.profile_ready(profile)
        status = "[bold green]READY[/bold green]" if ready else "[yellow]NOT READY[/yellow]"
        profile_table.add_row(profile, status, purposes[profile])

    console.print(profile_table)

    if report.lite_ready:
        console.print("\n[bold green]GitQuest Lite is ready to play.[/bold green]")
    else:
        console.print(
            "\n[bold red]GitQuest Lite needs attention before missions can run.[/bold red]"
        )
