# app.py
"""
AI Short Script Generator — Luxurious Transparent UI
- No API key needed
- Uses local tiny GPT-2 model if available
- Luxurious glassmorphic design
- Options: genre, tone, length, hook, characters, platform
- Export/download scripts
"""

import streamlit as st
import textwrap
import datetime

# Try to import transformers
USE_MODEL = False
try:
    from transformers import pipeline, set_seed
    import torch
    USE_MODEL = True
except Exception:
    USE_MODEL = False

st.set_page_config(page_title="Lux AI Scripter", layout="centered", initial_sidebar_state="expanded")

# Luxurious CSS
st.markdown("""
<style>
:root{--glass-bg: rgba(255,255,255,0.06); --glass-border: rgba(255,255,255,0.12); --accent: rgba(255,215,0,0.9);} 
.stApp { background: linear-gradient(135deg, rgba(10,10,20,0.85), rgba(5,10,30,0.85)); background-attachment: fixed; }
.glass { background: var(--glass-bg); border: 1px solid var(--glass-border); backdrop-filter: blur(8px) saturate(1.2); border-radius: 16px; padding: 18px; }
.huge { font-size:28px; font-weight:700; color: white; letter-spacing: -0.5px }
.muted { color: #cfd8dc; }
.accent { color: var(--accent); }
.controlsRow { display:flex; gap:8px; align-items:center; }
.footerSmall { font-size:12px; color:#98a7b3 }
</style>
""", unsafe_allow_html=True)

# Sidebar controls
with st.sidebar:
    st.markdown("<div class='glass'>", unsafe_allow_html=True)
    st.markdown("<div class='huge'>Lux AI Scripter</div>", unsafe_allow_html=True)
    st.markdown("<div class='muted'>Short scripts, reels, shorts & sketches — no API key needed.</div>", unsafe_allow_html=True)
    st.write("")
    
    genre = st.selectbox("Genre", ["Motivational", "Comedy", "Drama", "Romance", "Horror", "Educational", "Religious/Inspirational", "Product Promo", "Explainer"], index=0)
    tone = st.selectbox("Tone", ["Warm", "Funny", "Sarcastic", "Serious", "Emotional", "Businesslike", "Playful"], index=0)
    platform = st.selectbox("Target Platform", ["YouTube Short", "TikTok", "Instagram Reel", "Facebook", "Podcast Intro"], index=0)
    length = st.slider("Script length (seconds)", 15, 180, value=45, step=5)
    hook_strength = st.select_slider("Hook strength", options=["Mild", "Standard", "All-in"], value="All-in")
    add_characters = st.checkbox("Add named characters / roles", value=False)
    character_names = st.text_input("Characters (comma separated)", value="Hero, Sidekick") if add_characters else ""
    include_call_to_action = st.checkbox("Include CTA / Endline", value=True)
    st.write("")
    st.markdown("</div>", unsafe_allow_html=True)

# Main UI
st.markdown("<div class='glass' style='padding:22px'>", unsafe_allow_html=True)
st.markdown("<div style='display:flex; justify-content:space-between; align-items:center;'> <div class='huge'>AI Short Script Generator</div> <div class='muted'>Luxurious • Transparent • Offline-first</div></div>", unsafe_allow_html=True)

with st.form(key='script_form'):
    title = st.text_input("Script title / topic", value="A quick motivational boost for entrepreneurs")
    prompts_extra = st.text_area("Extra notes / keywords (tone, lines, props)", value="Use emotional hook, short punchlines, mention hustle and faith.")
    submitted = st.form_submit_button("Generate Script")

# Deterministic fallback generator
def fallback_generate(title, genre, tone, platform, length, hook_strength, chars, notes, cta):
    hook_map = {'Mild': 'What if I told you...?','Standard': 'Listen — this changed my whole year.','All-in': 'Stop scrolling. Your life could change in 30 seconds.'}
    hook = hook_map.get(hook_strength, 'Here’s something to think about:')
    
    tone_words = {'Warm': ['warmly'], 'Funny': ['jokingly'], 'Sarcastic': ['dryly'], 'Serious': ['firmly'], 'Emotional': ['softly'], 'Businesslike': ['strategically'], 'Playful': ['playfully']}
    twords = tone_words.get(tone, ['sincerely'])
    
    char_section = ''
    if chars:
        names = [c.strip() for c in chars.split(',') if c.strip()]
        for i, n in enumerate(names, start=1):
            char_section += f"{n}: (short descriptor)\n"
    
    approx_lines = max(3, int(length / 8))
    lines = []
    lines.append(hook)
    lines.append(f"Topic: {title} — {genre} | Tone: {tone} | Platform: {platform}")
    if notes:
        lines.append(f"Notes: {notes}")
    if char_section:
        lines.append("Characters:")
        lines.append(char_section)
    for i in range(approx_lines):
        lines.append(f"{i+1}. " + textwrap.shorten(f"This line carries the {twords[0]} punch and drives the idea home.", width=120))
    if cta:
        lines.append("END: " + ("Subscribe for more" if platform != 'Podcast Intro' else 'Follow our podcast'))
    return "\n\n".join(lines)

# Model-backed generator
GENERATOR = None
if USE_MODEL:
    try:
        GENERATOR = pipeline("text-generation", model="sshleifer/tiny-gpt2", device=-1 if not torch.cuda.is_available() else 0)
        set_seed(42)
    except Exception:
        GENERATOR = None

def model_generate(prompt, max_tokens=150):
    if not GENERATOR:
        return None
    try:
        out = GENERATOR(prompt, max_length=max_tokens, do_sample=True, top_p=0.9, top_k=50, num_return_sequences=1)
        text = out[0]['generated_text']
        if text.startswith(prompt):
            text = text[len(prompt):].strip()
        return text
    except Exception:
        return None

# Generate script
if submitted:
    st.markdown("<hr/>", unsafe_allow_html=True)
    st.markdown("<div class='muted'>Generating — crafting a luxurious short script for you...</div>", unsafe_allow_html=True)
    timestamp = datetime.datetime.utcnow().isoformat()
    
    prompt = f"Generate a short {genre} script titled '{title}' for {platform}. Tone: {tone}. Length approx {length} seconds. Hook: {hook_strength}. Extra notes: {prompts_extra}. Include CTA: {include_call_to_action}. Characters: {character_names}\n\nScript:"
    
    result_text = None
    if USE_MODEL and GENERATOR:
        result_text = model_generate(prompt, max_tokens=300)
    if not result_text:
        result_text = fallback_generate(title, genre, tone, platform, length, hook_strength, character_names, prompts_extra, include_call_to_action)
    
    st.subheader("Generated Script")
    st.text_area("Preview", value=result_text, height=360)
    
    st.download_button(label="Download .txt", data=result_text, file_name=f"script-{title[:30].strip().replace(' ','-')}.txt", mime='text/plain')
    
    st.markdown("""<div class='footerSmall'>Tip: For best results install the tiny GPT-2 model (transformers + torch). The app will automatically use it if available.</div>""", unsafe_allow_html=True)
else:
    st.markdown("<div class='muted'>Enter a title and options, then press Generate Script.</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
