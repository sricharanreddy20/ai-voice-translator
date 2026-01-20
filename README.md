# AI Voice Translator

A real-time, multilingual voice translation agent built with LiveKit Agents. This project creates a conversational AI capable of translating speech between English and Hindi/Telugu with ultra-low latency.

## Tech Stack

This project leverages the fastest available models for a seamless conversational experience:

* Framework: LiveKit Agents
* Speech-to-Text (STT): Deepgram (Nova-2 model)
* Translation Engine (LLM): Groq (Llama 3-70b/8b)
* Text-to-Speech (TTS): ElevenLabs (Multilingual v2)

## Features

* Real-time Processing: Streaming audio pipeline for near-instant translation.
* Bi-directional Translation: Automatically detects language and translates:
    * English to Hindi/Telugu
    * Hindi/Telugu to English
* Dockerized: Ready for deployment using Docker.
* Context Aware: The LLM is system-prompted strictly as a translator, not a chatbot.

## Prerequisites

* Python 3.11+
* Docker (optional, for containerized deployment)
* A LiveKit Cloud project (WebSocket URL, API Key, Secret)
* API Keys for:
    * Deepgram
    * Groq
    * ElevenLabs

## Configuration

1. Clone the repository:
   git clone https://github.com/yourusername/voice-translator.git
   cd voice-translator

2. Create a .env file in the root directory and add your keys:
   LIVEKIT_URL=wss://your-project.livekit.cloud
   LIVEKIT_API_KEY=your_api_key
   LIVEKIT_API_SECRET=your_api_secret
   DEEPGRAM_API_KEY=your_deepgram_key
   ELEVENLABS_API_KEY=your_elevenlabs_key
   GROQ_API_KEY=your_groq_key

## Local Development

1. Create a virtual environment:
   python -m venv venv
   source venv/bin/activate  # On Windows use venv\Scripts\activate

2. Install dependencies:
   pip install -r requirements.txt

3. Run the agent in development mode:
   python polyglot.py dev

## Docker Deployment

To build and run the agent as a container:

1. Build the image:
   docker build -t voice-translator .

2. Run the container:
   docker run --env-file .env voice-translator

## How to Test

Since this is a backend agent, you need a frontend client to connect to the LiveKit room and send audio.

1. Run the agent locally (python polyglot.py dev).
2. Open the LiveKit Agents Playground (https://agents-playground.livekit.io/).
3. Enter your LIVEKIT_URL, API_KEY, and SECRET (the same ones used in your .env).
4. Connect to the room. The agent should join automatically and greet you.
5. Speak in English, and it will respond in Hindi (or vice versa).

## License

MIT
