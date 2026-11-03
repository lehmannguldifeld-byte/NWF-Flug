import streamlit as st
import requests
import json

st.set_page_config(page_title="BIT Adler Storyboard", layout="wide")

st.title("🦅 BIT Lehrlings-Story: Die visuelle Geschichte")
st.write("Generiere 4 zusammenhängende, hochauflösende Schlüsselbilder deiner Geschichte über OpenRouter.")

api_key = st.secrets.get("OPENROUTER_API_KEY", "")

if not api_key:
    st.warning("⚠️ Bitte hinterlege deinen OPENROUTER_API_KEY in den Streamlit Secrets.")

# Gemeinsamer Stil-Anker für visuelle Konsistenz
STYLE_PREFIX = "Photorealistic 8k cinematic film render, golden hour sunlight, warm color palette, highly detailed, "

# Die 4 Szenen deiner Geschichte mit abgestimmten Prompts
scenes = [
    {
        "title": "Szene 1: Der Start beim BIT",
        "desc": "Ein majestätischer Adler steht stolz auf dem modernen Glas-Gebäude des BIT in der Schweiz und erhebt sich in den Himmel.",
        "prompt": STYLE_PREFIX + "Low-angle shot of a majestic golden-brown eagle with sharp beak perched on top of a modern angular glass architecture building in Switzerland, eagle launching into the sky with wings spread, sharp feather details"
    },
    {
        "title": "Szene 2: Der Flug & Der Lehrvertrag",
        "desc": "Er gleitet über die Schweizer Landschaft und lässt über einem Pausenhof ein Blatt Papier ('Lehrvertrag') fallen.",
        "prompt": STYLE_PREFIX + "Wide-angle aerial view following the same majestic eagle flying over green Swiss hills and traditional village roofs, a single paper document tumbling gently down from its talons over a lively schoolyard below"
    },
    {
        "title": "Szene 3: Die magische Verwandlung",
        "desc": "Ein sanftes, goldenes Licht umhüllt den Jungen auf dem Pausenhof und verwandelt ihn sanft in einen kleinen Adler.",
        "prompt": STYLE_PREFIX + "A young Swiss boy in a schoolyard surrounded by a glowing ethereal golden magic light, soft magical transformation morphing him into a small beautiful eaglet, warm glowing atmosphere, innocent face"
    },
    {
        "title": "Szene 4: Gemeinsamer Rückflug zum BIT",
        "desc": "Großer und kleiner Adler fliegen Seite an Seite als Mentor und Lehrling zurück zum imposanten BIT-Gebäude.",
        "prompt": STYLE_PREFIX + "Two eagles, one large adult eagle and one small eaglet, flying side-by-side against a vibrant blue sky over a scenic Swiss landscape toward a modern glass building in the distance, majestic mentor and apprentice moment"
    }
]

if st.button("🖼️ Bilder-Story generieren", type="primary"):
    if not api_key:
        st.error("Kein API-Key vorhanden! Bitte trage ihn in den Streamlit Secrets ein.")
    else:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        # 2x2 Raster für die visuelle Darstellung
        col1, col2 = st.columns(2)
        columns = [col1, col2, col1, col2]

        for idx, scene in enumerate(scenes):
            with columns[idx]:
                st.subheader(scene["title"])
                st.caption(scene["desc"])

                with st.spinner(f"Rendere Bild für {scene['title']}..."):
                    payload = {
                        "model": "bytedance-seed/seedream-4.5",  # Leistungsstarkes Bildmodell auf OpenRouter
                        "prompt": scene["prompt"]
                    }

                    try:
                        # Aufruf des dedizierten IMAGE-Endpunkts
                        res = requests.post(
                            "https://openrouter.ai/api/v1/images",
                            headers=headers,
                            data=json.dumps(payload)
                        )

                        if res.status_code == 200:
                            res_data = res.json()
                            
                            # Bild-URL oder Base64 verarbeiten und anzeigen
                            if "data" in res_data and len(res_data["data"]) > 0:
                                image_entry = res_data["data"][0]
                                if "url" in image_entry:
                                    st.image(image_entry["url"], use_container_width=True)
                                elif "b64_json" in image_entry:
                                    import base64
                                    img_bytes = base64.b64decode(image_entry["b64_json"])
                                    st.image(img_bytes, use_container_width=True)
                            else:
                                st.write("Keine Bild-URL in der Antwort empfangen.")
                                st.json(res_data)
                        else:
                            st.error(f"Fehler {res.status_code}: {res.text}")

                    except Exception as e:
                        st.error(f"Verbindungsfehler: {e}")
