import streamlit as st
import requests
import json

# Seiten-Konfiguration
st.set_page_config(page_title="3D Gebäude Visualisierung", layout="centered")

st.title("🏗️ AI Gebäude Visualisierung")
st.write("Erstelle Architektur-Visualisierungen und Raumkonzepte über OpenRouter.")

# API-Key sicher aus den Streamlit Secrets auslesen
api_key = st.secrets.get("OPENROUTER_API_KEY", "")

if not api_key:
    st.warning("⚠️ Kein API-Key in den Streamlit Secrets gefunden! Bitte trage OPENROUTER_API_KEY im Cloud Dashboard ein.")

# Eingabefeld für den Prompt
prompt = st.text_area(
    "Beschreibe den Raum oder das Gebäude:",
    value="A wide-angle photorealistic interior shot of a modern glass-wall villa lounge, cinematic architectural photography, 8k resolution",
    height=100
)

# Button zur Generierung
if st.button("Bild generieren", type="primary"):
    if not api_key:
        st.error("Bitte zuerst den API-Key in den Streamlit Secrets konfigurieren!")
    else:
        with st.spinner("Anfrage wird an OpenRouter gesendet..."):
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://streamlit.io"
            }
            
            # Payload mit funktionierender FLUX Modell-ID
            payload = {
                "model": "black-forest-labs/flux-1-schnell",
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }
            
            try:
                response = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=headers,
                    data=json.dumps(payload)
                )
                
                if response.status_code == 200:
                    res_data = response.json()
                    st.success("Erfolgreich generiert!")
                    
                    # Versuch, das Bild oder die Rückgabe-URL direkt anzuzeigen
                    try:
                        content = res_data["choices"][0]["message"]["content"]
                        
                        # Falls die Antwort eine Markdown-Bild-URL enthält
                        if "![" in content or "http" in content:
                            st.write(content)
                        else:
                            st.write(content)
                            
                    except (KeyError, IndexError):
                        # Falls das Format abweicht, rohes JSON als Fallback anzeigen
                        st.json(res_data)
                else:
                    st.error(f"Fehler {response.status_code}: {response.text}")
                    
            except Exception as e:
                st.error(f"Verbindungsfehler: {e}")
