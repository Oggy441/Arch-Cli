# Team Arch 🔥

A CLI tool we made for the friend group. Uses Google Gemini AI and Rich for terminal styling.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Gemini](https://img.shields.io/badge/AI-Google%20Gemini-orange)

## Quick Start

### Setup

```bash
pip install google-generativeai rich requests python-dotenv
```

Get a free API key from [aistudio.google.com](https://aistudio.google.com), then add it to your `.env`:

```env
GEMINI_API_KEY=your_key_here
```

### Run it

```bash
python teamarch.py
```

**Examples:**
```bash
python teamarch.py flip
python teamarch.py roast Alice
python teamarch.py weather London
```

## Commands

**AI stuff:**
- `roast <name>` - roast someone
- `hype <name>` - hype them up
- `team-lore` - make up lore
- `advice <topic>` - bad life advice
- `debate <topic>` - ai debates things
- `fortune` - random fortune
- `nickname <name>` - funny names
- `chat` - just chat with it

**Games:**
- `flip` - flip a coin
- `roll [sides]` - roll dice
- `pick <options>` - pick randomly
- `timer <seconds>` - countdown

**Utils:**
- `meme-fact` - random fact
- `weather <city>` - check weather
- `quote` - get a quote

**Team stuff:**
- `members` - who's in the team
- `add-member` - add someone new
- `whos-turn` - pick someone randomly

## Team

| Name | |
|------|---|
| Alice | 🏗️ |
| Bob | 💻 |
| Charlie | ✨ |
| Dave | 🧠 |
| Eve | 🚀 |
| Frank | ☕ |

## Troubleshooting

- No API key? → add it to `.env`
- Can't connect? → check your internet
- Weather broken? → try a bigger city
- members.json messed up? → delete it and use `add-member`