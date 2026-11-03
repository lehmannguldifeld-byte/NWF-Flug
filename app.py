import streamlit as st
import requests
import json

st.set_page_config(page_title="BIT Lehrlings-Story (13 Bilder)", layout="wide")

st.title("🦅 Die Geschichte vom BIT-Schnuppern bis zum EFZ-Gipfel")
st.write("Generiere das erweiterte 13-Bilder-Storyboard deiner Geschichte über OpenRouter.")

api_key = st.secrets.get("OPENROUTER_API_KEY", "")

if not api_key:
    st.warning("⚠️ Bitte hinterlege deinen OPENROUTER_API_KEY in den Streamlit Secrets.")

# Stil-Anker für durchgehende visuelle Konsistenz
STYLE = "Photorealistic 8k cinematic film render, golden hour sunlight, warm color palette, highly detailed Swiss architecture and nature, "

# Die 13 aufeinander abgestimmten Szenen
scenes = [
    {
        "nr": "1",
        "title": "1. Empfang beim BIT-Schnuppertag",
        "desc": "Ein junger Schweizer Junge und ein Mädchen betreten motiviert das moderne BIT-Gebäude.",
        "prompt": STYLE + "A 15-year-old Swiss boy and a girl entering the bright modern reception hall of the BIT building in Switzerland, smiling with excitement, warm indoor lighting"
    },
    {
        "nr": "2",
        "title": "2. Erste Hands-on Erfahrung",
        "desc": "Beide tüfteln fasziniert an Tastaturen und Bildschirmen beim Programmieren.",
        "prompt": STYLE + "Close-up of the young boy and girl focused and happy, coding on glowing dual monitors in a high-tech Swiss IT lab, modern desk setup"
    },
    {
        "nr": "3",
        "title": "3. Motivation zu Hause",
        "desc": "Der Junge tippt am Abend voller Tatendrang seine Bewerbung am eigenen Laptop.",
        "prompt": STYLE + "The young Swiss boy sitting motivated at his bedroom desk at dusk, typing a job application on a laptop, warm desk lamp light"
    },
    {
        "nr": "4",
        "title": "4. Vorbereitung mit den Eltern",
        "desc": "Gemeinsam mit Mutter und Vater bespricht er am Esstisch die Bewerbungsunterlagen.",
        "prompt": STYLE + "The boy sitting at a cozy wooden family dining table with his supportive mother and father, looking over printed application documents together, proud family moment"
    },
    {
        "nr": "5",
        "title": "5. Das Bewerbungsgespräch",
        "desc": "Im Sitzungszimmer des BIT stellt sich der Junge im Gespräch mit den 3 Experten vor.",
        "prompt": STYLE + "Interior shot of a sleek glass conference room at BIT, the young boy sitting confidently with his parents, facing 3 friendly Swiss IT interviewers across a table"
    },
    {
        "nr": "6",
        "title": "6. Glücklicher Ausstieg aus dem BIT",
        "desc": "Glücklich und erleichtert verlässt die Familie das gläserne BIT-Gebäude.",
        "prompt": STYLE + "The boy and his parents walking outside the modern glass BIT building in Bern, smiling and high-fiving under a bright sunny sky"
    },
    {
        "nr": "7",
        "title": "7. Der Boten-Adler auf dem Dach",
        "desc": "Ein majestätischer Adler nimmt den Lehrvertrag auf dem Dach des BIT entgegen.",
        "prompt": STYLE + "A majestic golden eagle perched on top of the futuristic glass roof of the BIT building in Switzerland, holding a folded paper document with 'Lehrvertrag' written on it in its talons, dramatic sunset"
    },
    {
        "nr": "8",
        "title": "8. Landung im Garten des Mädchens",
        "desc": "Der Adler fliegt sanft über das Wohnhaus des Mädchens und lässt das Papier fallen.",
        "prompt": STYLE + "Aerial view of a picturesque Swiss family house, a paper document tumbling gently down from the talons of a flying eagle toward a young girl standing in the garden"
    },
    {
        "nr": "9",
        "title": "9. Die magische Verwandlung",
        "desc": "Ein goldenes Licht hüllt das Mädchen ein – sie verwandelt sich in einen kleinen Adler.",
        "prompt": STYLE + "The young Swiss girl in the garden surrounded by an ethereal glowing golden aura, soft magical transformation morphing her into a small beautiful young eagle"
    },
    {
        "nr": "10",
        "title": "10. Start in Richtung Berge",
        "desc": "Der große und der kleine Adler steigen gemeinsam bei strahlendem Sonnenschein auf.",
        "prompt": STYLE + "Two eagles, one large mentor eagle and one small eaglet, taking off together into a crystal blue sky above lush green Swiss hills, bright sunlight"
    },
    {
        "nr": "11",
        "title": "11. Flug durch den Regenschauer",
        "desc": "Das Wetter wechselt: Sie fliegen mutig durch einen Regenschauer mit Regenbogen.",
        "prompt": STYLE + "Dynamic shot of the two eagles flying through a dramatic summer rainstorm over Swiss mountain peaks, golden sunlight breaking through clouds with a colorful rainbow"
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
        "prompt": STYLE + "Close-up of two fully grown magnificent adult eagles perched side-by-side next to the 'EFZ' summit cross, panoramic view of Swiss Alps in the background, triumphant atmospheric mood"
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

        col1, col2 = st.columns(2)
        columns = [col1, col2] * 7  # Ausreichend Spalten-Zuordnungen für 13 Bilder

        for idx, scene in enumerate(scenes):
            with columns[idx]:
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
                                    st.image(image_entry["url"], use_container_width=True)
                                elif "b64_json" in image_entry:
                                    import base64
                                    img_bytes = base64.b64decode(image_entry["b64_json"])
                                    st.image(img_bytes, use_container_width=True)
                            else:
                                st.write("Keine Bild-URL empfangen.")
                                st.json(res_data)
                        else:
                            st.error(f"Fehler {res.status_code}: {res.text}")

                    except Exception as e:
                        st.error(f"Verbindungsfehler: {e}")
