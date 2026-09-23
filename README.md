# AI Voice Translator

A real-time English ↔ Hindi voice translation agent built with LiveKit Agents. Speak in Hindi and hear English, or speak in English and hear Hindi, in a live voice session.

This is a prototype exploring the core pipeline for a multilingual voice translator.

## How It Works

```
Microphone → LiveKit (WebRTC) → Deepgram STT → Groq LLM (translation) → ElevenLabs TTS → Speaker
```

1. The agent joins a LiveKit room and subscribes to the user's microphone track.
2. Audio frames are streamed to Deepgram Nova-2 for speech-to-text.
3. Each final transcript is sent to Llama 3.3 70B on Groq, prompted strictly as a translator. The model infers the translation direction from the input language.
4. The translation is synthesized with ElevenLabs and streamed back into the room as audio.

Audio intake and transcript processing run as concurrent asyncio loops.

## Tech Stack

- **Framework:** LiveKit Agents (Python)
- **Speech-to-Text:** Deepgram Nova-2
- **Translation:** Llama 3.3 70B via Groq
- **Text-to-Speech:** ElevenLabs
- **Deployment:** Docker

## Prerequisites

- Python 3.11+
- Docker (optional)
- A LiveKit Cloud project (URL, API key, API secret)
- API keys for Deepgram, Groq, and ElevenLabs

## Setup

1. Clone the repository:
```bash
   git clone https://github.com/sricharanreddy20/ai-voice-translator.git
   cd ai-voice-translator
```

2. Copy `.env.example` to `.env` and fill in your keys:
```bash
   cp .env.example .env
```

3. Create a virtual environment and install dependencies:
```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   pip install -r requirements.txt
```

4. Run the agent:
```bash
   python polyglot.py dev
```

## Run with Docker

```bash
docker build -t voice-translator .
docker run --env-file .env voice-translator
```

## Testing

1. Start the agent.
2. Open the [LiveKit Agents Playground](https://agents-playground.livekit.io/).
3. Connect using the same LiveKit URL, API key, and secret from your `.env`.
4. The agent joins and greets you. Speak in Hindi or English to hear the translation.

## Limitations and Next Steps

- Supports English and Hindi only; the speech-to-text model is configured for Hindi.
- The LLM response is fully generated before speech synthesis begins. Streaming it to TTS sentence by sentence would reduce response time.
- Planned: explicit language detection and a multilingual STT model to support more languages, such as Telugu.

## License

MIT
