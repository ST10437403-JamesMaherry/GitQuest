from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text


# This Console object is the main Rich object we use to print styled output.
# Instead of using Python's normal print(), we can use console.print().
console = Console()


def print_title(title, subtitle=None):
    """
    Prints a styled title panel.

    Args:
        title: The main title text.
        subtitle: Optional subtitle text displayed below the title.
    """
    title_text = Text(title, style="bold cyan")

    # If a subtitle was provided, add it below the main title.
    if subtitle:
        title_text.append(f"\n{subtitle}", style="white")

    console.print(
        Panel(
            title_text,
            border_style="cyan",
            padding=(1, 2)
        )
    )


def print_section(title):
    """
    Prints a simple styled section heading.

    Args:
        title: The heading text.
    """
    console.print(f"\n[bold cyan]{title}[/bold cyan]")
    console.print(f"[cyan]{'=' * len(title)}[/cyan]")


def print_success(message):
    """
    Prints a green success message.

    Args:
        message: The message to display.
    """
    console.print(f"[bold green]{message}[/bold green]")


def print_error(message):
    """
    Prints a red error message.

    Args:
        message: The message to display.
    """
    console.print(f"[bold red]{message}[/bold red]")


def print_warning(message):
    """
    Prints a yellow warning message.

    Args:
        message: The message to display.
    """
    console.print(f"[bold yellow]{message}[/bold yellow]")


def print_info(message):
    """
    Prints a blue information message.

    Args:
        message: The message to display.
    """
    console.print(f"[blue]{message}[/blue]")


def print_story(message):
    """
    Prints mission story text inside a styled panel.

    Args:
        message: The story text to display.
    """
    console.print(
        Panel(
            message,
            title="Story",
            border_style="magenta",
            padding=(1, 2)
        )
    )


def create_menu_table(title):
    """
    Creates a reusable Rich table for menus.

    Args:
        title: The title shown above the table.

    Returns:
        A configured Rich Table object.
    """
    table = Table(title=title, show_header=True, header_style="bold cyan")
    table.add_column("Option", style="bold")
    table.add_column("Action")

    return table