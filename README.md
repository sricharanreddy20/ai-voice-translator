# AI Voice Translator

Real-time multilingual voice translator using LiveKit Agents.

## Features
- Speech-to-text: Deepgram  
- Translation: Groq LLM  
- Text-to-speech: ElevenLabs  
- Supports English ↔ Hindi/Telugu  
- Dockerized for easy deployment  

---

## Prerequisites
- Python 3.11+  
- Docker (optional, for containerized run)  
- LiveKit Cloud account  
- API keys for:
  - Deepgram  
  - ElevenLabs  
  - Groq  

---

## Environment Variables

Create a `.env` file in the project root with:

LIVEKIT_URL=wss://your-livekit-url
LIVEKIT_API_KEY=your_livekit_key
LIVEKIT_API_SECRET=your_livekit_secret
DEEPGRAM_API_KEY=your_deepgram_key
ELEVENLABS_API_KEY=your_elevenlabs_key
GROQ_API_KEY=your_groq_key


---

## Setup (Local)

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python polyglot.py dev

docker build -t voice-translator .
docker run --env-file .env voice-translator




