import streamlit as st
import requests
import json

st.set_page_config(page_title="3D Gebäude Flug", layout="centered")

st.title("🏗️ AI Gebäude-Kameraflug")
st.write("Generiere Kamerafahrten und Architektur-Visualisierungen über OpenRouter.")

# API-Key sicher aus den Streamlit Secrets auslesen
api_key = st.secrets.get("OPENROUTER_API_KEY", "")

if not api_key:
    st.warning("⚠️ Keinen API-Key in den Streamlit Secrets gefunden! Bitte trage ihn im Cloud Dashboard ein.")

prompt = st.text_area(
    "Beschreibe die Kamerafahrt durch das Gebäude:",
    value="A smooth FPV drone shot flying through a modern glass villa, cinematic lighting, 4k",
    height=100
)

if st.button("Flug generieren", type="primary"):
    if not api_key:
        st.error("Bitte erst den API-Key konfigurieren!")
    else:
        with st.spinner("Anfrage wird an OpenRouter gesendet..."):
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://streamlit.io"
            }
            
            payload = {
                "model": "black-forest-labs/flux-1-dev",  # Hier kannst du auch Videomodelle eintragen
                "messages": [{"role": "user", "content": prompt}]
            }
            
            try:
                response = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=headers,
                    data=json.dumps(payload)
                )
                
                if response.status_code == 200:
                    st.success("Erfolgreich empfangen!")
                    res_data = response.json()
                    st.json(res_data)
                else:
                    st.error(f"Fehler {response.status_code}: {response.text}")
                    
            except Exception as e:
                st.error(f"Verbindungsfehler: {e}")
