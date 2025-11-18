import streamlit as st
import pandas as pd
from io import BytesIO
from pathlib import Path

from recon_engine import generate_reconciliation_file  # your backend logic


# -------------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------------
st.set_page_config(
    page_title="Recon File Generator",
    layout="wide"
)

# -------------------------------------------------------
# PATHS
# -------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

logo_path = STATIC_DIR / "logo.png"   # your actual logo


# -------------------------------------------------------
# HEADER — Perfect alignment + ~0.5 cm spacing
# -------------------------------------------------------

st.markdown(
    f"""
    <div style="
        display:flex;
        align-items:center;
        justify-content:center;
        gap:15px;                 /* ← 0.5 cm spacing */
        margin-top:20px;
        margin-bottom:40px;       /* space BEFORE Step 1 */
    ">
        <img src="static/logo.png" style="width:120px; border-radius:5px;">
        <h1 style="
            font-size:42px;
            margin:0;
            padding:0;
            line-height:1;
        ">
            Recon File Generator
        </h1>
    </div>
    """,
    unsafe_allow_html=True
)


# -------------------------------------------------------
# STEP 1 — FILE UPLOADS
# -------------------------------------------------------
st.header("Step 1 — Upload Inputs")

trial_balance_file = st.file_uploader(
    "Upload Trial Balance file",
    type=["xlsx"],
    key="trial_balance_upload"
)

entries_file = st.file_uploader(
    "Upload All Entries file",
    type=["xlsx"],
    key="entries_upload"
)

icp_code = st.text_input("Enter ICP Code", placeholder="Example: SKPVAB")


# -------------------------------------------------------
# STEP 2 — GENERATE BUTTON
# -------------------------------------------------------
st.write("---")
st.header("Step 2 — Generate Recon File")

generate_button = st.button("Generate Recon File", type="primary")


# -------------------------------------------------------
# PROCESS FILES
# -------------------------------------------------------
if generate_button:

    if not trial_balance_file or not entries_file or not icp_code.strip():
        st.error("❌ Please upload both files and enter an ICP code.")
        st.stop()

    with st.spinner("⏳ Generating reconciliation file..."):

        output_bytes = generate_reconciliation_file(
            trial_balance_file,
            entries_file,
            icp_code.strip().upper()
        )

    st.success("✅ Reconciliation file generated successfully!")

    st.download_button(
        label="📥 Download Reconciliation Workbook",
        data=output_bytes,
        file_name="Reconciliation_Mapped.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


# -------------------------------------------------------
# FOOTER
# -------------------------------------------------------
st.write("---")
st.caption("EE Internal Tool — Powered by Streamlit")





