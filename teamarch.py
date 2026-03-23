"""
===============================================
  TEAM ARCH CLI 🔥
  "We go hard." — Team Arch
===============================================
Main entry point for the Team Arch CLI tool.
Opens directly in chat mode with slash-command support.

Run:  python teamarch.py
"""

import sys
import os

# ── Fix Windows Unicode encoding issues ─────────────────────────────
if sys.platform == "win32":
    os.environ.setdefault("PYTHONUTF8", "1")
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import json
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import print as rprint

# ── Load environment variables ──────────────────────────────────────
load_dotenv()

# ── Rich console ────────────────────────────────────────────────────
console = Console()

# ── ASCII Art Banner ────────────────────────────────────────────────
BANNER = r"""
[bold cyan]
  ████████╗███████╗ █████╗ ███╗   ███╗
  ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║
     ██║   █████╗  ███████║██╔████╔██║
     ██║   ██╔══╝  ██╔══██║██║╚██╔╝██║
     ██║   ███████╗██║  ██║██║ ╚═╝ ██║
     ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝
[/bold cyan]
[bold magenta]
      █████╗ ██████╗  ██████╗██╗  ██╗
     ██╔══██╗██╔══██╗██╔════╝██║  ██║
     ███████║██████╔╝██║     ███████║
     ██╔══██║██╔══██╗██║     ██╔══██║
     ██║  ██║██║  ██║╚██████╗██║  ██║
     ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝
[/bold magenta]
[bold yellow]        ⚡ We go hard 🔥 ⚡[/bold yellow]
"""

# ── Member colors for the roster box ────────────────────────────────
MEMBER_COLORS = [
    "bright_green",
    "bright_yellow",
    "bright_magenta",
    "bright_red",
    "bright_blue",
    "bright_cyan",
]

BAR_COLORS = [
    "green",
    "magenta",
    "red",
    "blue",
    "cyan",
    "yellow",
]

def show_roster_box():
    """Display the ARCH TEAM — ACTIVE ROSTER box on startup."""
    members_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "members.json")
    try:
        with open(members_file, "r", encoding="utf-8") as f:
            members = json.load(f)
    except Exception:
        return

    if not members:
        return

    box_w = 48
    title = "ARCH TEAM — ACTIVE ROSTER"
    pad_title = (box_w - 4 - len(title)) // 2

    console.print(f"  [bright_green]╔{'═' * (box_w - 2)}╗[/bright_green]")
    console.print(f"  [bright_green]║[/bright_green]{' ' * pad_title}[bold bright_white]{title}[/bold bright_white]{' ' * (box_w - 4 - pad_title - len(title))}  [bright_green]║[/bright_green]")
    console.print(f"  [bright_green]╠{'═' * (box_w - 2)}╣[/bright_green]")

    for i, member in enumerate(members):
        name = member.get("name", "Unknown")
        name_color = MEMBER_COLORS[i % len(MEMBER_COLORS)]
        bar_color = BAR_COLORS[i % len(BAR_COLORS)]
        status = "[ACTIVE]"

        name_display = f"[{name_color}]{name}[/{name_color}]"
        name_raw_len = len(name)
        padding = box_w - 12 - name_raw_len - len(status)

        console.print(
            f"  [{bar_color}]║[/{bar_color}] "
            f"[{bar_color}]●[/{bar_color}] "
            f"{name_display}"
            f"{' ' * max(1, padding)}"
            f"[bold bright_green]{status}[/bold bright_green]"
            f"  [{bar_color}]║[/{bar_color}]"
        )

    console.print(f"  [bright_green]╚{'═' * (box_w - 2)}╝[/bright_green]")
    console.print()


# ── Gemini Client Setup ─────────────────────────────────────────────

def get_gemini_client():
    """Initialize and return the Google GenAI client."""
    from google import genai

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key.strip() == "" or api_key == "your_key_here":
        console.print(
            Panel(
                "[bold red]Bro, the API key is missing or still the placeholder\n"
                "Set your GEMINI_API_KEY in the .env file!\n"
                "Get one free at: [link=https://aistudio.google.com]aistudio.google.com[/link][/bold red]",
                title="API Key Error",
                border_style="red",
            )
        )
        return None

    client = genai.Client(api_key=api_key)
    return client


# ═══════════════════════════════════════════════════════════════════
#  SLASH COMMAND REGISTRY
#  All commands available as /command inside chat mode.
#  Typing just "/" opens an interactive selector.
# ═══════════════════════════════════════════════════════════════════

# ── Mode-specific prompts for commands needing arguments ────────────
# Maps command name → (prompt_message, emoji, color)
COMMAND_PROMPTS = {
    "roast":    ("💀 Who to roast today",              "bold red"),
    "hype":     ("🔥 Who needs the hype",              "bold green"),
    "advice":   ("🧠 What topic needs terrible advice", "bold bright_magenta"),
    "debate":   ("⚔️  What dumb topic to debate",       "bold bright_cyan"),
    "nickname": ("🏷️  Who needs new nicknames",         "bold bright_green"),
    "weather":  ("🌤️  Which city to check",             "bold bright_yellow"),
    "roll":     ("🎲 How many sides (default 6)",      "bold bright_cyan"),
    "pick":     ("🎯 Options (space-separated)",       "bold bright_magenta"),
    "timer":    ("⏱️  How many seconds",                "bold bright_yellow"),
}


def build_slash_commands(client):
    """
    Build the slash-command routing table.
    Returns dict: name -> (handler, description, usage, category).
    """
    from commands.ai_commands import (
        cmd_roast, cmd_hype, cmd_team_lore, cmd_advice,
        cmd_debate, cmd_fortune, cmd_nickname,
    )
    from commands.fun_commands import (
        cmd_flip, cmd_roll, cmd_pick, cmd_timer,
    )
    from commands.util_commands import (
        cmd_meme_fact, cmd_weather, cmd_quote,
    )
    from commands.team_commands import (
        cmd_members, cmd_add_member, cmd_whos_turn,
    )

    return {
        # ── AI Commands ──
        "roast":      (lambda a: cmd_roast(client, a),      "Roast a team member",          "/roast <name>",           "⚡ AI"),
        "hype":       (lambda a: cmd_hype(client, a),       "Hype up a team member",        "/hype <name>",            "⚡ AI"),
        "team-lore":  (lambda a: cmd_team_lore(client),     "Generate epic Team Arch lore", "/team-lore",              "⚡ AI"),
        "advice":     (lambda a: cmd_advice(client, a),     "Get hilariously bad advice",   "/advice <topic>",         "⚡ AI"),
        "debate":     (lambda a: cmd_debate(client, a),     "AI debates a dumb topic",      "/debate <topic>",         "⚡ AI"),
        "fortune":    (lambda a: cmd_fortune(client),       "Get a cryptic fortune",        "/fortune",                "⚡ AI"),
        "nickname":   (lambda a: cmd_nickname(client, a),   "Generate funny nicknames",     "/nickname <name>",        "⚡ AI"),
        # ── Fun Commands ──
        "flip":       (lambda a: cmd_flip(),                "Flip a coin",                  "/flip",                   "🎮 Fun"),
        "roll":       (lambda a: cmd_roll(a),               "Roll an N-sided dice",         "/roll [sides]",           "🎮 Fun"),
        "pick":       (lambda a: cmd_pick(a),               "Pick a random option",         "/pick <opt1> <opt2> ...", "🎮 Fun"),
        "timer":      (lambda a: cmd_timer(a),              "Countdown timer",              "/timer <seconds>",        "🎮 Fun"),
        # ── Utility Commands ──
        "meme-fact":  (lambda a: cmd_meme_fact(),           "Random useless fun fact",      "/meme-fact",              "🔧 Util"),
        "weather":    (lambda a: cmd_weather(a),            "Check weather for a city",     "/weather <city>",         "🔧 Util"),
        "quote":      (lambda a: cmd_quote(),               "Random motivational quote",    "/quote",                  "🔧 Util"),
        # ── Team Commands ──
        "members":    (lambda a: cmd_members(),             "Show the team roster",         "/members",                "👥 Team"),
        "add-member": (lambda a: cmd_add_member(),          "Add a new team member",        "/add-member",             "👥 Team"),
        "whos-turn":  (lambda a: cmd_whos_turn(),           "Pick someone for a task",      "/whos-turn",              "👥 Team"),
    }


def _interactive_command_select(slash_commands):
    """
    Show an interactive fuzzy-search selector for slash commands.
    Returns (command_name, args_list) or (None, None) if cancelled.
    """
    import questionary
    from questionary import Style

    # Build choices with category labels
    choices = []
    for name, (_, desc, _, category) in slash_commands.items():
        label = f"/{name:<14} {desc}  [{category}]"
        choices.append(questionary.Choice(title=label, value=name))

    custom_style = Style([
        ("qmark",       "fg:#e74c3c bold"),       # red question mark
        ("question",    "fg:#c678dd bold"),        # purple prompt text
        ("pointer",     "fg:#e5c07b bold"),        # yellow pointer arrow
        ("highlighted", "fg:#61afef bold"),        # blue highlighted item
        ("selected",    "fg:#98c379 bold"),        # green selected item
        ("text",        "fg:#abb2bf"),             # light gray text
        ("instruction", "fg:#5c6370"),             # dim gray instruction
    ])

    selected = questionary.select(
        "Pick a command:",
        choices=choices,
        style=custom_style,
        instruction="(↑↓ to move, type to filter, Enter to select, Esc to cancel)",
        qmark="⚡",
    ).ask()

    if selected is None:
        return None, None

    # If the command needs arguments, prompt for them
    if selected in COMMAND_PROMPTS:
        prompt_msg, color = COMMAND_PROMPTS[selected]
        console.print()
        arg_input = console.input(f"[{color}]{prompt_msg} >[/{color}] ").strip()
        if not arg_input:
            # Let the handler show its own usage error
            return selected, []
        args = arg_input.split()
        return selected, args

    return selected, []


def show_slash_help(slash_commands):
    """Display all slash commands in a beautiful table."""
    table = Table(
        title="⚡ Slash Commands",
        title_style="bold bright_cyan",
        border_style="bright_magenta",
        show_lines=True,
    )
    table.add_column("Command", style="bold green", min_width=16)
    table.add_column("Description", style="white")
    table.add_column("Usage", style="dim cyan")

    sections = {
        "roast":     ">> AI-Powered",
        "flip":      ">> Fun & Games",
        "meme-fact": ">> Utilities",
        "members":   ">> Team Management",
    }

    for name, (_, desc, usage, _) in slash_commands.items():
        if name in sections:
            table.add_row(
                f"[bold bright_yellow]{sections[name]}[/]", "", "",
            )
        table.add_row(name, desc, usage)

    console.print(table)
    console.print(
        "\n[dim]Type [bold]/[/bold] to open the command picker. "
        "Or type [bold]/command[/bold] directly. "
        "Regular text goes to AI chat. "
        "Type [bold]exit[/bold] or [bold]quit[/bold] to leave.[/dim]\n"
    )


# ═══════════════════════════════════════════════════════════════════
#  UNIFIED CHAT MODE (default)
#  - Regular text → AI conversation
#  - / alone → interactive command picker
#  - /command → runs the slash command (with interactive arg prompt)
# ═══════════════════════════════════════════════════════════════════

def _run_slash_command(cmd_name, cmd_args, slash_commands):
    """Execute a slash command by name, prompting for args if needed."""
    if cmd_name not in slash_commands:
        console.print(
            f"[bold red]Unknown command:[/bold red] [cyan]/{cmd_name}[/cyan]\n"
            "[dim]Type [bold]/[/bold] to browse or [bold]/help[/bold] for the list.[/dim]"
        )
        return

    # If no args provided and the command needs args, prompt interactively
    if not cmd_args and cmd_name in COMMAND_PROMPTS:
        prompt_msg, color = COMMAND_PROMPTS[cmd_name]
        console.print()
        arg_input = console.input(f"[{color}]{prompt_msg} >[/{color}] ").strip()
        if arg_input:
            cmd_args = arg_input.split()

    handler, _, _, _ = slash_commands[cmd_name]
    handler(cmd_args)


def chat_mode(client, slash_commands):
    """
    The main interactive loop.
    Opens in AI chat by default.
    Type / to open command picker, /command for direct access.
    """
    from commands.ai_commands import (
        _generate_streaming, _get_loading_message, _stream_markdown_panel,
        MODEL_NAME, SYSTEM_PROMPT,
    )

    console.print(BANNER)
    show_roster_box()
    console.print(
        Panel(
            "[bold white]Welcome to Team Arch AI! 🔥\n\n"
            "Just start typing to chat with the AI.\n"
            "Type [green]/[/green] to open the command picker, "
            "or [green]/command[/green] directly.\n"
            "Type [red]exit[/red] or [red]quit[/red] to leave.[/bold white]",
            border_style="bright_cyan",
            padding=(1, 2),
        )
    )

    # ── Chat conversation history ──
    history = []

    if client is not None:
        from google.genai import types
    else:
        types = None

    while True:
        try:
            raw = console.input("\n[bold magenta]arch >[/bold magenta] ").strip()
            if not raw:
                continue

            # ── Exit ──
            if raw.lower() in ("exit", "quit", "q", "bye"):
                console.print("\n[bold cyan]Later, Team Arch! Stay legendary. 💀[/bold cyan]\n")
                break

            # ── Just "/" → open interactive picker ──
            if raw == "/":
                cmd_name, cmd_args = _interactive_command_select(slash_commands)
                if cmd_name is None:
                    console.print("[dim]Cancelled. Back to chat.[/dim]")
                    continue
                try:
                    _run_slash_command(cmd_name, cmd_args, slash_commands)
                except KeyboardInterrupt:
                    console.print("\n[yellow]Interrupted! Back to chat.[/yellow]")
                except Exception as e:
                    console.print(
                        Panel(f"[bold red]Something broke\n\n{e}[/bold red]",
                              title="Error", border_style="red")
                    )
                continue

            # ── Slash command with name typed ──
            if raw.startswith("/"):
                parts = raw[1:].split()
                cmd_name = parts[0].lower() if parts else ""
                cmd_args = parts[1:]

                if cmd_name in ("help", "h", "?"):
                    show_slash_help(slash_commands)
                    continue

                if cmd_name in ("clear", "reset"):
                    history.clear()
                    console.print("[bold yellow]🗑️ Chat history cleared! Fresh start.[/bold yellow]")
                    continue

                try:
                    _run_slash_command(cmd_name, cmd_args, slash_commands)
                except KeyboardInterrupt:
                    console.print("\n[yellow]Interrupted! Back to chat.[/yellow]")
                except Exception as e:
                    console.print(
                        Panel(f"[bold red]Something broke\n\n{e}[/bold red]",
                              title="Error", border_style="red")
                    )
                continue

            # ── Regular text → AI chat ──
            if client is None or types is None:
                console.print(
                    Panel(
                        "[bold red]No Gemini API key loaded!\n"
                        "Set your GEMINI_API_KEY in .env to chat.\n"
                        "You can still use /commands.[/bold red]",
                        title="API Error",
                        border_style="red",
                    )
                )
                continue

            # Add user message to history
            history.append(
                types.Content(role="user", parts=[types.Part.from_text(text=raw)])
            )

            loading_msg = _get_loading_message(client)
            try:
                from rich.spinner import Spinner
                from rich.live import Live

                with Live(
                    Spinner("dots", text=f"[bold yellow]{loading_msg}[/bold yellow]"),
                    console=console,
                    transient=True,
                ):
                    response = client.models.generate_content(
                        model=MODEL_NAME,
                        contents=history,
                        config=types.GenerateContentConfig(
                            system_instruction=SYSTEM_PROMPT,
                        ),
                    )

                reply = response.text or ""
                history.append(
                    types.Content(role="model", parts=[types.Part.from_text(text=reply)])
                )

                # Stream the response in a formatted panel
                console.print()
                _stream_markdown_panel(
                    text=reply.strip(),
                    title="Team Arch AI",
                    border_style="bold bright_magenta"
                )

            except KeyboardInterrupt:
                console.print("\n[yellow]Generation interrupted.[/yellow]")
            except Exception as e:
                console.print(f"[bold red]AI choked: {e}[/bold red]")

        except (KeyboardInterrupt, EOFError):
            console.print("\n[bold cyan]Later, Team Arch! Stay legendary. 💀[/bold cyan]\n")
            break


# ── Main ────────────────────────────────────────────────────────────

def main():
    """Main entry point — always opens in chat mode."""
    client = get_gemini_client()  # May be None if no API key
    slash_commands = build_slash_commands(client)
    chat_mode(client, slash_commands)


if __name__ == "__main__":
    main()
