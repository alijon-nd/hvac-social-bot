import os
import requests
import json
import random
from config import OPENROUTER_API_KEY

HOOKS = [
    "Ever wondered",
    "Here's why",
    "Most homeowners don't know",
    "This happens more than you think",
    "The truth about",
    "Here's a quick tip",
    "What if I told you",
    "One thing we always check",
]

CONTENT_TYPES = [
    "educational", "behind-the-scenes", "customer-focused",
    "seasonal", "myth-busting", "storytelling"
]

HISTORY_LOG = "caption_history.json"

def load_history():
    if os.path.exists(HISTORY_LOG):
        with open(HISTORY_LOG, "r") as f:
            return json.load(f)
    return []

def save_history(history):
    with open(HISTORY_LOG, "w") as f:
        json.dump(history[-10:], f, indent=2)

def get_photo_description(filename):
    name = os.path.basename(filename)
    name = os.path.splitext(name)[0]
    name = name.replace("_", " ").replace("-", " ").strip()
    return name if name else "an HVAC system"

def generate_captions(photo_description, history):
    hook = random.choice(HOOKS)
    content_type = random.choice(CONTENT_TYPES)

    system_prompt = f"""You are a professional HVAC social media manager for AN Heating & Air.

Photo shows: {photo_description}
Use this hook to start: "{hook}..."
Content style: {content_type}

Generate 2 captions:
1. Facebook: 100-150 words, include https://www.anairconditioning.com naturally
2. Instagram: 40-60 words, 5 hashtags

Rules:
- 80% educational, 20% promotional
- Mention "AN Heating & Air" only ONCE per caption
- Use "you" and "your"
- Ask 1 rhetorical question
- No generic phrases, no sales pressure
- Natural, human tone
- Never repeat these previous captions: {history[-5:] if history else "None"}

Format:
FACEBOOK: [caption]
INSTAGRAM: [caption]"""

    payload = {
        "model": "meta-llama/llama-3.2-3b-instruct:free",
        "messages": [
            {"role": "system", "content": "You are an HVAC social media expert."},
            {"role": "user", "content": system_prompt}
        ],
        "temperature": 0.85,
        "max_tokens": 500
    }

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://www.anairconditioning.com",
        "X-Title": "HVAC Social Bot"
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        json=payload,
        headers=headers
    )
    response.raise_for_status()

    content = response.json()["choices"][0]["message"]["content"]

    fb_cap = ""
    ig_cap = ""
    if "FACEBOOK:" in content and "INSTAGRAM:" in content:
        parts = content.split("INSTAGRAM:")
        fb_part = parts[0].replace("FACEBOOK:", "").strip()
        ig_part = parts[1].strip() if len(parts) > 1 else ""
        fb_cap = fb_part
        ig_cap = ig_part
    else:
        lines = content.strip().split("\n\n")
        if len(lines) >= 2:
            fb_cap = lines[0].strip()
            ig_cap = lines[1].strip()
        else:
            fb_cap = content.strip()
            ig_cap = content.strip()

    return {"facebook": fb_cap, "instagram": ig_cap}
