import os
import json
import random
import time
import requests
from config import OPENROUTER_API_KEY

# Dynamic content templates
HOOKS = [
    "Ever wondered", "Here's why", "Most homeowners don't know",
    "This happens more than you think", "The truth about",
    "Here's a quick tip", "What if I told you", "One thing we always check"
]

CONTENT_STYLES = [
    "educational", "behind-the-scenes", "customer-focused",
    "seasonal", "myth-busting", "storytelling"
]

HISTORY_FILE = "caption_history.json"

def load_history():
    """Load caption history to avoid repetition."""
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return []

def save_history(history):
    """Save caption history (keep last 10)."""
    with open(HISTORY_FILE, "w") as f:
        json.dump(history[-10:], f, indent=2)

def get_photo_description(filename):
    """Extract description from filename."""
    name = os.path.basename(filename)
    name = os.path.splitext(name)[0]
    name = name.replace("_", " ").replace("-", " ").strip()
    return name if name else "an HVAC system"

def generate_captions(photo_description, history):
    """Generate captions with retry logic."""
    
    # Build prompt
    hook = random.choice(HOOKS)
    style = random.choice(CONTENT_STYLES)
    
    user_prompt = f"""Photo shows: {photo_description}
Start with: "{hook}..."
Style: {style}

Generate 2 captions:
1. Facebook (100-150 words, include https://www.anairconditioning.com)
2. Instagram (40-60 words, 5 hashtags)

Rules:
- 80% educational, 20% promotional  
- Mention "AN Heating & Air" once max
- Natural, human tone, use "you/your"
- No generic phrases like "contact us"
- Previous captions to avoid: {history[-3:] if history else "None"}

Format exactly:
FB: [caption]
IG: [caption]"""

    payload = {
        "model": "meta-llama/llama-3.2-3b-instruct:free",
        "messages": [
            {"role": "system", "content": "You're an HVAC social media expert. Write engaging, professional captions."},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.8,
        "max_tokens": 400
    }
    
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://www.anairconditioning.com",
        "X-Title": "HVAC Bot"
    }
    
    # Retry logic
    for attempt in range(4):
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                json=payload,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 429:
                wait = (attempt + 1) * 8
                print(f"⏳ Rate limit, waiting {wait}s...")
                time.sleep(wait)
                continue
                
            response.raise_for_status()
            break
            
        except Exception as e:
            if attempt == 3:
                raise
            print(f"⚠️ Attempt {attempt+1} failed, retrying...")
            time.sleep(3)
    
    # Parse response
    content = response.json()["choices"][0]["message"]["content"]
    
    fb = ""
    ig = ""
    
    if "FB:" in content and "IG:" in content:
        parts = content.split("IG:")
        fb = parts[0].replace("FB:", "").strip()
        ig = parts[1].strip() if len(parts) > 1 else ""
    elif "FACEBOOK:" in content and "INSTAGRAM:" in content:
        parts = content.split("INSTAGRAM:")
        fb = parts[0].replace("FACEBOOK:", "").strip()
        ig = parts[1].strip() if len(parts) > 1 else ""
    else:
        # Fallback
        lines = content.strip().split("\n\n")
        fb = lines[0] if lines else content
        ig = lines[1] if len(lines) > 1 else content
    
    return {"facebook": fb, "instagram": ig}
