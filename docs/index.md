Building LeagleDingle: An AI-Powered Legal Document AnalyzerLegal contracts, statutory frameworks, and court filings are notoriously dense and full of complex jargon. LeagleDingle is built to bridge the gap between heavy legal documentation and fast comprehension. By combining Streamlit's interface capabilities, pypdf extraction, and Google's Gemini models via the google-genai SDK, LeagleDingle ingests PDFs and delivers instant executive summaries, clause risk flagging, and natural language contract querying.System Architecture      ┌───────────────────┐      ┌─────────────────────────┐      ┌────────────────────────┐
│   User Browser    │ ───> │   Streamlit Cloud App   │ ───> │  pypdf Engine          │
│  (Document Upload)│      │   (app.py UI Runtime)   │      │  (Text Extraction)     │
└───────────────────┘      └─────────────────────────┘      └────────────────────────┘
                                        │                                │
                                        ▼                                ▼
                           ┌─────────────────────────┐      ┌────────────────────────┐
                           │   Prompt Orchestration  │ <─── │   Parsed Raw Text      │
                           └─────────────────────────┘      └────────────────────────┘
                                        │
                                        ▼
                           ┌─────────────────────────┐
                           │   google-genai SDK      │
                           └─────────────────────────┘
                                        │
                                        ▼
                           ┌─────────────────────────┐
                           │  Google Gemini Model    │
                           │  (Legal NLP Analysis)   │
                           └─────────────────────────┘
End-to-End Execution Flow
Document Ingestion: The user uploads a .pdf file via st.file_uploader().
Text Parsing: pypdf.PdfReader processes the file in-memory and extracts clean string representations across all pages.
Context Structuring: Extracted text combines with explicit system instruction prompts requiring context analysis, clause extraction, and risk level tagging.
Model Inference: The payload sends securely to the Gemini API using the google-genai client SDK.
Output Rendering: Streamlit parses the model's structured Markdown response, displaying executive summaries and actionable key takeaways directly to the user.

Core Capabilities
Automated Risk Assessment: Scans uploaded files to highlight potential liability, indemnity, or breach risks.
Plain-English Summarization: Translates complex legal terminology into clear, accessible terms.
Interactive Document Q&A: Allows users to query specific sections of their uploaded contracts on demand.
Deployment SetupTo host this update on GitHub Pages or reference it in your app repository, ensure your project's requirements.txt 

Links & ResourcesLive Web App: [LeagleDingle on Streamlit Cloud](https://suvegkali-legaldingle-app-vsknuz.streamlit.app/)
Source Code: https://github.com/SuvegKali/LegalDingle
