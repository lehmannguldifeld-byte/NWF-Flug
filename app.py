import streamlit as st
import requests
import json

st.set_page_config(page_title="3D Gebäude Visualisierung", layout="centered")

st.title("🏗️ AI Gebäude Visualisierung")
st.write("Erstelle Architektur-Visualisierungen über den OpenRouter Image Endpunkt.")

# API-Key aus den Streamlit Secrets auslesen
api_key = st.secrets.get("OPENROUTER_API_KEY", "")

if not api_key:
    st.warning("⚠️ Kein API-Key in den Streamlit Secrets gefunden! Bitte trage OPENROUTER_API_KEY im Cloud Dashboard ein.")

prompt = st.text_area(
    "Beschreibe den Raum oder das Gebäude:",
    value="A wide-angle photorealistic interior shot of a modern glass-wall villa lounge, cinematic architectural photography, 8k resolution",
    height=100
)

if st.button("Bild generieren", type="primary"):
    if not api_key:
        st.error("Bitte zuerst den API-Key in den Streamlit Secrets konfigurieren!")
    else:
        with st.spinner("Anfrage wird an OpenRouter generiert..."):
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            }
            
            # Bild-Payload für den Image API-Endpunkt
            payload = {
                "model": "bytedance-seed/seedream-4.5",  # Aktuell starkes & volatiles Bildmodell
                "prompt": prompt
            }
            
            try:
                # WICHTIG: Dedizierter Bild-Endpunkt /api/v1/images
                response = requests.post(
                    "https://openrouter.ai/api/v1/images",
                    headers=headers,
                    data=json.dumps(payload)
                )
                
                if response.status_code == 200:
                    res_data = response.json()
                    st.success("Erfolgreich generiert!")
                    
                    # Bild anzeigen (Base64 oder URL aus der Antwort)
                    if "data" in res_data and len(res_data["data"]) > 0:
                        image_entry = res_data["data"][0]
                        if "url" in image_entry:
                            st.image(image_entry["url"], caption="Generierter Raum")
                        elif "b64_json" in image_entry:
                            import base64
                            img_data = base64.b64decode(image_entry["b64_json"])
                            st.image(img_data, caption="Generierter Raum")
                    else:
                        st.json(res_data)
                else:
                    st.error(f"Fehler {response.status_code}: {response.text}")
                    
            except Exception as e:
                st.error(f"Verbindungsfehler: {e}")
