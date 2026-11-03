import streamlit as st
import requests
import json

st.set_page_config(page_title="AI Adlerflug Simulation", layout="centered")

st.title("🦅 AI Adlerflug Simulation")
st.write("Generiere kinoreife Aufnahmen aus der Adlerperspektive über OpenRouter.")

# API-Key sicher aus den Streamlit Secrets auslesen
api_key = st.secrets.get("OPENROUTER_API_KEY", "")

if not api_key:
    st.warning("⚠️ Kein API-Key in den Streamlit Secrets gefunden! Bitte trage OPENROUTER_API_KEY im Cloud Dashboard ein.")

# Eingabefeld für den Adlerflug
prompt_input = st.text_area(
    "Describe what the eagle should do (Englisch für beste Ergebnisse):",
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

        with st.spinner("Generiere Adlerflug-Visualisierung..."):
            # Nutzt Gemini Flash für verlässliche multimodale Resultate über den OpenRouter Chat Endpunkt
            payload = {
                "model": "google/gemini-2.5-flash",
                "messages": [
                    {
                        "role": "user",
                        "content": f"Generate a high quality cinematic image of: {prompt_input}"
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

                    content = res_data["choices"][0]["message"]["content"]
                    st.write(content)
                else:
                    st.error(f"Fehler {response.status_code}: {response.text}")

            except Exception as e:
                st.error(f"Verbindungsfehler: {e}")
