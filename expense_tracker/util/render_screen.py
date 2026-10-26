from datetime import datetime
from time import sleep
from rich.console import Console,Group
from rich.panel import Panel
from rich.align import Align
from rich.text import Text
from rich.rule import Rule
from rich.padding import Padding
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.columns import Columns
console = Console()

# Get iso format date & time
def today():
    return datetime.now().isoformat(sep=" ", timespec="seconds")

def render_screen():
    title = "        ⚡ MY TOOL "
    subtitle = "mini Expense_Tracker CLI Interface"

    header_color = "bright_magenta"
    box_color = "gold"
    accent_color = "bright_green"
    
    console.clear()
    
    header = Text(title, style=f"bold {header_color}")
    sub = Text(subtitle, style=accent_color)

    console.print(
        Padding(
            Panel(
                Align.center(header + "\n" + sub),
                border_style=header_color
            ),
            (1, 2)
        )
    )

    sections = [
        (
            "EXPENSE OPTIONS",
            [
                " [blue][0][/blue]🔴 [bold blue]Exit Expense[/bold blue]",
                " [blue][1][/blue]➕ [bold blue]Add Expense[/bold blue]",
                " [blue][2][/blue]➖ [bold blue]Delete Expense[/bold blue]",
                " [blue][3][/blue]📖 [bold blue]Edit/Update Expense[/bold blue]",
                " [blue][4][/blue]📋 [bold blue]Get All Expenses[/bold blue]",
            ],
        ),
        (
            "FILTER OPTIONS",
            [
                " [yellow][5][/yellow]🚀 [bold yellow]Load Expense(ID)[/bold yellow]",
            ],
        ),
        (
            "SUMMARY OPTIONS",
            [
                " [green][6] [/green]🔍 [bold green]Summary All Categories[/bold green]",
                " [green][7] [/green]🔍 [bold green]Summary By A Category[/bold green]",
                " [green][8] [/green]🔍 [bold green]Summary By Date[/bold green]",
            ],
        ),
    ]

    panels = [
        Panel(
            Group(*options),
            border_style="cyan",
            title=f"[bold]{title}",
            title_align="left",
            expand=True,
            padding=(0, 1),
        )
        for title, options in sections
    ]
    console.print(Padding(Columns(panels, equal=True, expand=True), (1, 4)))

    console.print(f"[bold yellow]log :[/bold yellow] [bold cyan]{today()}")
    console.print()
    console.print(Rule(f"[bold {accent_color}] MAIN CONTRO PANEL ", style=accent_color))


#Loading animation
def loading_animation(duration=1):
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold green]Loading interface..."),
        transient=True,
    ) as progress:
        task = progress.add_task("load", total=None)
        sleep(duration)

if __name__ == "__main__":
    loading_animation()
    render_screen()
