"""
===============================================
  Team Commands — Member Management 👥
===============================================
Manage the Team Arch roster:
  - View members
  - Add new members
  - Random task assignment
"""

import json
import os
import random
import time
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.align import Align
from rich.text import Text

console = Console()

# Path to members.json (relative to project root)
MEMBERS_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "members.json")


def _load_members():
    """Load members from JSON file. Returns list of dicts or empty list."""
    try:
        with open(MEMBERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        console.print(
            Panel(
                "[bold red]members.json not found 🤷\n"
                "Run [green]add-member[/green] to create the roster![/bold red]",
                title="❌ Missing File",
                border_style="red",
            )
        )
        return []
    except json.JSONDecodeError:
        console.print(
            Panel(
                "[bold red]members.json is corrupted 💀\n"
                "The file isn't valid JSON. Fix it manually or delete it to start fresh.[/bold red]",
                title="❌ Parse Error",
                border_style="red",
            )
        )
        return []


def _save_members(members):
    """Save members list to JSON file."""
    try:
        with open(MEMBERS_FILE, "w", encoding="utf-8") as f:
            json.dump(members, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        console.print(f"[bold red]Couldn't save members.json: {e}[/bold red]")
        return False


# ═══════════════════════════════════════════════════════════════════
#  MEMBERS — Show the team roster
# ═══════════════════════════════════════════════════════════════════

def cmd_members(*_):
    """Display all team members in a styled table."""
    members = _load_members()
    if not members:
        return

    # Role color mapping for visual flair
    role_colors = {
        "Developer":    "bright_green",
        "Designer":     "bright_magenta",
        "Strategist":   "bright_yellow",
        "Backend Lead": "bright_cyan",
        "Full Stack":   "bright_blue",
    }

    table = Table(
        title="👥 Team Arch Roster 🔥",
        title_style="bold bright_cyan",
        border_style="bright_magenta",
        show_lines=True,
        padding=(0, 1),
    )
    table.add_column("#", style="dim", width=4, justify="center")
    table.add_column("Name", style="bold bright_white", min_width=12)
    table.add_column("Role", min_width=14)
    table.add_column("Title", style="bold bright_yellow", min_width=16)
    table.add_column("Catchphrase", style="italic dim", min_width=24)

    for i, member in enumerate(members, 1):
        name = member.get("name", "Unknown")
        role = member.get("role", "Member")
        title = member.get("title", "The Nobody")
        catchphrase = member.get("catchphrase", "...")

        role_color = role_colors.get(role, "white")
        table.add_row(
            str(i),
            name,
            f"[{role_color}]{role}[/{role_color}]",
            title,
            catchphrase,
        )

    console.print()
    console.print(table)
    console.print(f"\n[dim]Total members: {len(members)} 💪[/dim]\n")


# ═══════════════════════════════════════════════════════════════════
#  ADD-MEMBER — Interactively add a new member
# ═══════════════════════════════════════════════════════════════════

def cmd_add_member(*_):
    """Interactively add a new member to the team roster."""
    console.print(
        Panel(
            "[bold white]Let's add a new legend to Team Arch! 🎉\n"
            "Fill in the details below:[/bold white]",
            border_style="bright_green",
            padding=(1, 2),
        )
    )

    try:
        name = console.input("[bold green]  Name:[/bold green] ").strip()
        if not name:
            console.print("[bold red]Bro, they gotta have a name 🤦[/bold red]")
            return

        role = console.input("[bold green]  Role (e.g., Developer, Designer):[/bold green] ").strip()
        if not role:
            role = "Member"

        title = console.input("[bold green]  Fun Title (e.g., The Debugger):[/bold green] ").strip()
        if not title:
            title = "The Newbie"

        catchphrase = console.input("[bold green]  Catchphrase:[/bold green] ").strip()
        if not catchphrase:
            catchphrase = "I just got here. 👋"

    except (KeyboardInterrupt, EOFError):
        console.print("\n[yellow]Cancelled! No one was added.[/yellow]")
        return

    # Load existing members and append
    members = _load_members()
    if members is None:
        members = []

    new_member = {
        "name": name,
        "role": role,
        "title": title,
        "catchphrase": catchphrase,
    }
    members.append(new_member)

    if _save_members(members):
        console.print(
            Panel(
                f"[bold bright_green]✅ {name} has joined Team Arch!\n\n"
                f"  🏷️  Role: {role}\n"
                f"  🎭  Title: {title}\n"
                f"  💬  Catchphrase: {catchphrase}[/bold bright_green]",
                title="🎉 Welcome to the Team!",
                border_style="bold bright_green",
                padding=(1, 2),
            )
        )


# ═══════════════════════════════════════════════════════════════════
#  WHO'S TURN — Random member picker for tasks
# ═══════════════════════════════════════════════════════════════════

def cmd_whos_turn(*_):
    """Randomly pick a member for a task."""
    members = _load_members()
    if not members:
        return

    names = [m.get("name", "???") for m in members]

    console.print("\n[bold yellow]🎰 Spinning the wheel of fate...[/bold yellow]\n")

    # Dramatic selection animation
    with Live(console=console, refresh_per_second=8, transient=True) as live:
        for i in range(15):
            fake = random.choice(names)
            live.update(
                Align.center(
                    Text(f"🎯  {fake}  🎯", style="bold cyan")
                )
            )
            time.sleep(0.08 + i * 0.03)

    chosen = random.choice(names)

    # Fun task suggestions
    tasks = [
        "buying snacks today 🍕",
        "making the tea ☕",
        "doing the code review 👀",
        "presenting to the team 🎤",
        "picking the restaurant 🍽️",
        "writing the docs 📝",
        "fixing the bug 🐛",
        "ordering the pizza 🍕",
    ]

    console.print(
        Panel(
            f"[bold bright_green]\n   🎉  It's [bold bright_yellow]{chosen}[/bold bright_yellow]'s turn!\n\n"
            f"   📋  Suggested task: {random.choice(tasks)}\n\n"
            f"   [dim]No arguments. The wheel has spoken. 🎡[/dim]\n[/bold bright_green]",
            title="🎰 Who's Turn?",
            border_style="bold bright_magenta",
            padding=(1, 2),
        )
    )
