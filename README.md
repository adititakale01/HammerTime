# HammerTime

TUM.ai X Anthropic - Procurement Assistant

An Agentic Procurement Assistant for Construction: HammerTime

This is our submission for the TUM.ai x Anthropic Hackathon with comstruct: HammerTime. We tackled the "C-Materials Challenge", simplifying the messy, overlooked tail-spend of construction procurement (screws, gloves, drill bits) for non-digital native foremen.
Instead of forcing construction workers to navigate complex ERPs, we built a multi-modal AI agent that translates "site talk" into structured orders.

🚀 The Tech Stack & Architecture
We built a decoupled architecture designed for speed and reliability:

🔹 The Brain: Agentic AI with Anthropic Claude 3.5 Sonnet
We didn't just wrap a chatbot. We built a logic-driven agent (request_agent.py) that handles the procurement lifecycle:
- Intent Recognition: Cleans raw voice transcripts to remove filler words ("um," "uh") using a specialized prompt chain.
- Structured Extraction: Forces Claude to output strict JSON mapped to our normalized product model ([ID, Quantity]) rather than conversational fluff.
- Fuzzy Logic Layer: Since LLMs can hallucinate SKUs, we implemented a Python validation layer using difflib to fuzzy-match AI outputs against our sample.csv catalog, ensuring real-time inventory and price checks.

🔹 Multi-Modal Inputs (Vision & Voice)
- Voice-First UX: Integrated PyAudio and Google Speech Recognition for hands-free ordering.
- Computer Vision: Users can snap a photo of a handwritten scribbled note or a pile of parts. The backend (image_processing.py) uses Claude’s vision capabilities to transcribe handwriting or identify parts and immediately build a cart.

🔹 Backend: FastAPI & Business Logic
- API-First: Built on FastAPI to serve the agent logic, image analysis, and PDF generation asynchronously.
- Approval Workflows: Implemented real-world business rules. Orders >€100 trigger an "Admin Approval" state, requiring a password override (simulating a procurement manager review).
- Contract Generation: Uses ReportLab to programmatically generate standard PDF Supply Contracts (pdf_generator.py) instantly upon approval.

🔹 Frontend: Streamlit
We used Streamlit for a responsive, mobile-first dashboard that manages session state (st.session_state) for cart persistence and chat history, creating a seamless WhatsApp-like experience for the user.

💡 Why it matters
We took unstructured data (a foreman yelling "I need drywall screws!") and gave structured ERP data (Contract creation, SKU mapping, and Inventory checks) without changing how the worker operates.

## Prerequisites

### System Dependencies (Ubuntu/Debian)

```bash
# For voice input (PyAudio)
sudo apt-get install -y portaudio19-dev

# For audio processing (optional)
sudo apt-get install -y ffmpeg
```

### Python Dependencies

```bash
pip install -e .
```

Or install manually:
```bash
pip install SpeechRecognition PyAudio
```

## Getting Started

1. **Add API Key** - Create `secrets.yaml` in the project root:
   ```yaml
   API_KEY: "your-anthropic-api-key"
   ```

2. **Install Dependencies**:
   ```bash
   pip install -e .
   ```

3. **Run Backend**:
   ```bash
   python backend/main.py
   ```

4. **Run Frontend** (in a new terminal):
   ```bash
   streamlit run Frontend/app.py
   ```

## Project Structure

```
HammerTime/
├── backend/
│   ├── main.py              # FastAPI backend
│   └── utils/
│       ├── request_agent.py # AI agent logic
│       └── image_processing.py
├── Frontend/
│   ├── app.py               # Main entry point
│   ├── styles.py            # CSS styling
│   ├── config.py            # Configuration & session state
│   ├── utils.py             # Helper functions
│   ├── components.py        # Reusable UI components
│   └── views/               # Page views
│       ├── dashboard.py
│       ├── voice_request.py
│       ├── image_search.py
│       ├── orders.py
│       └── reports.py
├── secrets.yaml             # API keys (not in git)
└── pyproject.toml           # Dependencies
```

## Troubleshooting

### "Could not find PyAudio" Error
```bash
sudo apt-get install -y portaudio19-dev
pip install pyaudio
```

### "No module named 'speech_recognition'" Error
```bash
pip install SpeechRecognition
```

---
Hackathon Demo v2.0
