"""
===============================================
  Fun Commands — Games & Utilities 🎮
===============================================
No AI needed — coin flips, dice rolls, picks,
and timers with dramatic flair.
"""

import random
import time
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeRemainingColumn
from rich.text import Text
from rich.live import Live
from rich.align import Align

console = Console()

# ── ASCII art for coin faces ────────────────────────────────────────
HEADS_ART = r"""
    ┌──────────┐
    │  ★ ★ ★   │
    │  HEADS   │
    │  ★ ★ ★   │
    └──────────┘
"""

TAILS_ART = r"""
    ┌──────────┐
    │  ○ ○ ○   │
    │  TAILS   │
    │  ○ ○ ○   │
    └──────────┘
"""

COIN_SPIN_FRAMES = [
    "    ┌──────────┐\n    │ ░░░░░░░░ │\n    └──────────┘",
    "    ┌────┐\n    │░░░░│\n    └────┘",
    "      ││\n      ││\n      ││",
    "    ┌────┐\n    │░░░░│\n    └────┘",
    "    ┌──────────┐\n    │ ░░░░░░░░ │\n    └──────────┘",
]


# ═══════════════════════════════════════════════════════════════════
#  FLIP — Coin flip with animation
# ═══════════════════════════════════════════════════════════════════

def cmd_flip(*_):
    """Flip a coin with ASCII art animation."""
    console.print("\n[bold yellow]🪙 Flipping the coin...[/bold yellow]\n")

    # Animate the coin spinning
    with Live(console=console, refresh_per_second=8, transient=True) as live:
        for _ in range(3):  # 3 full spin cycles
            for frame in COIN_SPIN_FRAMES:
                live.update(
                    Align.center(Text(frame, style="bold cyan"))
                )
                time.sleep(0.1)

    # The result
    result = random.choice(["HEADS", "TAILS"])
    art = HEADS_ART if result == "HEADS" else TAILS_ART
    color = "bold green" if result == "HEADS" else "bold blue"

    console.print(
        Panel(
            f"[{color}]{art}\n\n         🎉 {result}! 🎉[/{color}]",
            title="🪙 Coin Flip Result",
            border_style=color,
            padding=(1, 2),
        )
    )


# ═══════════════════════════════════════════════════════════════════
#  ROLL — Dice roll with dramatic reveal
# ═══════════════════════════════════════════════════════════════════

def cmd_roll(args):
    """Roll an N-sided die (default d6) with dramatic animation."""
    sides = 6  # default
    if args:
        try:
            sides = int(args[0])
            if sides < 2:
                console.print("[bold red]Bro, a die needs at least 2 sides 🤦[/bold red]")
                return
        except ValueError:
            console.print("[bold red]That's not a number fam. Usage: roll [sides][/bold red]")
            return

    console.print(f"\n[bold yellow]🎲 Rolling a d{sides}...[/bold yellow]\n")

    # Dramatic rolling animation
    with Live(console=console, refresh_per_second=10, transient=True) as live:
        for i in range(15):
            fake = random.randint(1, sides)
            size = "bold" if i > 10 else ""
            live.update(
                Align.center(
                    Text(f"🎲  {fake}  🎲", style=f"{size} cyan", justify="center")
                )
            )
            time.sleep(0.05 + i * 0.02)  # Slows down for drama

    result = random.randint(1, sides)

    # Special messages for certain rolls
    if result == sides:
        msg = "🏆 NATURAL MAX! You're built different! 💪"
    elif result == 1:
        msg = "💀 Critical fail... pack it up fam."
    else:
        msg = "🎯 A solid roll!"

    console.print(
        Panel(
            f"[bold bright_cyan]"
            f"\n   🎲  You rolled a  [bold bright_green]{result}[/bold bright_green]  out of {sides}!  🎲\n\n"
            f"   {msg}\n"
            f"[/bold bright_cyan]",
            title=f"🎲 d{sides} Result",
            border_style="bold bright_yellow",
            padding=(1, 2),
        )
    )


# ═══════════════════════════════════════════════════════════════════
#  PICK — Random selection from options
# ═══════════════════════════════════════════════════════════════════

def cmd_pick(args):
    """Randomly pick from a list of options."""
    if not args or len(args) < 2:
        console.print(
            "[bold red]Usage: pick <option1> <option2> ...[/bold red]\n"
            "[dim]Give me at least 2 options to pick from![/dim]"
        )
        return

    console.print(f"\n[bold yellow]🎯 Picking from: {', '.join(args)}...[/bold yellow]\n")

    # Dramatic selection animation
    with Live(console=console, refresh_per_second=8, transient=True) as live:
        for i in range(12):
            fake = random.choice(args)
            live.update(
                Align.center(
                    Text(f"👉  {fake}  👈", style="bold cyan")
                )
            )
            time.sleep(0.08 + i * 0.03)

    chosen = random.choice(args)

    # Fun reaction messages
    reactions = [
        "The universe has spoken! 🌌",
        "No take-backsies! 😤",
        "It is what it is. 🤷",
        "Destiny chose this one! ✨",
        "The algorithm never lies! 🤖",
        "Accept your fate! ⚡",
    ]

    console.print(
        Panel(
            f"[bold bright_green]\n   🎉  The winner is:  [bold bright_yellow]{chosen}[/bold bright_yellow]  🎉\n\n"
            f"   {random.choice(reactions)}\n[/bold bright_green]",
            title="🎯 The Chosen One",
            border_style="bold bright_magenta",
            padding=(1, 2),
        )
    )


# ═══════════════════════════════════════════════════════════════════
#  TIMER — Countdown with progress bar
# ═══════════════════════════════════════════════════════════════════

def cmd_timer(args):
    """Countdown timer with a progress bar and funny end message."""
    if not args:
        console.print("[bold red]Usage: timer <seconds>[/bold red] — How long should I count? ⏱️")
        return

    try:
        seconds = int(args[0])
        if seconds < 1:
            console.print("[bold red]Bro, time only moves forward 🕐[/bold red]")
            return
        if seconds > 3600:
            console.print("[bold red]Max 1 hour (3600s). I ain't got all day 😤[/bold red]")
            return
    except ValueError:
        console.print("[bold red]That's not a number fam. Usage: timer <seconds>[/bold red]")
        return

    console.print(f"\n[bold yellow]⏱️ Starting {seconds}s countdown...[/bold yellow]\n")

    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}[/bold blue]"),
        BarColumn(bar_width=40, complete_style="bright_green", finished_style="bold bright_green"),
        TextColumn("[bold]{task.percentage:>3.0f}%[/bold]"),
        TimeRemainingColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("⏳ Counting down...", total=seconds)
        for i in range(seconds):
            time.sleep(1)
            remaining = seconds - i - 1
            if remaining <= 3 and remaining > 0:
                progress.update(task, description=f"🔥 {remaining}...")
            progress.update(task, advance=1)

    # Funny end messages
    end_messages = [
        "⏰ TIME'S UP! Get off your phone! 📱",
        "🔔 DING DING DING! That's a wrap! 🎬",
        "💥 BOOM! Time just exploded! 💣",
        "🎉 You survived the countdown! Achievement unlocked! 🏆",
        "⚡ TIME'S UP! Reality hits different now. 😤",
        "🚨 ALERT: Your time has left the chat. 👋",
    ]

    console.print(
        Panel(
            f"[bold bright_green]\n   {random.choice(end_messages)}\n[/bold bright_green]",
            title="⏱️ Timer Complete!",
            border_style="bold bright_yellow",
            padding=(1, 2),
        )
    )
