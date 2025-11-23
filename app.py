# app.py
"""
AI Short Script Generator — GPT-4 powered
- Requires OpenAI API key
- Luxurious transparent UI
- Options: genre, tone, platform, length, characters, hook, CTA
- Fallback deterministic generator included
"""

import streamlit as st
import textwrap
import datetime
import openai

# -------------------------------
# Page config
# -------------------------------
st.set_page_config(page_title="GPT-4 Lux Script Generator", layout="centered", initial_sidebar_state="expanded")

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

# -------------------------------
# Sidebar controls
# -------------------------------
with st.sidebar:
    st.markdown("<div class='glass'>", unsafe_allow_html=True)
    st.markdown("<div class='huge'>GPT-4 Lux Script Generator</div>", unsafe_allow_html=True)
    st.markdown("<div class='muted'>Generate short scripts with GPT-4</div>", unsafe_allow_html=True)
    st.write("")
    
    api_key = st.text_input("OpenAI API Key", type="password")
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

# -------------------------------
# Main UI
# -------------------------------
st.markdown("<div class='glass' style='padding:22px'>", unsafe_allow_html=True)
st.markdown("<div style='display:flex; justify-content:space-between; align-items:center;'> <div class='huge'>AI Short Script Generator</div> <div class='muted'>GPT-4 powered • Luxurious • Transparent</div></div>", unsafe_allow_html=True)

with st.form(key='script_form'):
    title = st.text_input("Script title / topic", value="A quick motivational boost for entrepreneurs")
    prompts_extra = st.text_area("Extra notes / keywords (tone, lines, props)", value="Use emotional hook, short punchlines, mention hustle and faith.")
    submitted = st.form_submit_button("Generate Script")

# -------------------------------
# Fallback deterministic generator
# -------------------------------
def fallback_generate(title, genre, tone, platform, length, hook_strength, chars, notes, cta):
    hook_map = {'Mild': 'What if I told you...?','Standard': 'Listen — this changed my whole year.','All-in': 'Pay attention — this could change your day.'}
    hook = hook_map.get(hook_strength, 'Here’s something to think about:')
    
    tone_words = {'Warm': ['warmly'], 'Funny': ['jokingly'], 'Sarcastic': ['dryly'], 'Serious': ['firmly'], 'Emotional': ['softly'], 'Businesslike': ['strategically'], 'Playful': ['playfully']}
    twords = tone_words.get(tone, ['sincerely'])
    
    char_section = ''
    if chars:
        names = [c.strip() for c in chars.split(',') if c.strip()]
        for i, n in enumerate(names, start=1):
            char_section += f"{n}: (short descriptor)\n"
    
    lines = [hook]
    lines.append(f"Topic: {title} — {genre} | Tone: {tone} | Platform: {platform}")
    if notes:
        lines.append(f"Notes: {notes}")
    if char_section:
        lines.append("Characters:")
        lines.append(char_section)
    
    approx_lines = max(3, int(length / 8))
    for i in range(approx_lines):
        lines.append(f"{i+1}. This is a meaningful short script line written {twords[0]}.")
    
    if cta:
        lines.append("END: " + ("Subscribe for more" if platform != 'Podcast Intro' else 'Follow our podcast'))
    return "\n\n".join(lines)

# -------------------------------
# GPT-4 script generation
# -------------------------------
def gpt4_generate(api_key, title, genre, tone, platform, length, hook_strength, characters, notes, cta):
    if not api_key:
        return None
    openai.api_key = api_key
    prompt = f"""
    Generate a short script for a {platform}.
    Title: {title}
    Genre: {genre}
    Tone: {tone}
    Length: approx {length} seconds
    Hook: {hook_strength}
    Characters: {characters}
    Extra notes: {notes}
    Include CTA: {cta}
    
    Write 5-10 lines that are natural, varied, punchy, and suitable for a short video script.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,
            max_tokens=400
        )
        text = response['choices'][0]['message']['content'].strip()
        return text
    except Exception as e:
        return None

# -------------------------------
# Generate script action
# -------------------------------
if submitted:
    st.markdown("<hr/>", unsafe_allow_html=True)
    st.markdown("<div class='muted'>Generating script with GPT-4...</div>", unsafe_allow_html=True)
    
    result_text = gpt4_generate(api_key, title, genre, tone, platform, length, hook_strength, character_names, prompts_extra, include_call_to_action)
    
    if not result_text:
        st.warning("GPT-4 generation failed or API key missing. Using fallback generator.")
        result_text = fallback_generate(title, genre, tone, platform, length, hook_strength, character_names, prompts_extra, include_call_to_action)
    
    st.subheader("Generated Script")
    st.text_area("Preview", value=result_text, height=360)
    st.download_button(label="Download .txt", data=result_text, file_name=f"script-{title[:30].strip().replace(' ','-')}.txt", mime='text/plain')
    
    st.markdown("""<div class='footerSmall'>Tip: Enter a valid OpenAI API key for GPT-4 generation. Fallback ensures readable English scripts if API is missing or fails.</div>""", unsafe_allow_html=True)
else:
    st.markdown("<div class='muted'>Enter a title and options, then press Generate Script.</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
