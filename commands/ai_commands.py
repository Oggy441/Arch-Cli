"""
===============================================
  AI Commands — Powered by Google Gemini
===============================================
All commands that use the Gemini API to generate
creative, funny, and personality-filled responses.

Features:
  - Streaming text animation (like actual LLMs)
  - Dark humor personality
  - AI-generated loading messages
  - Short, punchy responses

Uses the new google.genai SDK.
"""

import random
import time
import sys
import os
import json
from rich.console import Console
from rich.panel import Panel
from rich.spinner import Spinner
from rich.live import Live
from rich.markdown import Markdown
from rich.text import Text

console = Console()

# ── Model name to use across all AI commands ────────────────────────
MODEL_NAME = "gemini-2.5-flash"

# ── System instruction (dark humor + short) ─────────────────────────
SYSTEM_PROMPT = (
    "You are the Team Arch AI — a brutally witty, dark-humored, and unapologetically savage "
    "AI assistant for a friend group called Team Arch. The members are Medhansh, Neeraj, Mansi, "
    "Loveleen, Pankaj, and Rehan. "
    "Your humor is DARK — think deadpan sarcasm, existential dread jokes, morbid wit, and "
    "the kind of burns that make people go 'bro that's foul 💀'. You roast like a villain "
    "with no filter but somehow it's still hilarious. "
    "CRITICAL: Keep ALL responses VERY SHORT — under 80 words MAX. Be concise, punchy, and "
    "hit hard. No filler, no fluff. Every word should count. Use emojis sparingly but effectively."
)

def _get_member_traits(name):
    """Helper to find a member's traits from members.json."""
    members_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "members.json")
    try:
        with open(members_file, "r", encoding="utf-8") as f:
            members = json.load(f)
            # Try to match the name (case-insensitive)
            for m in members:
                if m.get("name", "").lower() in name.lower() or name.lower() in m.get("name", "").lower():
                    return (
                        f"Role: {m.get('role', 'Unknown')}, "
                        f"Title: {m.get('title', 'Unknown')}, "
                        f"Catchphrase: '{m.get('catchphrase', '')}', "
                        f"Traits: {m.get('traits', 'None')}"
                    )
    except Exception:
        pass
    return "No specific info known about this person."

# ── Fallback loading messages (used if AI generation fails) ─────────
FALLBACK_LOADING = [
    "Consulting the dark side...",
    "Sacrificing brain cells for this...",
    "Downloading your replacement...",
    "Asking the voices in my head...",
    "Running on pure spite and caffeine...",
    "Generating toxicity report...",
    "Loading existential dread...",
    "Summoning your sleep paralysis demon...",
    "Calculating your worth... still loading...",
    "Bribing the AI with your data...",
    "Preparing emotional damage...",
    "Rewriting your will...",
    "Loading roast.exe...",
    "Your therapist would not approve...",
    "Googling 'how to be nice'... nah...",
]

# ── Cache for AI-generated loading messages ─────────────────────────
_ai_loading_cache = []


def _get_loading_message(client):
    """
    Get a loading message — tries AI-generated first, falls back to static.
    Generates a batch of 10 and caches them for reuse.
    """
    global _ai_loading_cache

    # If cache has messages, pop one
    if _ai_loading_cache:
        return _ai_loading_cache.pop()

    # Try to generate a batch with AI
    if client is not None:
        try:
            from google.genai import types
            resp = client.models.generate_content(
                model=MODEL_NAME,
                contents=(
                    "Generate exactly 10 funny, dark-humor loading messages for a CLI tool. "
                    "Like 'Consulting the ancient scrolls...' but edgier and funnier. "
                    "Each message should be SHORT (under 8 words), end with '...', and be on its own line. "
                    "No numbering, no bullets, just the messages. Make them savage, sarcastic, "
                    "and slightly unhinged. Think dark humor meets tech bro energy."
                ),
                config=types.GenerateContentConfig(
                    system_instruction="You generate short, funny loading messages. Dark humor only. No explanations.",
                ),
            )
            lines = [l.strip() for l in resp.text.strip().split("\n") if l.strip()]
            if lines:
                _ai_loading_cache.extend(lines)
                return _ai_loading_cache.pop()
        except Exception:
            pass

    # Fallback
    return random.choice(FALLBACK_LOADING)


def _stream_markdown_panel(text, title=None, border_style="bright_white", delay_char=0.005, delay_word=0.015):
    """
    Render text as Markdown inside a Panel, simulating a streaming LLM response
    so the response layout is properly formatted.
    """
    displayed_text = ""
    with Live(console=console, refresh_per_second=24) as live:
        for char in text:
            displayed_text += char
            live.update(
                Panel(
                    Markdown(displayed_text),
                    title=f"[bold]{title}[/bold]" if title else None,
                    border_style=border_style,
                    padding=(1, 2)
                )
            )
            if char == " ":
                time.sleep(delay_word)
            elif char in ".!?\n":
                time.sleep(delay_word * 3)
            else:
                time.sleep(delay_char)


def _generate_streaming(client, prompt, title="Team Arch AI", border_style="bold bright_cyan"):
    """
    Send a prompt to Gemini, show a spinner while waiting for the first chunk,
    then stream the response character by character in a panel.
    """
    if client is None:
        console.print(
            Panel(
                "[bold red]Bro, the API is cooked — No Gemini client loaded!\n"
                "Check your GEMINI_API_KEY in .env[/bold red]",
                title="API Error",
                border_style="red",
            )
        )
        return None

    loading_msg = _get_loading_message(client)

    try:
        from google.genai import types

        # Phase 1: Show spinner while waiting for first chunk
        full_text = ""
        with Live(
            Spinner("dots", text=f"[bold yellow]{loading_msg}[/bold yellow]"),
            console=console,
            transient=True,
        ):
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                ),
            )
            full_text = response.text or ""

        if not full_text.strip():
            console.print("[dim]AI returned nothing... even the AI is speechless.[/dim]")
            return None

        # Phase 2: Stream the text with Markdown layout
        console.print()
        _stream_markdown_panel(
            text=full_text.strip(),
            title=title,
            border_style=border_style
        )
        console.print()

        return full_text

    except Exception as e:
        console.print(
            Panel(
                f"[bold red]Bro, the API is cooked\n\n{e}[/bold red]",
                title="Gemini Error",
                border_style="red",
            )
        )
        return None


# ═══════════════════════════════════════════════════════════════════
#  ROAST — Generate a savage but funny roast
# ═══════════════════════════════════════════════════════════════════

def cmd_roast(client, args):
    """Roast a team member by name."""
    if not args:
        console.print("[bold red]Usage: roast <name>[/bold red] — Who are we destroying today?")
        return

    name = " ".join(args)
    member_info = _get_member_traits(name)
    
    prompt = (
        f"Roast '{name}' from Team Arch. Here is all their info: {member_info}. "
        "Make fun of them in a very funny but rude way using all this information. "
        "IMPORTANT: Use very simple and easy to understand English. "
        "Do NOT use big words, complex grammar, or high level English. "
        "Keep it short, under 80 words. End with a fake nice comment."
    )

    _generate_streaming(client, prompt, title=f"Roasting {name} 💀", border_style="bold red")


# ═══════════════════════════════════════════════════════════════════
#  HYPE — Over-the-top motivational speech
# ═══════════════════════════════════════════════════════════════════

def cmd_hype(client, args):
    """Hype up a team member with dark humor twist."""
    if not args:
        console.print("[bold red]Usage: hype <name>[/bold red] — Who needs the delusional confidence boost?")
        return

    name = " ".join(args)
    traits = _get_member_traits(name)
    
    prompt = (
        f"Hype up '{name}' from Team Arch. Context: {traits}. "
        "Do it with a dark humor twist. Start with insane "
        "over-the-top motivation like they're an anime protagonist, but sneak in some "
        "backhanded darkness. Make them feel powerful AND slightly concerned. Under 80 words."
    )

    _generate_streaming(client, prompt, title=f"HYPE TRAIN for {name}", border_style="bold green")


# ═══════════════════════════════════════════════════════════════════
#  TEAM LORE — Epic fictional backstory for Team Arch
# ═══════════════════════════════════════════════════════════════════

def cmd_team_lore(client, *_):
    """Generate dark/epic fictional lore for Team Arch."""
    prompt = (
        "Generate a SHORT but epic dark-fantasy lore for 'Team Arch'. "
        "Members: Medhansh (The Architect), Neeraj (The Debugger), Mansi (The Visionary), "
        "Loveleen (The Mastermind), Pankaj (The Tank), Rehan (The Wildcard). "
        "Make it sound like a cursed prophecy. Dark, dramatic, slightly unhinged. Under 100 words. "
        "End with a group motto that sounds cool but is lowkey threatening."
    )

    _generate_streaming(client, prompt, title="The Dark Lore of Team Arch", border_style="bold bright_yellow")


# ═══════════════════════════════════════════════════════════════════
#  ADVICE — Hilariously bad life advice
# ═══════════════════════════════════════════════════════════════════

def cmd_advice(client, args):
    """Get hilariously dark life advice on any topic."""
    if not args:
        console.print("[bold red]Usage: advice <topic>[/bold red] — What terrible decision do you need validated?")
        return

    topic = " ".join(args)
    prompt = (
        f"Give darkly hilarious and terrible advice about: '{topic}'. "
        "Sound extremely confident while being completely unhinged. "
        "3 short numbered tips max, each one worse than the last. "
        "Dark humor, existential dread energy. Under 80 words total."
    )

    _generate_streaming(client, prompt, title=f"Terrible Advice: {topic}", border_style="bold bright_magenta")


# ═══════════════════════════════════════════════════════════════════
#  DEBATE — Argue both sides of a dumb topic
# ═══════════════════════════════════════════════════════════════════

def cmd_debate(client, args):
    """Debate both sides of a dumb topic with dark humor."""
    if not args:
        console.print("[bold red]Usage: debate <topic>[/bold red] — Give me something stupid to argue about!")
        return

    topic = " ".join(args)
    prompt = (
        f"Debate '{topic}' with dark humor. "
        "FOR: 2 sentences max. AGAINST: 2 sentences max. "
        "VERDICT: 1 savage sentence declaring a winner. "
        "Be unhinged, be dark, be funny. Under 80 words total."
    )

    _generate_streaming(client, prompt, title=f"Debate: {topic}", border_style="bold bright_cyan")


# ═══════════════════════════════════════════════════════════════════
#  FORTUNE — Cryptic dark fortune cookie
# ═══════════════════════════════════════════════════════════════════

def cmd_fortune(client, *_):
    """Get a cryptic, dark fortune cookie message."""
    prompt = (
        "Generate ONE cryptic fortune cookie message with dark humor. "
        "Sound like an ancient curse disguised as wisdom. "
        "1-2 sentences MAX. Ominous but funny. Start with an emoji."
    )

    _generate_streaming(client, prompt, title="Your Fortune", border_style="bold yellow")


# ═══════════════════════════════════════════════════════════════════
#  NICKNAME — Generate creative/dark nicknames
# ═══════════════════════════════════════════════════════════════════

def cmd_nickname(client, args):
    """Generate 5 dark/funny nicknames for a team member."""
    if not args:
        console.print("[bold red]Usage: nickname <name>[/bold red] — Who needs a new identity?")
        return

    name = " ".join(args)
    prompt = (
        f"Generate 5 nicknames for '{name}' from Team Arch. Mix: some cool villain names, "
        "some dark roast-y ones, some that sound like gamer tags from 2009. "
        "Number them 1-5. One-line reason each. Keep it short and savage."
    )

    _generate_streaming(client, prompt, title=f"Nicknames for {name}", border_style="bold bright_green")



