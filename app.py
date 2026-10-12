
import hashlib
import io
import time

import streamlit as st
from pypdf import PdfReader

from chunker import split_text
from retriever import build_index, retrieve
from generator import generate_answer


# -------------------- PAGE CONFIG --------------------

st.set_page_config(
    page_title="DocuMind | AI Document Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)


# -------------------- CUSTOM STYLING --------------------

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

    :root {
        --bg: #0b1020;
        --panel: #111a2e;
        --border: rgba(148, 163, 184, 0.16);
        --muted: #9caac2;
        --accent: #818cf8;
        --text: #edf2ff;
    }

    .stApp {
        background:
            radial-gradient(ellipse at 15% 0%, #182343 0%, transparent 38%),
            radial-gradient(ellipse at 95% 15%, #20204a 0%, transparent 30%),
            var(--bg);
        color: var(--text);
        font-family: 'DM Sans', sans-serif;
    }

    h1, h2, h3, .brand-name {
        font-family: 'Space Grotesk', sans-serif !important;
        letter-spacing: -0.5px;
    }

    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    [data-testid="stSidebar"] {
        background: rgba(9, 14, 29, 0.96);
        border-right: 1px solid var(--border);
    }

    [data-testid="stSidebar"] .block-container {
        padding-top: 1.6rem;
    }

    .brand {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 25px;
    }

    .brand-icon {
        width: 43px;
        height: 43px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 14px;
        background: linear-gradient(135deg, #6366f1, #a78bfa);
        color: white;
        font-size: 22px;
        box-shadow: 0 8px 28px rgba(99, 102, 241, 0.25);
    }

    .brand-name {
        color: #f3f5ff;
        font-size: 23px;
        font-weight: 700;
        line-height: 1.15;
    }

    .brand-subtitle {
        color: var(--muted);
        font-size: 11px;
        margin-top: 4px;
    }

    .eyebrow {
        color: #a5b4fc;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 10px;
    }

    .hero-title {
        color: #f4f6ff;
        font-size: clamp(32px, 4vw, 46px);
        font-weight: 700;
        line-height: 1.12;
        margin: 0 0 12px 0;
    }

    .hero-description {
        color: #a7b4cb;
        font-size: 15px;
        line-height: 1.8;
        max-width: 680px;
        margin-bottom: 24px;
    }

    .gradient-text {
        background: linear-gradient(90deg, #a5b4fc, #c4b5fd, #67e8f9);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .panel {
        background: linear-gradient(
            145deg,
            rgba(24, 36, 61, 0.92),
            rgba(15, 23, 42, 0.92)
        );
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 22px;
        margin-bottom: 16px;
    }

    .panel-title {
        color: #edf2ff;
        font-size: 16px;
        font-weight: 700;
        margin-bottom: 7px;
    }

    .panel-description {
        color: #a3b0c7;
        font-size: 13px;
        line-height: 1.7;
    }

    .metric-card {
        background: rgba(17, 26, 46, 0.85);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 17px;
        min-height: 94px;
    }

    .metric-label {
        color: #9caac2;
        font-size: 12px;
        margin-bottom: 8px;
    }

    .metric-value {
        color: #eef2ff;
        font-family: 'Space Grotesk', sans-serif;
        font-size: 22px;
        font-weight: 700;
    }

    .status-dot {
        display: inline-block;
        height: 8px;
        width: 8px;
        border-radius: 50%;
        background: #34d399;
        margin-right: 8px;
    }

    .status-line {
        color: #b9c5db;
        font-size: 12px;
        margin-top: 8px;
    }

    .tech-pill {
        display: inline-block;
        color: #c7d2fe;
        background: rgba(99, 102, 241, 0.12);
        border: 1px solid rgba(129, 140, 248, 0.23);
        border-radius: 9px;
        padding: 7px 11px;
        font-size: 12px;
        margin: 4px 5px 4px 0;
    }

    .stButton > button {
        border-radius: 10px;
        min-height: 42px;
        font-weight: 600;
        transition: all 0.2s ease;
    }

    .stButton > button[kind="primary"] {
        background: linear-gradient(110deg, #6366f1, #8b5cf6);
        border: none;
        color: white;
    }

    .stButton > button:hover {
        border-color: #a5b4fc;
        transform: translateY(-1px);
    }

    .stTextInput input,
    .stTextArea textarea {
        background: #111a2e;
        color: #edf2ff;
        border-color: var(--border);
        border-radius: 10px;
    }

    [data-testid="stFileUploader"] {
        background: rgba(17, 26, 46, 0.55);
        border: 1px dashed rgba(129, 140, 248, 0.45);
        border-radius: 14px;
        padding: 10px;
    }

    [data-testid="stChatMessage"] {
        background: rgba(17, 26, 46, 0.72);
        border: 1px solid var(--border);
        border-radius: 15px;
        padding: 14px;
        margin-bottom: 12px;
    }

    [data-testid="stChatInput"] textarea {
        background: #111a2e;
        border: 1px solid rgba(129, 140, 248, 0.35);
        border-radius: 13px;
        color: #f3f5ff;
    }

    .footer {
        color: #75839d;
        font-size: 12px;
        text-align: center;
        border-top: 1px solid var(--border);
        padding-top: 20px;
        margin-top: 35px;
    }

    a {
        color: #a5b4fc !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# -------------------- SESSION STATE --------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "rag_data" not in st.session_state:
    st.session_state.rag_data = None


# -------------------- SIDEBAR --------------------

with st.sidebar:
    st.markdown(
        """
        <div class="brand">
            <div class="brand-icon">✳</div>
            <div>
                <div class="brand-name">DocuMind</div>
                <div class="brand-subtitle">YOUR DOCUMENTS, UNDERSTOOD</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("##### WORKSPACE")

    page = st.radio(
        "Navigation",
        ["💬  AI Workspace", "👨‍💻  About Developer"],
        label_visibility="collapsed",
        key="navigation",
    )

    st.divider()

    st.markdown("##### CURRENT SESSION")

    if st.session_state.rag_data:
        data = st.session_state.rag_data
        st.markdown(
            f"""
            <div class="panel">
                <div class="panel-title">📄 Document indexed</div>
                <div class="panel-description">
                    {data["filename"]}
                </div>
                <div class="status-line">
                    <span class="status-dot"></span>
                    Ready to answer questions
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.caption(f'{len(data["chunks"])} text chunks indexed')
    else:
        st.caption("No document loaded yet.")

    if st.button("＋  New conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown(
        """
        <div class="footer">
            Built with Python, FAISS & Gemini
        </div>
        """,
        unsafe_allow_html=True,
    )


# -------------------- REUSABLE COMPONENTS --------------------

def render_footer():
    st.markdown(
        """
        <div class="footer">
            DocuMind · AI-powered document intelligence
            <br><br>
            Built with curiosity and code.
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_hero(title, description):
    st.markdown(
        f"""
        <div class="eyebrow">DOCUMIND / AI DOCUMENT INTELLIGENCE</div>
        <div class="hero-title">{title}</div>
        <div class="hero-description">{description}</div>
        """,
        unsafe_allow_html=True,
    )


def render_sources(sources):
    if not sources:
        return

    with st.expander(f"📚 View sources ({len(sources)} chunks)"):
        for source in sources:
            st.markdown(
                f"**Chunk {source['chunk_id']}** · "
                f"Similarity: `{source['score']:.3f}`"
            )
            st.write(source["text"])
            st.divider()


# -------------------- AI WORKSPACE --------------------

if page == "💬  AI Workspace":

    render_hero(
        'Chat with your <span class="gradient-text">documents.</span>',
        "Upload a PDF, ask questions in natural language, "
        "and get answers grounded in your document with source references.",
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-label">RETRIEVAL</div>
                <div class="metric-value">FAISS</div>
                <div class="panel-description">Semantic search</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-label">GENERATION</div>
                <div class="metric-value">Gemini</div>
                <div class="panel-description">Context-aware answers</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-label">KNOWLEDGE SOURCE</div>
                <div class="metric-value">Your PDF</div>
                <div class="panel-description">Document-grounded AI</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")

    st.markdown(
        """
        <div class="panel">
            <div class="panel-title">📎 Upload your document</div>
            <div class="panel-description">
                Select a text-based PDF to build your searchable knowledge base.
                Your document is processed into chunks and indexed for retrieval.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type=["pdf"],
        help="For this version, upload one PDF at a time.",
    )

    if uploaded_file is not None:
        file_bytes = uploaded_file.getvalue()
        file_hash = hashlib.sha256(file_bytes).hexdigest()

        current_data = st.session_state.rag_data

        if current_data is None or current_data["file_hash"] != file_hash:
            try:
                with st.spinner("Reading, chunking and indexing your PDF..."):
                    reader = PdfReader(io.BytesIO(file_bytes))
                    pages = [
                        page.extract_text() or ""
                        for page in reader.pages
                    ]
                    text = "\n".join(pages).strip()

                    if not text:
                        st.error(
                            "No selectable text was found. "
                            "This PDF may require OCR."
                        )
                        st.stop()

                    chunks = split_text(
                        text,
                        chunk_size=1000,
                        overlap=150,
                    )

                    if not chunks:
                        st.error("No text chunks could be created.")
                        st.stop()

                    model, index = build_index(chunks)

                    st.session_state.rag_data = {
                        "filename": uploaded_file.name,
                        "file_hash": file_hash,
                        "chunks": chunks,
                        "model": model,
                        "index": index,
                    }

                    st.session_state.messages = []

                st.success(
                    f"Document indexed successfully · "
                    f"{len(chunks)} chunks created"
                )

            except Exception as exc:
                st.error(f"Unable to process this PDF: {exc}")
                st.stop()

        data = st.session_state.rag_data

        st.markdown(
            f"""
            <div class="panel">
                <div class="panel-title">✓ {data["filename"]}</div>
                <div class="panel-description">
                    Your document is ready. Ask a question below to get started.
                </div>
                <div class="status-line">
                    <span class="status-dot"></span>
                    {len(data["chunks"])} chunks indexed
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("### Conversation")

        if not st.session_state.messages:
            st.markdown(
                """
                <div class="panel">
                    <div class="panel-title">👋 Start exploring your document</div>
                    <div class="panel-description">
                        Ask for a summary, key facts, important dates,
                        comparisons or answers to specific questions.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            examples = [
                "Summarize this document",
                "What are the key points?",
                "List the important dates",
            ]

            example_cols = st.columns(3)

            for i, example in enumerate(examples):
                with example_cols[i]:
                    if st.button(example, use_container_width=True):
                        st.session_state.pending_question = example
                        st.rerun()

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                if message.get("sources"):
                    render_sources(message["sources"])

        pending_question = st.session_state.pop(
            "pending_question", None
        )

        question = st.chat_input(
            "Ask anything about your document..."
        )

        question = question or pending_question

        if question:
            st.session_state.messages.append(
                {"role": "user", "content": question}
            )

            with st.chat_message("user"):
                st.markdown(question)

            with st.chat_message("assistant"):
                try:
                    with st.spinner("Searching your document..."):
                        start = time.perf_counter()
                        results = retrieve(
                            question=question,
                            model=data["model"],
                            index=data["index"],
                            chunks=data["chunks"],
                            top_k=8,
                        )

                        retrieval_time = time.perf_counter() - start
                        st.caption(f"Retrieval completed in {retrieval_time:.2f}s")


                        with st.spinner("Generating your answer with Gemini..."):
                                answer = generate_answer(question, results)

                        st.markdown(answer)
                    render_sources(results)

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": answer,
                            "sources": results,
                        }
                    )

                except Exception as exc:
                    error_message = str(exc)

                    if "RESOURCE_EXHAUSTED" in error_message or "429" in error_message:
                        st.warning(
                     "The AI service has reached its current usage limit. "
                     "Please try again later."
                 )
                    else:
                     st.error(
                         "I couldn't generate an answer right now. "
                         "Please try again shortly."
                     )

                     st.caption(f"Technical details: {exc}")

    else:
        st.info("Upload a PDF above to start chatting with your document.")

    render_footer()


# -------------------- ABOUT DEVELOPER --------------------

elif page == "👨‍💻  About Developer":

    render_hero(
        'The developer behind <span class="gradient-text">DocuMind.</span>',
        "A little about the person, the engineering behind this project, "
        "and the ideas that brought it to life.",
    )

    st.markdown(
        """
        <div class="panel">
            <div style="font-size: 13px; color: #a5b4fc;
                        font-weight: 700; letter-spacing: 1.5px;">
                BUILT BY
            </div>
            <div style="font-family: 'Space Grotesk', sans-serif;
                        font-size: 34px; font-weight: 700;
                        margin-top: 12px; color: #f3f5ff;">
                Ayush Chainani
            </div>
            <div style="font-size: 16px; color: #c4b5fd;
                        margin-top: 5px;">
                AI & Data Science Engineer · Python Developer
            </div>
            <div class="panel-description" style="margin-top: 18px;">
                I enjoy building practical software that combines backend
                engineering, data, and AI. I focus on understanding how
                systems work under the hood and turning ideas into useful,
                working applications.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Connect with me")

    link1, link2 = st.columns(2)

    with link1:
        st.link_button(
            "🌐  Visit my portfolio",
            "https://ayushchainani.dev",
            use_container_width=True,
        )

    with link2:
        st.link_button(
            "💻  Explore my GitHub",
            "https://github.com/Codeayu",
            use_container_width=True,
        )

    st.write("")

    st.markdown("### Technologies I work with")

    st.markdown(
        """
        <div class="panel">
            <div class="panel-title">Backend development</div>
            <div style="margin-top: 10px;">
                <span class="tech-pill">Python</span>
                <span class="tech-pill">Django</span>
                <span class="tech-pill">Django REST Framework</span>
                <span class="tech-pill">Node.js</span>
                <span class="tech-pill">Express.js</span>
                <span class="tech-pill">REST APIs</span>
            </div>
        </div>

        <div class="panel">
            <div class="panel-title">AI & data</div>
            <div style="margin-top: 10px;">
                <span class="tech-pill">Retrieval-Augmented Generation</span>
                <span class="tech-pill">Sentence Transformers</span>
                <span class="tech-pill">FAISS</span>
                <span class="tech-pill">Gemini API</span>
                <span class="tech-pill">Scikit-learn</span>
                <span class="tech-pill">SQL</span>
            </div>
        </div>

        <div class="panel">
            <div class="panel-title">Frontend & databases</div>
            <div style="margin-top: 10px;">
                <span class="tech-pill">React</span>
                <span class="tech-pill">Streamlit</span>
                <span class="tech-pill">Tailwind CSS</span>
                <span class="tech-pill">PostgreSQL</span>
                <span class="tech-pill">MySQL</span>
                <span class="tech-pill">Git & GitHub</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Why I built DocuMind")

    st.markdown(
        """
        <div class="panel">
            <div class="panel-title">From documents to useful answers</div>
            <div class="panel-description">
                DocuMind is a hands-on exploration of Retrieval-Augmented
                Generation (RAG). Instead of asking an AI model to answer
                from general knowledge alone, the application retrieves
                relevant passages from a user's PDF and uses that context
                to generate an answer.
                <br><br>
                The goal is to understand the complete workflow:
                document extraction, chunking, embeddings, vector search,
                grounded generation, and an interface people can actually use.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### How DocuMind works")

    st.markdown(
        """
        <div class="panel">
            <div class="panel-title">01 · Extract</div>
            <div class="panel-description">
                Extract text from the uploaded PDF using pypdf.
            </div>
            <br>
            <div class="panel-title">02 · Chunk & embed</div>
            <div class="panel-description">
                Split text into manageable chunks and encode it using
                Sentence Transformers.
            </div>
            <br>
            <div class="panel-title">03 · Retrieve</div>
            <div class="panel-description">
                Use FAISS similarity search to find relevant document chunks.
            </div>
            <br>
            <div class="panel-title">04 · Generate</div>
            <div class="panel-description">
                Send the question and retrieved context to Gemini to produce
                a grounded response.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="footer">
            Designed and developed by Ayush Chainani
            <br>
            DocuMind · Built to learn, engineered to be useful.
        </div>
        """,
        unsafe_allow_html=True,
    )
