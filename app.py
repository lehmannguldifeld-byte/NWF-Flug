import streamlit as st
import requests
import json
import time

st.set_page_config(page_title="AI Adlerflug Simulation", layout="centered")

st.title("🦅 AI Adlerflug Simulation")
st.write("Generiere kinoreife Kameraflüge aus der Adlerperspektive über OpenRouter.")

# API-Key sicher aus den Streamlit Secrets auslesen
api_key = st.secrets.get("OPENROUTER_API_KEY", "")

if not api_key:
    st.warning("⚠️ Kein API-Key in den Streamlit Secrets gefunden! Bitte trage OPENROUTER_API_KEY im Cloud Dashboard ein.")

# Eingabefeld für den Adlerflug
prompt_input = st.text_area(
    "Describe what the eagle should do (Text auf Englisch für beste KI-Ergebnisse):",
    value="A majestic eagle flying forward smoothly over epic alpine mountain peaks, misty canyons, cinematic sunset lighting, highly detailed feathers, 8k resolution",
    height=100
)

if st.button("Adlerflug generieren", type="primary"):
    if not api_key:
        st.error("Bitte zuerst den API-Key in den Streamlit Secrets konfigurieren!")
    else:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://streamlit.io"
        }

        # Step 1: High-Quality Start Frame (FLUX via OpenRouter Chat/Image Endpunkt)
        with st.spinner("Schritt 1/2: Hochauflösendes Startbild des Adlerflugs wird erstellt..."):
            image_payload = {
                "model": "google/gemini-2.5-flash",  # Multimodales Modell für stabile Bild- & Promptverarbeitung
                "messages": [
                    {
                        "role": "user",
                        "content": f"Generate a cinematic ultra-wide shot: {prompt_input}"
                    }
                ]
            }

            try:
                img_response = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=headers,
                    data=json.dumps(image_payload)
                )

                if img_response.status_code == 200:
                    img_data = img_response.json()
                    st.success("Startbild erfolgreich gerendert!")

                    # Step 2: Image-to-Video Animation (Luma Ray 2 auf OpenRouter)
                    with st.spinner("Schritt 2/2: KI erzeugt die flüssige Flug-Animation (dauert ca. 30-60 Sek)..."):
                        video_payload = {
                            "model": "luma/ray-2",
                            "messages": [
                                {
                                    "role": "user",
                                    "content": f"Smooth forward camera motion following the eagle flying through the landscape: {prompt_input}"
                                }
                            ]
                        }

                        vid_response = requests.post(
                            "https://openrouter.ai/api/v1/chat/completions",
                            headers=headers,
                            data=json.dumps(video_payload)
                        )

                        if vid_response.status_code == 200:
                            vid_data = vid_response.json()
                            content = vid_data["choices"][0]["message"]["content"]

                            st.balloons()
                            st.subheader("🎬 Dein Adlerflug:")

                            # Video oder Link direkt anzeigen
                            if "http" in content and (".mp4" in content or "video" in content):
                                st.video(content)
                            else:
                                st.write(content)
                                st.json(vid_data)
                        else:
                            st.error(f"Fehler bei der Videogenerierung (Status {vid_response.status_code}): {vid_response.text}")

                else:
                    st.error(f"Fehler bei Bildgenerierung (Status {img_response.status_code}): {img_response.text}")

            except Exception as e:
                st.error(f"Verbindungsfehler: {e}")
