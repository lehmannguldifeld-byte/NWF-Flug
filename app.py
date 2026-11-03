import streamlit as st
import requests
import json

st.set_page_config(page_title="BIT Lehrlings-Story", layout="wide")

st.title("🦅 Die Geschichte vom BIT-Schnuppern bis zum EFZ-Gipfel")
st.write("13-Bilder Storyboard mit exakter mobiler Reihenfolge und angepasster Bewerbungs-Szene.")

api_key = st.secrets.get("OPENROUTER_API_KEY", "")

if not api_key:
    st.warning("⚠️ Bitte hinterlege deinen OPENROUTER_API_KEY in den Streamlit Secrets.")

# Neutrale Stil-Vorgabe für durchgehende Optik
STYLE = "Photorealistic 8k cinematic film render, golden hour sunlight, warm color palette, highly detailed modern environment, "

scenes = [
    {
        "nr": "1",
        "title": "1. Empfang beim BIT-Schnuppertag",
        "desc": "Ein junger Teenie-Junge und ein Mädchen betreten motiviert das moderne BIT-Gebäude in Zollikofen.",
        "prompt": STYLE + "A 15-year-old teenage boy and a teenage girl entering the bright modern reception hall of a sleek glass Bundesamt für Informatik (BIT) building in Zollikofen, smiling with excitement, warm indoor lighting"
    },
    {
        "nr": "2",
        "title": "2. Erste Hands-on Erfahrung",
        "desc": "Beide tüfteln fasziniert an Tastaturen und Bildschirmen beim Programmieren.",
        "prompt": STYLE + "Close-up of a 15-year-old boy and girl focused and happy, coding on glowing dual monitors in a high-tech modern IT workplace, sleek desk setup"
    },
    {
        "nr": "3",
        "title": "3. Motivation zu Hause",
        "desc": "Der Junge tippt am Abend voller Tatendrang seine Bewerbung am eigenen Laptop.",
        "prompt": STYLE + "A teenage boy sitting motivated at his bedroom desk at dusk, typing a job Informatiker EFZ on a modern laptop, warm desk lamp light"
    },
    {
        "nr": "4",
        "title": "4. Vorbereitung mit den Eltern",
        "desc": "Gemeinsam mit Mutter und Vater bespricht er am Esstisch die Bewerbungsunterlagen.",
        "prompt": STYLE + "A teenage boy sitting at a cozy wooden dining table with his supportive mother and father, looking over printed Bewerbung documents together, proud family moment"
    },
    {
        "nr": "5",
        "title": "5. Das Bewerbungsgespräch",
        "desc": "Exakter Raum im BIT: 3 Interviewer (Lernender 3. LJ, 55-jährige HR-Frau mit roten Haaren, 57-jähriger Martin mit braunen Haaren) gegenüber von Schüler & Eltern. An der Wand hängt eine Tafel mit einem Tetris-Spiel.",
        "prompt": STYLE + "Interior shot of a modern office meeting room. On one side of the table sit 3 interviewers: a young male 3rd-year apprentice, a 55-year-old female HR employee with medium-length red hair, and a 57-year-old man named Martin with short brown hair. On the other side of the table sits the 15-year-old student with his mother and father. In the background on the wall, there is a blackboard with a colorful Tetris game drawn on it."
    },
    {
        "nr": "6",
        "title": "6. Glücklicher Ausstieg aus dem BIT",
        "desc": "Glücklich und erleichtert verlässt die Familie das moderne BIT-Gebäude in Zollikofen.",
        "prompt": STYLE + "A teenage boy and his parents walking outside a modern glass administrative BIT office building in Zollikofen, smiling and happy under a bright sunny sky"
    },
    {
        "nr": "7",
        "title": "7. Der Boten-Adler auf dem Dach",
        "desc": "Ein majestätischer Adler nimmt den Lehrvertrag auf dem Dach des BIT-Gebäudes entgegen.",
        "prompt": STYLE + "A majestic golden eagle perched on top of the modern glass roof of the BIT building in Zollikofen, holding a folded paper document in its talons, dramatic sunset light"
    },
    {
        "nr": "8",
        "title": "8. Landung im Garten des Mädchens",
        "desc": "Der Adler fliegt sanft über das Wohnhaus des Mädchens und lässt das Papier fallen.",
        "prompt": STYLE + "Aerial view of a quiet modern residential family house, a paper document tumbling gently down from the talons of a flying eagle toward a teenage girl standing in the garden"
    },
    {
        "nr": "9",
        "title": "9. Die magische Verwandlung",
        "desc": "Ein goldenes Licht hüllt das Mädchen ein – sie verwandelt sich in einen kleinen Adler.",
        "prompt": STYLE + "A teenage girl in a garden surrounded by an ethereal glowing golden aura, soft magical transformation morphing her into a small beautiful young eagle"
    },
    {
        "nr": "10",
        "title": "10. Start in Richtung Berge",
        "desc": "Der große und der kleine Adler steigen gemeinsam bei strahlendem Sonnenschein auf.",
        "prompt": STYLE + "Two eagles, one large mentor eagle and one small eaglet, taking off together into a crystal blue sky above rolling green hills, bright sunlight"
    },
    {
        "nr": "11",
        "title": "11. Flug durch den Regenschauer",
        "desc": "Das Wetter wechselt: Sie fliegen mutig durch einen Regenschauer mit Regenbogen über die Berglandschaft.",
        "prompt": STYLE + "Dynamic shot of the two eagles flying through a dramatic rainstorm over alpine mountain peaks, golden sunlight breaking through clouds with a colorful rainbow"
    },
    {
        "nr": "12",
        "title": "12. Der Anflug auf den EFZ-Gipfel",
        "desc": "Vor ihnen ragt der Berggipfel mit dem hölzernen Kreuz und den Lettern 'EFZ' empor.",
        "prompt": STYLE + "Cinematic shot of the two eagles soaring toward an epic Alpine summit with a majestic wooden summit cross marked with bold 'EFZ' lettering, volumetric morning light"
    },
    {
        "nr": "13",
        "title": "13. Das große Finale am Ziel",
        "desc": "Beide stolzen Adler landen am Gipfelkreuz – das Mädchen ist nun ein ausgewachsener Adler.",
        "prompt": STYLE + "Close-up of two fully grown magnificent adult eagles perched side-by-side next to the 'EFZ' summit cross, panoramic mountain view in the background, triumphant atmospheric mood"
    }
]

if st.button("🚀 13-Bilder Storyboard generieren", type="primary"):
    if not api_key:
        st.error("Kein API-Key vorhanden!")
    else:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        # Paarweise Erzeugung für perfekte mobile Sortierung (1, 2, 3, 4, 5...)
        for i in range(0, len(scenes), 2):
            col1, col2 = st.columns(2)
            
            # Linkes Bild im Paar
            with col1:
                scene = scenes[i]
                st.subheader(scene["title"])
                st.caption(scene["desc"])

                with st.spinner(f"Rendere Bild {scene['nr']}/13..."):
                    payload = {
                        "model": "bytedance-seed/seedream-4.5",
                        "prompt": scene["prompt"]
                    }

                    try:
                        res = requests.post(
                            "https://openrouter.ai/api/v1/images",
                            headers=headers,
                            data=json.dumps(payload)
                        )

                        if res.status_code == 200:
                            res_data = res.json()
                            if "data" in res_data and len(res_data["data"]) > 0:
                                image_entry = res_data["data"][0]
                                if "url" in image_entry:
                                    st.image(image_entry["url"], width="stretch")
                                elif "b64_json" in image_entry:
                                    import base64
                                    img_bytes = base64.b64decode(image_entry["b64_json"])
                                    st.image(img_bytes, width="stretch")
                            else:
                                st.write("Keine Bild-URL empfangen.")
                                st.json(res_data)
                        else:
                            st.error(f"Fehler {res.status_code}: {res.text}")
                    except Exception as e:
                        st.error(f"Verbindungsfehler: {e}")

            # Rechtes Bild im Paar (falls vorhanden)
            if i + 1 < len(scenes):
                with col2:
                    scene = scenes[i + 1]
                    st.subheader(scene["title"])
                    st.caption(scene["desc"])

                    with st.spinner(f"Rendere Bild {scene['nr']}/13..."):
                        payload = {
                            "model": "bytedance-seed/seedream-4.5",
                            "prompt": scene["prompt"]
                        }

                        try:
                            res = requests.post(
                                "https://openrouter.ai/api/v1/images",
                                headers=headers,
                                data=json.dumps(payload)
                            )

                            if res.status_code == 200:
                                res_data = res.json()
                                if "data" in res_data and len(res_data["data"]) > 0:
                                    image_entry = res_data["data"][0]
                                    if "url" in image_entry:
                                        st.image(image_entry["url"], width="stretch")
                                    elif "b64_json" in image_entry:
                                        import base64
                                        img_bytes = base64.b64decode(image_entry["b64_json"])
                                        st.image(img_bytes, width="stretch")
                                else:
                                    st.write("Keine Bild-URL empfangen.")
                                    st.json(res_data)
                            else:
                                st.error(f"Fehler {res.status_code}: {res.text}")
                        except Exception as e:
                            st.error(f"Verbindungsfehler: {e}")
