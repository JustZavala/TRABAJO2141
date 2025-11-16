import time
import streamlit as st

# ─────────────────────────────
# CONFIGURACIÓN BÁSICA
# ─────────────────────────────
st.set_page_config(
    page_title="Tulkit Pay - KYC",
    page_icon="💳",
    layout="centered"
)

# Video de ejemplo (FUNCIONA en YouTube)
TULKIT_TUTORIAL_URL = "https://www.youtube.com/watch?v=ysz5NMXJiyU"

# ─────────────────────────────
# ESTADO GLOBAL
# ─────────────────────────────
if "step" not in st.session_state:
    st.session_state.step = "welcome"

if "dni_file" not in st.session_state:
    st.session_state.dni_file = None

if "selfie_file" not in st.session_state:
    st.session_state.selfie_file = None


def go_to(step_name: str):
    st.session_state.step = step_name


# ─────────────────────────────
# PANTALLAS
# ─────────────────────────────

def step_welcome():
    st.markdown("## 💳 Tulkit Pay")
    st.caption("Verificación rápida de identidad (demo)")

    st.write(
        """
        En menos de **2 minutos** verificamos tu identidad con:
        - Foto de tu **DNI**
        - Selfie tomada desde tu **cámara**
        """
    )

    if st.button("Empezar verificación"):
        go_to("dni")


def step_dni():
    st.markdown("### Paso 1 · Adjunta tu DNI")

    dni = st.file_uploader(
        "Sube una foto de tu DNI",
        type=["png", "jpg", "jpeg"]
    )

    if dni is not None:
        st.session_state.dni_file = dni
        st.success("DNI cargado correctamente.")
        st.image(dni, caption="Vista previa del DNI", use_column_width=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅ Volver"):
            go_to("welcome")
    with col2:
        if st.button("Continuar"):
            if st.session_state.dni_file is None:
                st.warning("Primero sube una imagen de tu DNI.")
            else:
                go_to("selfie")


def step_selfie():
    st.markdown("### Paso 2 · Selfie en vivo")

    st.write("Toma una selfie desde tu cámara (funciona en PC y celular).")

    tab_cam, tab_upload = st.tabs(["📷 Cámara", "📁 Subir archivo"])

    with tab_cam:
        selfie_cam = st.camera_input("Toma tu selfie")
        if selfie_cam is not None:
            st.session_state.selfie_file = selfie_cam
            st.success("Selfie tomada desde la cámara.")

    with tab_upload:
        selfie_upload = st.file_uploader(
            "O sube una foto de tu rostro",
            type=["png", "jpg", "jpeg"],
            key="selfie_upload"
        )
        if selfie_upload is not None:
            st.session_state.selfie_file = selfie_upload
            st.success("Selfie subida desde archivo.")

    if st.session_state.selfie_file is not None:
        st.image(
            st.session_state.selfie_file,
            caption="Vista previa de tu selfie",
            use_column_width=True
        )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅ Volver al DNI"):
            go_to("dni")
    with col2:
        if st.button("Iniciar verificación"):
            if st.session_state.selfie_file is None or st.session_state.dni_file is None:
                st.warning("Necesitas DNI y selfie para continuar.")
            else:
                go_to("verifying")


def step_verifying():
    st.markdown("### Paso 3 · Verificando tu identidad")
    st.write(
        """
        Estamos revisando tu DNI y tu selfie.  
        Esto puede tardar **hasta 2 minutos** (simulado).
        """
    )

    VERIFICATION_SECONDS = 20  # pon 120 para 2 minutos reales

    progress_bar = st.progress(0)
    placeholder = st.empty()

    for i in range(VERIFICATION_SECONDS):
        time.sleep(1)
        pct = int((i + 1) / VERIFICATION_SECONDS * 100)
        progress_bar.progress(pct)
        remaining = VERIFICATION_SECONDS - i - 1
        placeholder.write(f"Tiempo restante estimado: **{remaining} s**")

    st.success("Verificación completada (demo).")

    st.markdown("---")
    st.subheader("Mientras tanto, aprende a usar Tulkit Pay")

    st.video(TULKIT_TUTORIAL_URL)

    st.markdown("---")
    if st.button("Continuar"):
        go_to("done")


def step_done():
    st.markdown("### ✅ Identidad verificada (simulada)")
    st.write(
        """
        ¡Listo! En un sistema real ahora se activaría tu cuenta 
        y podrías empezar a usar Tulkit Pay.
        """
    )

    if st.button("Volver al inicio"):
        st.session_state.dni_file = None
        st.session_state.selfie_file = None
        go_to("welcome")


# ─────────────────────────────
# ROUTER PRINCIPAL
# ─────────────────────────────
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
