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

# URL del videotutorial (cámbiala por tu video real de YouTube)
TULKIT_TUTORIAL_URL = "https://www.youtube.com/embed/VIDEO_ID_AQUI"

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
    st.title("Tulkit Pay – Verificación de identidad")
    st.subheader("KYC en menos de 2 minutos ⏱️")

    st.write(
        """
        Antes de usar **Tulkit Pay**, necesitamos verificar tu identidad.  
        El proceso es rápido, guiado y 100% digital:
        
        1. Sube tu **DNI**.  
        2. Sube una **selfie**.  
        3. Espera mientras se verifica tu información (máx. 2 minutos).
        """
    )

    st.info("Este es un prototipo de demostración. No se realiza verificación real ni se envían datos a un servidor.")

    if st.button("Continuar • Identificarme con DNI"):
        go_to("dni")


def step_dni():
    st.title("Paso 1 de 2 · DNI")
    st.write("Sube una foto clara de tu **DNI** (frontal o frontal + reverso en la misma imagen).")

    dni = st.file_uploader(
        "Adjunta tu DNI",
        type=["png", "jpg", "jpeg"],
        help="Solo se usa para demostración. No se enviará a ningún servidor real."
    )

    if dni is not None:
        st.session_state.dni_file = dni
        st.success("✅ DNI adjuntado correctamente.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅ Volver"):
            go_to("welcome")
    with col2:
        if st.button("Continuar a selfie"):
            if st.session_state.dni_file is None:
                st.warning("Primero sube una imagen de tu DNI para continuar.")
            else:
                go_to("selfie")


def step_selfie():
    st.title("Paso 2 de 2 · Selfie con prueba de vida")
    st.write(
        """
        Ahora necesitamos una **selfie** tuya.  
        Intenta que tu rostro se vea bien iluminado y de frente.
        """
    )

    selfie = st.file_uploader(
        "Adjunta tu selfie",
        type=["png", "jpg", "jpeg"],
        help="Solo demostración: la imagen no se analiza realmente."
    )

    if selfie is not None:
        st.session_state.selfie_file = selfie
        st.success("✅ Selfie adjuntada correctamente.")

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


def step_verifying():
    st.title("Verificando tu identidad")
    st.markdown("### ⏳ Cargando...")

    st.write(
        """
        Estamos verificando tu DNI y tu selfie.  
        Este proceso puede tardar **hasta 2 minutos**.
        """
    )

    # Tiempo de verificación SIMULADO (en segundos)
    VERIFICATION_SECONDS = 20  # pon 120 para que sean 2 minutos reales

    # Barra de progreso y cuenta atrás simulada
    progress_bar = st.progress(0)
    status_placeholder = st.empty()

    # Video tutorial de Tulkit Pay mientras se “escanea”
    st.markdown("---")
    st.subheader("Mientras tanto, aprende a usar Tulkit Pay")
    st.write("Revisa este breve video mientras verificamos tu identidad:")
    st.video(TULKIT_TUTORIAL_URL)

    st.markdown("---")

    for i in range(VERIFICATION_SECONDS):
        time.sleep(1)
        pct = int((i + 1) / VERIFICATION_SECONDS * 100)
        progress_bar.progress(pct)
        remaining = VERIFICATION_SECONDS - i - 1
        status_placeholder.write(f"Tiempo restante estimado: **{remaining} s**")

    # Cuando termina la simulación
    go_to("done")
    st.experimental_rerun()


def step_done():
    st.title("✅ Identidad verificada (simulada)")
    st.success("¡Listo! Tu identidad ha sido verificada correctamente (demo).")

    st.write(
        """
        En una implementación real, en este punto Tulkit Pay:
        - Activaría tu cuenta.
        - Te mostraría tu tarjeta virtual.
        - Te permitiría empezar a recargar y usar tus beneficios.
        """
    )

    if st.button("Volver al inicio"):
        # Limpiamos archivos para un nuevo flujo
        st.session_state.dni_file = None
        st.session_state.selfie_file = None
        go_to("welcome")


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
        # fallback
        go_to("welcome")
        step_welcome()


if __name__ == "__main__":
    main()
