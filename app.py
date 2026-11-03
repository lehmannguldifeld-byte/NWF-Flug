import streamlit as st
import requests
import json

st.set_page_config(page_title="BIT Adler Storyboard", layout="wide")

st.title("🦅 BIT Lehrlings-Story: Der Adlerflug")
st.write("Generiere ein cineastisches Storyboard deiner Geschichte über OpenRouter.")

api_key = st.secrets.get("OPENROUTER_API_KEY", "")

if not api_key:
    st.warning("⚠️ Bitte hinterlege deinen OPENROUTER_API_KEY in den Streamlit Secrets.")

# Die 4 Szenen deiner Geschichte mit englischen Prompts für optimale Bildgenerierung
scenes = [
    {
        "title": "Szene 1: Der Start beim BIT",
        "desc": "Ein Adler steht stolz auf dem modernen Gebäude des Bundesamts für Informatik (BIT) und erhebt sich in den Himmel.",
        "prompt": "Cinematic low-angle shot of a majestic eagle perched on top of a modern angular glass architecture building in Switzerland, sharp details on eagle feathers, golden hour sunlight, 8k, photorealistic"
    },
    {
        "title": "Szene 2: Der Flug & Der Lehrvertrag",
        "desc": "Er gleitet über die Schweizer Landschaft und lässt über einem Schulhof das Blatt Papier ('Lehrvertrag') fallen.",
        "prompt": "FPV aerial view following a dark silhouette eagle flying over lush green Swiss hills and traditional village roofs, a paper document tumbling down gently from its talons over a lively schoolyard below, golden morning glow"
    },
    {
        "title": "Szene 3: Die magische Verwandlung",
        "desc": "Ein goldenes Licht umhüllt den Jungen auf dem Pausenhof und verwandelt ihn in einen kleinen Adler.",
        "prompt": "A glowing golden ethereal light surrounding a young Swiss boy in a schoolyard, magical transformation morphing him softly into a small beautiful eagle, warm glowing atmosphere, cinematic lighting"
    },
    {
        "title": "Szene 4: Gemeinsamer Rückflug zum BIT",
        "desc": "Großer und kleiner Adler fliegen Seite an Seite als Mentor und Lehrling zurück zum BIT.",
        "prompt": "Two eagles, one large and majestic, one smaller, flying side-by-side against a vibrant blue sky over a scenic Swiss landscape toward a modern building in the distance, cinematic wide angle, epic sunrise"
    }
]

if st.button("🎬 Storyboard generieren", type="primary"):
    if not api_key:
        st.error("Kein API-Key vorhanden!")
    else:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        cols = st.columns(2)  # 2x2 Raster für die Szenen

        for idx, scene in enumerate(scenes):
            with cols[idx % 2]:
                st.subheader(scene["title"])
                st.write(scene["desc"])

                with st.spinner(f"Generiere Bild für {scene['title']}..."):
                    payload = {
                        "model": "google/gemini-2.5-flash",
                        "messages": [
                            {
                                "role": "user",
                                "content": f"Generate a high quality cinematic image: {scene['prompt']}"
                            }
                        ]
                    }

                    try:
                        res = requests.post(
                            "https://openrouter.ai/api/v1/chat/completions",
                            headers=headers,
                            data=json.dumps(payload)
                        )
                        if res.status_code == 200:
                            content = res.json()["choices"][0]["message"]["content"]
                            st.write(content)
                        else:
                            st.error(f"Fehler {res.status_code}")
                    except Exception as e:
                        st.error(f"Fehler: {e}")
