import time
from datetime import datetime
import streamlit as st

# ─────────────────────────────────────
# CONFIGURACIÓN BÁSICA
# ─────────────────────────────────────

st.set_page_config(
    page_title="Tulkit Pay - KYC en menos de 2 minutos",
    page_icon="💳",
    layout="centered"
)

# PON AQUÍ UN VIDEO REAL DE YOUTUBE (reemplaza VIDEO_ID_AQUI)
TULKIT_TUTORIAL_URL = "https://www.youtube.com/embed/VIDEO_ID_AQUI"

# ─────────────────────────────────────
# ESTILOS PERSONALIZADOS
# ─────────────────────────────────────

def inject_css():
    st.markdown(
        """
        <style>
        body {
            background: radial-gradient(circle at top left, #111827, #020617);
        }
        .block-container {
            padding-top: 1rem;
            padding-bottom: 3rem;
            max-width: 780px !important;
        }
        .tulkit-header {
            text-align: center;
            margin-bottom: 1.3rem;
        }
        .tulkit-logo {
            font-weight: 800;
            font-size: 1.9rem;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            color: #e5e7eb;
        }
        .tulkit-logo span {
            color: #38bdf8;
        }
        .tulkit-badge {
            display: inline-block;
            margin-top: 0.3rem;
            padding: 0.2rem 0.7rem;
            border-radius: 999px;
            background: linear-gradient(90deg, #4f46e5, #06b6d4);
            color: white;
            font-size: 0.75rem;
        }
        .tulkit-card {
            background: rgba(15, 23, 42, 0.9);
            border-radius: 18px;
            padding: 1.6rem 1.9rem;
            box-shadow: 0 22px 50px rgba(15, 23, 42, 0.55);
            border: 1px solid rgba(148, 163, 184, 0.6);
            color: #e5e7eb;
        }
        .tulkit-card h1, .tulkit-card h2, .tulkit-card h3 {
            color: #e5e7eb !important;
        }
        .stepper {
            display: flex;
            justify-content: center;
            gap: 0.9rem;
            margin-bottom: 1.2rem;
        }
        .stepper-item {
            display: flex;
            flex-direction: column;
            align-items: center;
            font-size: 0.72rem;
            color: #9ca3af;
        }
        .stepper-circle {
            width: 26px;
            height: 26px;
            border-radius: 999px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 0.25rem;
            font-size: 0.82rem;
            font-weight: 600;
        }
        .stepper-circle.active {
            background: linear-gradient(135deg, #4f46e5, #06b6d4);
            color: white;
            box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.35);
        }
        .stepper-circle.inactive {
            background: #111827;
            border: 1px solid #4b5563;
            color: #9ca3af;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def brand_header():
    st.markdown(
        """
        <div class="tulkit-header">
            <div class="tulkit-logo">Tulkit<span>Pay</span></div>
            <div class="tulkit-badge">Verificación KYC segura y rápida</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def stepper(active_step: int):
    # active_step: 1, 2 o 3
    labels = ["DNI", "Selfie", "Verificación"]
    html = '<div class="stepper">'
    for i, label in enumerate(labels, start=1):
        state_class = "active" if i == active_step else "inactive"
        html += f"""
        <div class="stepper-item">
            <div class="stepper-circle {state_class}">{i}</div>
            <div>{label}</div>
        </div>
        """
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


inject_css()

# ─────────────────────────────────────
# MANEJO DE ESTADO
# ─────────────────────────────────────

if "step" not in st.session_state:
    st.session_state.step = "welcome"

if "dni_file" not in st.session_state:
    st.session_state.dni_file = None

if "selfie_file" not in st.session_state:
    st.session_state.selfie_file = None


def go_to(step_name: str):
    st.session_state.step = step_name


# ─────────────────────────────────────
# PANTALLAS / PASOS
# ─────────────────────────────────────

def step_welcome():
    brand_header()
    with st.container():
        st.markdown('<div class="tulkit-card">', unsafe_allow_html=True)

        st.markdown("#### Bienvenido a tu verificación de identidad")
        st.write(
            """
            Antes de usar **Tulkit Pay**, necesitamos confirmar quién eres.  
            El proceso es **100% digital**, inspirado en experiencias como Roblox, pero 
            adaptado a una app financiera:

            - Identifícate con tu **DNI**.  
            - Toma una **selfie en vivo** (para reducir riesgos de deepfakes).  
            - Espera mientras verificamos tu información (máx. 2 minutos).
            """
        )

        col1, col2 = st.columns([2, 1])
        with col1:
            st.write(
                """
                🔒 Tus datos solo se usan para este flujo de demostración.  
                ⚠️ **Importante:** este prototipo no hace verificación real.
                """
            )
        with col2:
            st.metric("Tiempo estimado", "≈ 2 minutos")
            st.metric("Pasos", "3")

        st.markdown("---")
        if st.button("Continuar • Identificarme con DNI"):
            go_to("dni")

        st.markdown("</div>", unsafe_allow_html=True)


def step_dni():
    brand_header()
    stepper(1)

    st.markdown('<div class="tulkit-card">', unsafe_allow_html=True)

    st.markdown("### Paso 1 · Adjunta tu DNI")
    st.write("Sube una foto clara de tu **DNI**. Idealmente sin reflejos y con todos los datos legibles.")

    dni = st.file_uploader(
        "Adjunta la imagen de tu DNI",
        type=["png", "jpg", "jpeg"],
        help="Esta imagen solo se usa para el prototipo, no se envía a un servidor real.",
    )

    if dni is not None:
        st.session_state.dni_file = dni
        st.success("✅ DNI adjuntado correctamente.")
        st.image(dni, caption="Previsualización de tu DNI (demo)", use_column_width=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅ Volver al inicio"):
            go_to("welcome")
    with col2:
        if st.button("Continuar a selfie"):
            if st.session_state.dni_file is None:
                st.warning("Primero sube una imagen de tu DNI para continuar.")
            else:
                go_to("selfie")

    st.markdown("</div>", unsafe_allow_html=True)


def step_selfie():
    brand_header()
    stepper(2)

    st.markdown('<div class="tulkit-card">', unsafe_allow_html=True)

    st.markdown("### Paso 2 · Selfie en vivo")
    st.write(
        """
        Para evitar suplantaciones y deepfakes, te pediremos una **selfie tomada desde tu cámara**.  
        Asegúrate de:
        - Estar bien iluminado.
        - Mirar de frente.
        - No usar gorras, gafas oscuras ni filtros.
        """
    )

    tab_cam, tab_upload = st.tabs(["📷 Usar cámara", "📁 Subir imagen (opcional)"])

    with tab_cam:
        selfie_cam = st.camera_input("Toma tu selfie ahora")
        if selfie_cam is not None:
            st.session_state.selfie_file = selfie_cam
            st.success("✅ Selfie tomada correctamente desde la cámara.")

    with tab_upload:
        selfie_upload = st.file_uploader(
            "O bien, sube una imagen de tu rostro",
            type=["png", "jpg", "jpeg"],
            key="selfie_uploader",
        )
        if selfie_upload is not None:
            st.session_state.selfie_file = selfie_upload
            st.success("✅ Selfie subida correctamente (archivo).")

    if st.session_state.selfie_file is not None:
        st.image(
            st.session_state.selfie_file,
            caption="Previsualización de tu selfie (demo)",
            use_column_width=True,
        )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅ Volver al DNI"):
            go_to("dni")
    with col2:
        if st.button("Iniciar verificación"):
            if st.session_state.selfie_file is None or st.session_state.dni_file is None:
                st.warning("Debes adjuntar tu DNI y tu selfie para comenzar la verificación.")
            else:
                go_to("verifying")

    st.markdown("</div>", unsafe_allow_html=True)


def step_verifying():
    brand_header()
    stepper(3)

    st.markdown('<div class="tulkit-card">', unsafe_allow_html=True)

    st.markdown("### Verificando tu identidad")
    st.write(
        """
        Estamos verificando tu DNI y tu selfie contra nuestros sistemas.  
        Este proceso puede tardar **hasta 2 minutos**.
        """
    )

    VERIFICATION_SECONDS = 20  # Cambia a 120 si quieres 2 minutos reales

    progress_bar = st.progress(0)
    status_placeholder = st.empty()

    for i in range(VERIFICATION_SECONDS):
        time.sleep(1)
        pct = int((i + 1) / VERIFICATION_SECONDS * 100)
        progress_bar.progress(pct)
        remaining = VERIFICATION_SECONDS - i - 1
        status_placeholder.write(f"Tiempo restante estimado: **{remaining} s**")

    st.success("✅ Verificación completada (demo).")

    st.markdown("---")
    st.subheader("Mientras tanto, aprende a usar Tulkit Pay")
    st.write("Revisa este breve video mientras verificamos tu identidad:")

    # Si el video da error, revisa que la URL tenga un ID de video válido
    st.video(TULKIT_TUTORIAL_URL)

    st.markdown("---")
    if st.button("Continuar"):
        go_to("done")

    st.markdown("</div>", unsafe_allow_html=True)


def step_done():
    brand_header()

    st.markdown('<div class="tulkit-card">', unsafe_allow_html=True)

    st.markdown("### 🎉 Identidad verificada (simulada)")
    st.success("¡Listo! Tu identidad ha sido verificada correctamente (demo).")

    st.write(
        """
        En una implementación real de **Tulkit Pay**, ahora podrías:
        - Activar tu **tarjeta virtual con cripto**.
        - Ver opciones de **recarga**, cashback y beneficios.
        - Explorar la app completa sin restricciones.
        """
    )

    if st.button("Volver al inicio"):
        st.session_state.dni_file = None
        st.session_state.selfie_file = None
        go_to("welcome")

    st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────
# ROUTER PRINCIPAL
# ─────────────────────────────────────

def main():
    step = st.session_state.step

    if step == "welcome":
        step_welcome()
    elif step == "dni":
        step_dni()
    elif step == "selfie":
        step_selfie()
    elif step == "verifying":
        step_verifying()
    elif step == "done":
        step_done()
    else:
        go_to("welcome")
        step_welcome()


if __name__ == "__main__":
    main()
