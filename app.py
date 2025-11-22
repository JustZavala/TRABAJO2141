import os
import tempfile

import streamlit as st
from openai import OpenAI
from audio_recorder_streamlit import audio_recorder  # pip install audio-recorder-streamlit


# ---------------- CONFIG BÁSICA ---------------- #

st.set_page_config(page_title="Chatbot IA con Voz", page_icon="🎙️")

st.title("🎙️ Chatbot de IA con voz + texto")
st.caption("Habla o escribe, y el bot te responde en el mismo chat (OpenAI + Streamlit).")

# --- API KEY (barra lateral) --- #
default_key = ""
try:
    # Si estás en Streamlit Cloud y usas secrets.toml
    default_key = st.secrets["OPENAI_API_KEY"]
except Exception:
    # Si no hay secrets, intentamos con variable de entorno
    default_key = os.environ.get("OPENAI_API_KEY", "")

api_key = st.sidebar.text_input(
    "🔑 OpenAI API key",
    value=default_key,
    type="password",
    help="Crea tu API key en platform.openai.com y ponla aquí.",
)

if not api_key:
    st.sidebar.warning("Pon tu API key para empezar.")
    st.stop()

client = OpenAI(api_key=api_key)


# ---------------- ESTADO DE LA CONVERSACIÓN ---------------- #

if "messages" not in st.session_state:
    # Incluimos el mensaje de sistema solo una vez
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "Eres un asistente útil que responde SIEMPRE en español, "
                "de forma clara y relativamente breve."
            ),
        }
    ]

# Mostrar historial (sin el mensaje de sistema)
for msg in st.session_state.messages:
    if msg["role"] == "system":
        continue

    with st.chat_message("user" if msg["role"] == "user" else "assistant"):
        st.markdown(msg["content"])


# ---------------- FUNCIONES AUXILIARES ---------------- #

def transcribir_audio(audio_bytes: bytes) -> str:
    # Voz -> texto usando el Audio API de OpenAI (transcripción).
    # Guardamos los bytes en un archivo temporal .wav
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        tmp.write(audio_bytes)
        tmp.flush()
        tmp_path = tmp.name

    with open(tmp_path, "rb") as f:
        transcript = client.audio.transcriptions.create(
            model="gpt-4o-transcribe",  # también puedes usar "whisper-1"
            file=f,
        )

    text = getattr(transcript, "text", None)
    return text or str(transcript)


def sintetizar_voz(texto: str) -> bytes:
    # Texto -> voz usando el Audio API de OpenAI (text-to-speech).
    response = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=texto,
        format="mp3",
    )
    audio_bytes = response.read()
    return audio_bytes


def preguntar_al_modelo(user_text: str) -> str:
    # Llama al modelo de chat de OpenAI (Responses API) con el historial completo.
    # Añadimos el mensaje del usuario al historial
    st.session_state.messages.append({"role": "user", "content": user_text})

    # Creamos la respuesta
    response = client.responses.create(
        model="gpt-4.1-mini",  # puedes cambiar a otro modelo compatible
        input=st.session_state.messages,
    )

    # Atajo para extraer el texto generado
    assistant_text = response.output_text

    # Guardamos respuesta en el historial
    st.session_state.messages.append(
        {"role": "assistant", "content": assistant_text}
    )

    return assistant_text


# ---------------- ENTRADA POR VOZ ---------------- #

st.subheader("🎙️ Hablar con el bot")

st.write("Pulsa el botón, habla, y cuando termines volverá a ejecutarse la app.")

audio_bytes = audio_recorder(
    text="Hacer clic para grabar / parar",
    pause_threshold=2.0,  # se para solo si detecta silencio
)

voz_a_texto = None
if audio_bytes:
    st.audio(audio_bytes, format="audio/wav")
    with st.spinner("Transcribiendo tu voz..."):
        voz_a_texto = transcribir_audio(audio_bytes)
        st.write(f"**Lo que entendí:** {voz_a_texto}")


# ---------------- ENTRADA POR TEXTO ---------------- #

st.subheader("⌨️ O escribir al bot")
texto_usuario = st.chat_input("Escribe tu mensaje aquí...")

# Si hay texto proveniente de la voz y el usuario no escribió nada,
# usamos la transcripción como mensaje.
if voz_a_texto and not texto_usuario:
    texto_usuario = voz_a_texto

# Cuando haya algún mensaje de usuario (voz o texto),
# llamamos al modelo y mostramos la respuesta.
if texto_usuario:
    # Mostrar mensaje del usuario inmediatamente
    with st.chat_message("user"):
        st.markdown(texto_usuario)

    # Obtener respuesta del modelo
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            respuesta = preguntar_al_modelo(texto_usuario)
            st.markdown(respuesta)

            # Generar audio de la respuesta
            try:
                audio_respuesta = sintetizar_voz(respuesta)
                st.audio(audio_respuesta, format="audio/mp3")
            except Exception as e:
                st.warning(f"No pude generar audio de la respuesta: {e}")
