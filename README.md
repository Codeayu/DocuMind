📚 DocuMind — AI-Powered PDF Assistant

Chat with your documents. Get answers grounded in your content.

DocuMind is an AI-powered document assistant built using Retrieval-Augmented Generation (RAG). Upload a PDF, ask questions in natural language, and receive context-aware answers based on relevant passages retrieved from your document.

Instead of relying solely on an LLM's general knowledge, DocuMind retrieves relevant document chunks and provides them as context to the language model to generate grounded responses.

<p align="center">
  <a href="https://documind-by-ayush.streamlit.app/">
    <strong>🚀 Try the Live Demo</strong>
  </a>
  &nbsp; • &nbsp;
  <a href="https://github.com/Codeayu/DocuMind">
    <strong>💻 View Source Code</strong>
  </a>
</p>---

✨ Features

- 📄 PDF Upload: Upload a text-based PDF and build a searchable knowledge base.
- ✂️ Intelligent Chunking: Split extracted document text into manageable, overlapping chunks.
- 🧠 Semantic Embeddings: Generate vector embeddings using Sentence Transformers.
- 🔎 Semantic Search: Use FAISS to retrieve relevant document passages for a question.
- 🤖 AI-Powered Answers: Generate context-aware answers using the Google Gemini API.
- 🔄 Automatic Model Fallback: Attempt alternative configured Gemini models when a model encounters quota or service errors.
- 📚 Source References: Inspect retrieved chunks and similarity scores to understand which document passages informed an answer.
- 💬 Interactive Chat: Ask multiple questions about an uploaded document in a conversational interface.
- 🎨 Modern UI: A dark-themed Streamlit interface with a dedicated developer profile page.

🏗️ How It Works

DocuMind follows a Retrieval-Augmented Generation pipeline:

flowchart TD
    A[Upload PDF] --> B[Extract Text with PyPDF]
    B --> C[Split Text into Overlapping Chunks]
    C --> D[Generate Embeddings]
    D --> E[Build FAISS Vector Index]
    F[User Question] --> G[Embed Question]
    G --> H[Retrieve Relevant Chunks]
    E --> H
    H --> I[Question + Retrieved Context]
    I --> J[Gemini Model with Fallback]
    J --> K[Grounded Answer]
    K --> L[Display Answer and Sources]

Pipeline Explained

1. Document extraction: PyPDF extracts selectable text from the uploaded PDF.
2. Chunking: The extracted text is divided into chunks of approximately 1,000 characters with 150 characters of overlap.
3. Embedding generation: Sentence Transformers converts chunks into numerical vector representations.
4. Vector indexing: FAISS creates an index for efficient similarity search.
5. Retrieval: The application retrieves up to eight relevant chunks for the user's question.
6. Answer generation: The question and retrieved context are passed to a configured Gemini model.
7. Model fallback: If a model encounters a qualifying quota or service error, DocuMind attempts another configured model.
8. Source inspection: The retrieved chunks and their similarity scores are displayed alongside the answer.

🛠️ Tech Stack

Component| Technology
Language| Python
User Interface| Streamlit
PDF Processing| PyPDF
Embeddings| Sentence Transformers
Embedding Model| "all-MiniLM-L6-v2"
Vector Search| FAISS
Generative AI| Google Gemini API
Configuration| Python dotenv and Streamlit Secrets
Deployment| Streamlit Community Cloud
Version Control| Git and GitHub

📂 Project Structure

DocuMind/
├── .streamlit/
│   └── config.toml
├── app.py
├── main.py
├── chunker.py
├── retriever.py
├── generator.py
├── requirements.txt
├── .gitignore
├── README.md
└── .env                  # Local only; never commit

The ".streamlit/config.toml" file contains Streamlit configuration. The ".env" file is used for local development and should remain outside version control.

🚀 Run Locally

Prerequisites

- Python 3.10 or a compatible Python version supported by your dependencies
- A Google Gemini API key
- Git

1. Clone the repository

git clone https://github.com/Codeayu/DocuMind.git
cd DocuMind

2. Create a virtual environment

Windows:

python -m venv .venv
.venv\Scripts\activate

macOS / Linux:

python -m venv .venv
source .venv/bin/activate

3. Install dependencies

pip install -r requirements.txt

4. Configure your API key

Create a ".env" file in the project root:

GEMINI_API_KEY=your_gemini_api_key

Get your API key through "Google AI Studio" (https://aistudio.google.com/).

Security note: Never commit your ".env" file or expose your API key in source code, screenshots, or public repositories.

5. Launch the application

streamlit run app.py

Streamlit will provide a local URL, usually "http://localhost:8501".

☁️ Deployment

DocuMind is deployed using Streamlit Community Cloud.

Live application: https://documind-by-ayush.streamlit.app/

To deploy your own instance:

1. Fork or clone the repository.
2. Sign in to "Streamlit Community Cloud" (https://share.streamlit.io/).
3. Create an app connected to your GitHub repository.
4. Set the main file path to "app.py".
5. Add your Gemini API key under the app's Settings → Secrets:

GEMINI_API_KEY = "your_gemini_api_key"

6. Deploy the application.

🔄 Model Fallback and Reliability

DocuMind supports a configurable sequence of Gemini models.

When a configured model encounters a qualifying API error, such as quota exhaustion or a temporary service issue, the application can attempt the next model in the sequence.

This improves resilience, but it does not guarantee uninterrupted generation. Alternative models must be available to the API project and have usable quota. If all configured models fail, the application displays a fallback message.

⚠️ Current Limitations

- Supports text-based PDFs; scanned documents may require OCR.
- Answer quality depends on PDF text extraction, chunking, retrieval relevance, and model behavior.
- Answers are grounded in retrieved context, but may still contain errors. Verify important information against the original document.
- Gemini API quotas, model availability, and response times can affect generation.
- Large PDFs may require additional processing time and memory.
- The current implementation is designed for one uploaded PDF per active session.

🔮 Potential Improvements

- OCR support for scanned PDFs.
- Support for multiple documents and persistent knowledge bases.
- Hybrid retrieval combining keyword and semantic search.
- Reranking retrieved chunks for improved relevance.
- Retrieval evaluation with precision, recall, and ranking metrics.
- Streaming responses and improved generation-time feedback.
- More robust model availability checks and fallback monitoring.
- Automated tests and deployment checks.

👨‍💻 About the Developer

Ayush Chainani
AI & Data Science Engineer | Python Developer

I enjoy building practical software that combines backend engineering, data, and artificial intelligence. DocuMind is a hands-on project exploring how retrieval, vector search, and language models can work together to create useful document-based AI applications.

- 🌐 Portfolio: https://ayushchainani.dev
- 💻 GitHub: https://github.com/Codeayu
- 🚀 Live Project: https://documind-by-ayush.streamlit.app/

🤝 Feedback and Contributions

Feedback, suggestions, and contributions are welcome!

If you encounter an issue or have an idea for improving DocuMind, open a GitHub issue or submit a pull request.

📄 License

No license has been specified yet. Add a "LICENSE" file if you intend to grant others permission to reuse, modify, or distribute the code.

---

<p align="center">
  <strong>Built with Python, FAISS, Sentence Transformers, and Gemini.</strong>
  <br>
  <em>From documents to useful answers.</em>
</p>