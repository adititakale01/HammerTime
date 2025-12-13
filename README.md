# HammerTime

TUM.ai X Anthropic - Procurement Assistant

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
