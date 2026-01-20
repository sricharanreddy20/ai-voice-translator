from livekit.plugins.deepgram import STT
from livekit.plugins.elevenlabs import TTS
from livekit.plugins.groq import LLM
from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli, llm
from livekit import rtc
import os
import logging
import asyncio
import certifi
from dotenv import load_dotenv

load_dotenv()
os.environ["SSL_CERT_FILE"] = certifi.where()

REQUIRED_ENV_VARS = [
    "LIVEKIT_API_KEY",
    "LIVEKIT_API_SECRET",
    "LIVEKIT_URL",
    "DEEPGRAM_API_KEY",
    "GROQ_API_KEY",
    "ELEVENLABS_API_KEY"
]

missing_vars = [v for v in REQUIRED_ENV_VARS if not os.getenv(v)]
if missing_vars:
    raise RuntimeError(
        f"Missing required environment variables: {', '.join(missing_vars)}"
    )

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("polyglot")

async def wait_for_first_audio_track(room: rtc.Room):
    logger.info("Waiting for microphone track...")
    for p in room.remote_participants.values():
        for pub in p.track_publications.values():
            if pub.track and pub.kind == rtc.TrackKind.KIND_AUDIO:
                return pub.track

    loop = asyncio.get_event_loop()
    audio_track_future = loop.create_future()

    def on_track_subscribed(track, publication, participant):
        if track.kind == rtc.TrackKind.KIND_AUDIO:
            if not audio_track_future.done():
                audio_track_future.set_result(track)

    room.on("track_subscribed", on_track_subscribed)
    track = await audio_track_future
    room.off("track_subscribed", on_track_subscribed)
    return track

async def entrypoint(ctx: JobContext):
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
    logger.info(f"CONNECTED TO ROOM: {ctx.room.name}")

    logger.info("Waiting for user...")
    participant = await ctx.wait_for_participant()
    logger.info(f"User joined: {participant.identity}")

    track = await wait_for_first_audio_track(ctx.room)
    logger.info(f"Microphone detected! Track ID: {track.sid}")

    stt_plugin = STT(model="nova-2-general", language="hi")
    tts_plugin = TTS()
    llm_plugin = LLM(model="llama-3.3-70b-versatile")

    simple_chat_history = [
        {
            "role": "system",
            "text": (
                "You are a translator. "
                "If the text is in English, translate it to Hindi. "
                "If the text is in Hindi, translate it to English. "
                "Reply ONLY with the translation."
            )
        }
    ]

    agent_source = None
    agent_track = None

    async def speak(text: str):
        nonlocal agent_source, agent_track
        try:
            stream = tts_plugin.synthesize(text)
            async for event in stream:
                frame = event.frame if hasattr(event, "frame") else event
                if frame:
                    if agent_source is None:
                        agent_source = rtc.AudioSource(
                            frame.sample_rate,
                            frame.num_channels
                        )
                        agent_track = rtc.LocalAudioTrack.create_audio_track(
                            "agent_voice",
                            agent_source
                        )
                        await ctx.room.local_participant.publish_track(agent_track)

                    await agent_source.capture_frame(frame)

        except Exception as e:
            logger.exception(f"TTS error: {e}")

    await speak("System connected. I am listening.")

    stt_stream = stt_plugin.stream()
    audio_stream = rtc.AudioStream(track)

    async def push_loop():
        async for event in audio_stream:
            if event.frame:
                stt_stream.push_frame(event.frame)

    async def receive_loop():
        async for event in stt_stream:
            if event.type == "final_transcript":
                try:
                    text = event.alternatives[0].text
                except Exception:
                    continue

                if not text:
                    continue

                logger.info(f"HEARD: {text}")

                simple_chat_history.append({"role": "user", "text": text})

                messages = [
                    llm.ChatMessage(
                        role=msg["role"],
                        content=[msg["text"]]
                    )
                    for msg in simple_chat_history
                ]

                chat_ctx = llm.ChatContext(messages)
                response = llm_plugin.chat(chat_ctx=chat_ctx)

                trans = ""

                async for chunk in response:
                    content = ""

                    if hasattr(chunk, "delta") and hasattr(chunk.delta, "content"):
                        content = chunk.delta.content

                    elif hasattr(chunk, "choices") and len(chunk.choices) > 0:
                        content = chunk.choices[0].delta.content

                    elif hasattr(chunk, "content"):
                        content = chunk.content

                    if content:
                        trans += content

                logger.info(f"TRANSLATION: {trans}")

                if trans.strip():
                    simple_chat_history.append(
                        {"role": "assistant", "text": trans}
                    )
                    await speak(trans)
                else:
                    logger.warning("Received empty translation.")

    await asyncio.gather(push_loop(), receive_loop())

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))