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
    title = "     ⚡ MY TOOL "
    subtitle = "mini ContactBook CLI Interface"

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
            "CONTACT OPTIONS",
            [
                " [blue][0][/blue]🔴 [bold blue]Exit Expense[/bold blue]",
                " [blue][1][/blue]➕ [bold blue]Add Contact[/bold blue]",
                " [blue][2][/blue]➖ [bold blue]Delete Contact[/bold blue]",
                " [blue][3][/blue]📖 [bold blue]Edit/Update Contact[/bold blue]",
                " [blue][4][/blue]📋 [bold blue]List All Contacts[/bold blue]",
            ],
        ),
        (
            "FUNCTIONALITY OPTIONS",
            [
                " [magenta][5][/magenta] ⭐ [bold magenta]Togle as Favorite(ID)[/bold magenta]",
                " [magenta][6][/magenta] 🔴 [bold magenta]Togle as UnFavorite(ID)[/bold magenta]",
            ],
        ),
        (
            "FILTER OPTIONS",
            [
                " [yellow][7][/yellow]🚀 [bold yellow]Load Note(ID)[/bold yellow]",
                " [yellow][8][/yellow]⭐ [bold yellow]Favorite Notes[/bold yellow]",
            ],
        ),
        (
            "SEARCH OPTIONS",
            [
                " [green][9] [/green]🔍 [bold green]Search By Name[/bold green]",
                " [green][10] [/green]🔍 [bold green]Search By Phone[/bold green]",
                " [green][11] [/green]🔍 [bold green]Search By Email[/bold green]",
            ],
        ),
        (
            "STATS",
            [
                " [blue][12] [/blue]🔍 [bold blue]Get Stats[/bold blue]",
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
