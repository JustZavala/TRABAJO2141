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

# Video de ejemplo de YouTube (funciona para probar)
TULKIT_TUTORIAL_URL = "https://www.youtube.com/watch?v=ysz5NMXJiyU"

# ─────────────────────────────
# ESTILOS (simple modo oscuro)
# ─────────────────────────────
def inject_css():
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #111827;
        }
        .main, .block-container {
            color: #e5e7eb;
        }
        .kyc-card {
            background-color: #111827;
            padding: 24px 20px;
            border-radius: 18px;
            border: 1px solid #374151;
            box-shadow: 0 18px 40px rgba(0,0,0,0.4);
        }
        .kyc-title {
            font-size: 1.25rem;
            font-weight: 600;
            margin-bottom: 0.25rem;
        }
        .kyc-subtitle {
            font-size: 0.9rem;
            color: #9ca3af;
            margin-bottom: 1rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


inject_css()

# ─────────────────────────────
# ESTADO GLOBAL
# ─────────────────────────────
if "step" not in st.session_state:
    st.session_state.step = "choose_id"

if "id_type" not in st.session_state:
    st.session_state.id_type = "National ID"

if "id_image" not in st.session_state:
    st.session_state.id_image = None

if "selfie_image" not in st.session_state:
    st.session_state.selfie_image = None

if "verification_done" not in st.session_state:
    st.session_state.verification_done = False


def go_to(step_name: str):
    st.session_state.step = step_name


# ─────────────────────────────
# PANTALLAS
# ─────────────────────────────

def screen_choose_id():
    st.markdown("## 💳 Tulkit Pay")
    st.caption("KYC en menos de 2 minutos (demo)")

    with st.container():
        st.markdown('<div class="kyc-card">', unsafe_allow_html=True)

        st.markdown('<div class="kyc-title">Upload a photo ID</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="kyc-subtitle">We require a photo of a government ID to verify your identity.</div>',
            unsafe_allow_html=True
        )

        st.write("Choose 1 of the following options:")

        id_type = st.radio(
            "",
            ["Driver License", "National ID", "Passport", "Residency Permit"],
            index=1
        )
        st.session_state.id_type = id_type

        st.markdown("")  # pequeño espacio

        if st.button("Continue"):
            go_to("capture_id")

        st.markdown("</div>", unsafe_allow_html=True)


def screen_capture_id():
    id_type = st.session_state.id_type

    st.markdown("## 💳 Tulkit Pay")
    st.caption("KYC · Document step")

    with st.container():
        st.markdown('<div class="kyc-card">', unsafe_allow_html=True)

        st.markdown(f"### {id_type}")
        st.write("Take a clear photo of the front of your government ID.")

        tab_cam, tab_upload = st.tabs(["📷 Use camera", "📁 Upload photo"])

        with tab_cam:
            id_cam = st.camera_input("Take a photo of your ID")
            if id_cam is not None:
                st.session_state.id_image = id_cam
                st.success("ID captured from camera.")

        with tab_upload:
            id_file = st.file_uploader(
                "Or upload a photo of your ID",
                type=["png", "jpg", "jpeg"],
                key="id_file"
            )
            if id_file is not None:
                st.session_state.id_image = id_file
                st.success("ID uploaded from file.")

        if st.session_state.id_image is not None:
            st.image(
                st.session_state.id_image,
                caption="Preview of your ID (demo)",
                use_column_width=True
            )

        st.markdown("---")
        st.button("Continue on another device", help="Solo decorativo para la demo.", disabled=True)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("⬅ Back"):
                go_to("choose_id")
        with col2:
            if st.button("Continue to face verification"):
                if st.session_state.id_image is None:
                    st.warning("Please capture or upload a photo of your ID first.")
                else:
                    go_to("capture_face")

        st.markdown("</div>", unsafe_allow_html=True)


def screen_capture_face():
    st.markdown("## 💳 Tulkit Pay")
    st.caption("KYC · Face verification")

    with st.container():
        st.markdown('<div class="kyc-card">', unsafe_allow_html=True)

        st.markdown("### Face verification")
        st.write(
            """
            Look straight at the camera and take a selfie.  
            This helps us confirm that you are the owner of the ID.
            """
        )

        tab_cam, tab_upload = st.tabs(["📷 Use camera", "📁 Upload photo"])

        with tab_cam:
            selfie_cam = st.camera_input("Take your selfie")
            if selfie_cam is not None:
                st.session_state.selfie_image = selfie_cam
                st.success("Selfie captured from camera.")

        with tab_upload:
            selfie_file = st.file_uploader(
                "Or upload a selfie",
                type=["png", "jpg", "jpeg"],
                key="selfie_file"
            )
            if selfie_file is not None:
                st.session_state.selfie_image = selfie_file
                st.success("Selfie uploaded from file.")

        if st.session_state.selfie_image is not None:
            st.image(
                st.session_state.selfie_image,
                caption="Preview of your selfie (demo)",
                use_column_width=True
            )

        col1, col2 = st.columns(2)
        with col1:
            if st.button("⬅ Back to ID"):
                go_to("capture_id")
        with col2:
            if st.button("Start verification"):
                if st.session_state.selfie_image is None or st.session_state.id_image is None:
                    st.warning("You must provide both ID and selfie.")
                else:
                    st.session_state.verification_done = False
                    go_to("verifying")

        st.markdown("</div>", unsafe_allow_html=True)


def screen_verifying():
    st.markdown("## 💳 Tulkit Pay")
    st.caption("KYC · Processing")

    with st.container():
        st.markdown('<div class="kyc-card">', unsafe_allow_html=True)

        st.markdown("### Verifying your identity")
        st.write(
            """
            We’re checking your ID and face match our security rules.  
            This can take up to **2 minutes** (simulated here).
            """
        )

        VERIFICATION_SECONDS = 20  # cambia a 120 para 2 minutos reales

        progress_bar = st.progress(0)
        time_placeholder = st.empty()

        # Solo ejecutamos la simulación la primera vez
        if not st.session_state.verification_done:
            for i in range(VERIFICATION_SECONDS):
                time.sleep(1)
                pct = int((i + 1) / VERIFICATION_SECONDS * 100)
                progress_bar.progress(pct)
                remaining = VERIFICATION_SECONDS - i - 1
                time_placeholder.write(f"Estimated time remaining: **{remaining} s**")

            st.session_state.verification_done = True

        if st.session_state.verification_done:
            progress_bar.progress(100)
            time_placeholder.write("Estimated time remaining: **0 s**")
            st.success("Verification completed (demo).")

        st.markdown("---")
        st.subheader("While you wait, learn how to use Tulkit Pay")
        st.video(TULKIT_TUTORIAL_URL)

        st.markdown("---")
        if st.button("Continue"):
            go_to("done")

        st.markdown("</div>", unsafe_allow_html=True)


def screen_done():
    st.markdown("## 💳 Tulkit Pay")
    st.caption("KYC · Finished")

    with st.container():
        st.markdown('<div class="kyc-card">', unsafe_allow_html=True)

        st.markdown("### ✅ Identity verified (demo)")
        st.write(
            """
            Your identity has been verified successfully.  
            In a real app, your account would now be activated and ready to use.
            """
        )

        if st.button("Start over"):
            st.session_state.step = "choose_id"
            st.session_state.id_image = None
            st.session_state.selfie_image = None
            st.session_state.verification_done = False

        st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────
# ROUTER PRINCIPAL
# ─────────────────────────────
def main():
    step = st.session_state.step

    if step == "choose_id":
        screen_choose_id()
    elif step == "capture_id":
        screen_capture_id()
    elif step == "capture_face":
        screen_capture_face()
    elif step == "verifying":
        screen_verifying()
    elif step == "done":
        screen_done()
    else:
        st.session_state.step = "choose_id"
        screen_choose_id()


if __name__ == "__main__":
    main()
