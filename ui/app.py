import requests
import streamlit as st

API = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Contexta",
    layout="wide",
)

# ---------- Custom styling ----------
st.markdown(
    """
    <style>
        .block-container {
            padding-top: 3rem;
            max-width: 1100px;
        }
        .centered {
            text-align: center;
        }
        .subtitle {
            color: #6b7280;
            font-size: 1.1rem;
            margin-top: -0.5rem;
            margin-bottom: 2.5rem;
        }
        .section {
            margin-top: 3rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Header ----------
st.markdown("<h1 class='centered'>Contexta</h1>", unsafe_allow_html=True)
st.markdown(
    "<div class='centered subtitle'>Understand documents through context, not keywords.</div>",
    unsafe_allow_html=True,
)

st.divider()

# ---------- Upload ----------
st.markdown("<div class='section'></div>", unsafe_allow_html=True)
st.subheader("Upload document")

uploaded = st.file_uploader(
    "Select a PDF file",
    type=["pdf"],
    label_visibility="collapsed",
)

if uploaded:
    with st.spinner("Processing document..."):
        files = {
            "file": (uploaded.name, uploaded.getvalue(), "application/pdf")
        }
        r = requests.post(f"{API}/upload", files=files, timeout=300)
        st.success("Document uploaded and indexed successfully")
        st.json(r.json())

st.divider()

# ---------- Ask ----------
st.markdown("<div class='section'></div>", unsafe_allow_html=True)
st.subheader("Ask a question")

question = st.text_input(
    "",
    placeholder="What is this document about?",
)

if st.button("Get answer"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Finding the answer..."):
            r = requests.post(
                f"{API}/ask",
                json={"question": question},
                timeout=300,
            )
            data = r.json()

            st.markdown("### Answer")
            st.write(data.get("answer"))

            if data.get("sources"):
                st.markdown("### Sources")
                for s in data["sources"]:
                    st.write(
                        f"- {s.get('source')} (section {s.get('chunk')})"
                    )

st.divider()

# ---------- Report ----------
st.markdown("<div class='section'></div>", unsafe_allow_html=True)
st.subheader("Generate report")

report_type = st.selectbox(
    "Choose report type",
    [
        "Executive summary",
        "Risks and issues",
        "Performance overview",
    ],
)

rtype_map = {
    "Executive summary": "executive",
    "Risks and issues": "risks",
    "Performance overview": "performance",
}

if st.button("Generate report"):
    with st.spinner("Generating report..."):
        r = requests.post(
            f"{API}/report",
            json={"type": rtype_map[report_type]},
            timeout=300,
        )
        data = r.json()
        md = data.get("markdown", "")

        st.markdown(md)

        st.download_button(
            "Download report",
            data=md.encode("utf-8"),
            file_name=f"{rtype_map[report_type]}_report.md",
            mime="text/markdown",
        )
