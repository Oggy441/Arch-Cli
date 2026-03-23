"""
===============================================
  Utility Commands — APIs & Info 🔧
===============================================
Fetch data from free public APIs:
  - Random fun facts
  - Weather
  - Motivational quotes
"""

import requests
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown
from rich.spinner import Spinner
from rich.live import Live

console = Console()


def _fetch_with_spinner(url, label="Fetching data..."):
    """Fetch a URL with a spinner. Returns response or None on error."""
    try:
        with Live(
            Spinner("dots", text=f"[bold yellow]{label}[/bold yellow]"),
            console=console,
            transient=True,
        ):
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
        return resp
    except requests.exceptions.Timeout:
        console.print(
            Panel(
                "[bold red]Request timed out ⏰ — The internet is napping.[/bold red]",
                title="❌ Timeout",
                border_style="red",
            )
        )
        return None
    except requests.exceptions.ConnectionError:
        console.print(
            Panel(
                "[bold red]Can't connect 🔌 — Are you sure you have internet?[/bold red]",
                title="❌ Connection Error",
                border_style="red",
            )
        )
        return None
    except Exception as e:
        console.print(
            Panel(
                f"[bold red]Something went sideways 💀\n\n{e}[/bold red]",
                title="❌ Error",
                border_style="red",
            )
        )
        return None


# ═══════════════════════════════════════════════════════════════════
#  MEME-FACT — Random useless fun fact
# ═══════════════════════════════════════════════════════════════════

def cmd_meme_fact(*_):
    """Fetch and display a random fun/useless fact."""
    resp = _fetch_with_spinner(
        "https://uselessfacts.jsph.pl/api/v2/facts/random?language=en",
        "Digging up useless knowledge... 🤓",
    )
    if resp is None:
        return

    try:
        data = resp.json()
        fact = data.get("text", "No fact found... the universe is empty 🕳️")
    except Exception:
        fact = "Couldn't parse the fact... the API is speaking in tongues 👅"

    console.print(
        Panel(
            f"[bold bright_white]{fact}[/bold bright_white]",
            title="🤓 Random Useless Fact",
            subtitle="[dim]Source: uselessfacts.jsph.pl[/dim]",
            border_style="bold bright_cyan",
            padding=(1, 2),
        )
    )


# ═══════════════════════════════════════════════════════════════════
#  WEATHER — Fetch weather from wttr.in
# ═══════════════════════════════════════════════════════════════════

def cmd_weather(args):
    """Fetch and display current weather for a city using wttr.in."""
    if not args:
        console.print("[bold red]Usage: weather <city>[/bold red] — Which city? 🌤️")
        return

    city = " ".join(args)

    # Fetch JSON weather data
    resp = _fetch_with_spinner(
        f"https://wttr.in/{city}?format=j1",
        f"Checking the skies over {city}... 🌤️",
    )
    if resp is None:
        return

    try:
        data = resp.json()
        current = data["current_condition"][0]

        temp_c = current.get("temp_C", "?")
        temp_f = current.get("temp_F", "?")
        feels_c = current.get("FeelsLikeC", "?")
        humidity = current.get("humidity", "?")
        desc = current.get("weatherDesc", [{}])[0].get("value", "Unknown")
        wind_speed = current.get("windspeedKmph", "?")
        wind_dir = current.get("winddir16Point", "?")
        visibility = current.get("visibility", "?")
        uv_index = current.get("uvIndex", "?")

        # Weather emoji mapping
        desc_lower = desc.lower()
        if "sun" in desc_lower or "clear" in desc_lower:
            emoji = "☀️"
        elif "cloud" in desc_lower or "overcast" in desc_lower:
            emoji = "☁️"
        elif "rain" in desc_lower or "drizzle" in desc_lower:
            emoji = "🌧️"
        elif "snow" in desc_lower:
            emoji = "❄️"
        elif "thunder" in desc_lower or "storm" in desc_lower:
            emoji = "⛈️"
        elif "fog" in desc_lower or "mist" in desc_lower:
            emoji = "🌫️"
        else:
            emoji = "🌤️"

        # Build a rich table
        table = Table(
            title=f"{emoji} Weather in {city.title()}",
            title_style="bold bright_cyan",
            border_style="bright_blue",
            show_lines=True,
        )
        table.add_column("Metric", style="bold bright_yellow", min_width=16)
        table.add_column("Value", style="bold white", min_width=20)

        table.add_row("🌡️ Temperature", f"{temp_c}°C / {temp_f}°F")
        table.add_row("🤒 Feels Like", f"{feels_c}°C")
        table.add_row(f"{emoji} Condition", desc)
        table.add_row("💧 Humidity", f"{humidity}%")
        table.add_row("💨 Wind", f"{wind_speed} km/h {wind_dir}")
        table.add_row("👁️ Visibility", f"{visibility} km")
        table.add_row("☀️ UV Index", str(uv_index))

        console.print()
        console.print(table)
        console.print()

    except (KeyError, IndexError, ValueError) as e:
        console.print(
            Panel(
                f"[bold red]Couldn't parse weather data for '{city}' 🤷\n"
                f"Maybe try a different city name?\n\n{e}[/bold red]",
                title="❌ Parse Error",
                border_style="red",
            )
        )


# ═══════════════════════════════════════════════════════════════════
#  QUOTE — Random motivational quote
# ═══════════════════════════════════════════════════════════════════

def cmd_quote(*_):
    """Fetch a random motivational quote and display it beautifully."""
    resp = _fetch_with_spinner(
        "https://zenquotes.io/api/random",
        "Fetching wisdom from the universe... 🌌",
    )
    if resp is None:
        return

    try:
        data = resp.json()
        if isinstance(data, list) and len(data) > 0:
            quote_text = data[0].get("q", "No quote found.")
            author = data[0].get("a", "Unknown")
        else:
            quote_text = "The universe had nothing to say today."
            author = "The Void"
    except Exception:
        quote_text = "Couldn't parse the quote... the API is feeling philosophical."
        author = "Error-san"

    console.print(
        Panel(
            f'[bold italic bright_white]"{quote_text}"[/bold italic bright_white]\n\n'
            f"[dim bright_cyan]— {author}[/dim bright_cyan]",
            title="💬 Motivational Quote",
            border_style="bold bright_magenta",
            padding=(1, 3),
        )
    )
