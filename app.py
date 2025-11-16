import time
import streamlit as st

# ─────────────────────────────
# CONFIGURACIÓN BÁSICA
# ─────────────────────────────
st.set_page_config(
    page_title="Tulkit Pay - Verificación DNI",
    page_icon="💳",
    layout="centered"
)

# Video tutorial (puedes cambiar la URL por tu propio video)
TULKIT_TUTORIAL_URL = "https://www.youtube.com/watch?v=ysz5NMXJiyU"

# ─────────────────────────────
# ESTILOS (modo oscuro elegante)
# ─────────────────────────────
def inject_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Poppins', sans-serif;
        }

        .stApp {
            background: radial-gradient(circle at top, #111827 0, #020617 55%);
        }

        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 2rem;
            max-width: 420px;
        }

        .brand {
            text-align: center;
            margin-bottom: 1.4rem;
        }

        .brand-logo {
            font-size: 2.1rem;
            font-weight: 700;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            background: linear-gradient(90deg, #38bdf8, #4f46e5);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .brand-sub {
            font-size: 0.9rem;
            color: #9ca3af;
        }

        .t-card {
            background: rgba(15, 23, 42, 0.95);
            border-radius: 18px;
            padding: 1.6rem 1.4rem;
            border: 1px solid rgba(148, 163, 184, 0.6);
            box-shadow: 0 22px 50px rgba(15, 23, 42, 0.8);
            color: #e5e7eb;
        }

        .t-title {
            font-size: 1.25rem;
            font-weight: 600;
            margin-bottom: 0.4rem;
        }

        .t-text {
            font-size: 0.9rem;
            color: #9ca3af;
            margin-bottom: 1rem;
        }

        .t-label {
            font-size: 0.85rem;
            color: #9ca3af;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def brand_header():
    st.markdown(
        """
        <div class="brand">
          <div class="brand-logo">Tulkit Pay</div>
          <div class="brand-sub">Verificación de identidad</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


inject_css()

# ─────────────────────────────
# ESTADO GLOBAL
# ─────────────────────────────
if "step" not in st.session_state:
    st.session_state.step = "dni"

if "dni_image" not in st.session_state:
    st.session_state.dni_image = None

if "verification_started" not in st.session_state:
    st.session_state.verification_started = False

if "verification_done" not in st.session_state:
    st.session_state.verification_done = False


def go_to(step_name: str):
    st.session_state.step = step_name


# ─────────────────────────────
# PANTALLA 1: SUBIR DNI
# ─────────────────────────────
def screen_dni():
    brand_header()

    st.markdown('<div class="t-card">', unsafe_allow_html=True)

    st.markdown('<div class="t-title">Documento de identidad</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="t-text">Sube una foto nítida del frente de tu DNI para comenzar la verificación.</div>',
        unsafe_allow_html=True,
    )

    tab_cam, tab_upload = st.tabs(["📷 Usar cámara", "📁 Subir imagen"])

    with tab_cam:
        dni_cam = st.camera_input("Toma una foto de tu DNI")
        if dni_cam is not None:
            st.session_state.dni_image = dni_cam
            st.success("DNI capturado desde la cámara.")

    with tab_upload:
        dni_file = st.file_uploader(
            "O selecciona una foto de tu DNI",
            type=["png", "jpg", "jpeg"],
            key="dni_file",
        )
        if dni_file is not None:
            st.session_state.dni_image = dni_file
            st.success("DNI subido desde archivo.")

    if st.session_state.dni_image is not None:
        st.image(
            st.session_state.dni_image,
            caption="Vista previa del DNI (prototipo)",
            use_column_width=True,
        )

    st.write("")
    if st.button("Continuar con la verificación"):
        if st.session_state.dni_image is None:
            st.warning("Por favor sube o captura primero la imagen de tu DNI.")
        else:
            st.session_state.verification_started = False
            st.session_state.verification_done = False
            go_to("verificando")

    st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────
# PANTALLA 2: VERIFICANDO (VIDEO)
# ─────────────────────────────
def screen_verificando():
    brand_header()

    st.markdown('<div class="t-card">', unsafe_allow_html=True)

    st.markdown('<div class="t-title">Verificando tu identidad…</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="t-text">Este proceso puede tardar hasta 2 minutos. No cierres esta ventana.</div>',
        unsafe_allow_html=True,
    )

    VERIFICATION_SECONDS = 20  # cambia a 120 para 2 minutos reales

    progress_bar = st.progress(0)
    tiempo_placeholder = st.empty()

    # Ejecutamos la simulación solo la primera vez
    if not st.session_state.verification_started:
        st.session_state.verification_started = True
        for i in range(VERIFICATION_SECONDS):
            time.sleep(1)
            pct = int((i + 1) / VERIFICATION_SECONDS * 100)
            progress_bar.progress(pct)
            restantes = VERIFICATION_SECONDS - i - 1
            tiempo_placeholder.markdown(
                f"<span class='t-label'>Tiempo estimado restante: <b>{restantes} s</b></span>",
                unsafe_allow_html=True,
            )
        st.session_state.verification_done = True

    if st.session_state.verification_done:
        progress_bar.progress(100)
        tiempo_placeholder.markdown(
            "<span class='t-label'>Tiempo estimado restante: <b>0 s</b></span>",
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # Aquí solo mostramos el video, como pediste
    st.video(TULKIT_TUTORIAL_URL)

    st.markdown("---")
    if st.session_state.verification_done and st.button("Finalizar verificación"):
        go_to("done")

    st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────
# PANTALLA 3: TERMINADO
# ─────────────────────────────
def screen_done():
    brand_header()

    st.markdown('<div class="t-card">', unsafe_allow_html=True)
    st.markdown('<div class="t-title">Identidad verificada (demo)</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="t-text">Tu documento ha sido verificado correctamente en este prototipo de Tulkit Pay.</div>',
        unsafe_allow_html=True,
    )

    if st.button("Volver a empezar"):
        st.session_state.step = "dni"
        st.session_state.dni_image = None
        st.session_state.verification_started = False
        st.session_state.verification_done = False

    st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────
# ROUTER PRINCIPAL
# ─────────────────────────────
def main():
    step = st.session_state.step

    if step == "dni":
        screen_dni()
    elif step == "verificando":
        screen_verificando()
    elif step == "done":
        screen_done()
    else:
        st.session_state.step = "dni"
        screen_dni()


if __name__ == "__main__":
    main()
