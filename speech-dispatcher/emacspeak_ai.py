#!/usr/bin/env python3

"""emacspeak_ai - OpenAPI-compatible adapter for Emacspeak

Implements the Emacspeak protocol.

Dependencies: pip install pyaudio openai
"""

import sys
import re
import threading
import time
import pyaudio
import os
import logging
import signal
from openai import OpenAI
import subprocess

THRESHOLD_LEN = 20
BACKUP = "espeak"

queue = []

def parse_config(path):
    config = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            key, _, value = line.partition(' ')
            value = re.sub(r'\s*#.*$', '', value).strip().strip('"')
            config[key] = value
    return config

client = None
audio_thread = None
stream = None
config = {}
stop_event = threading.Event()

voice = None
model = None
language = None

def speak(text):
    """Synthesize text and play it."""
    logging.info(f"Sending {text}")
    stop_event.clear()
    with client.audio.speech.with_streaming_response.create(
            model=model,
            voice=voice,
            input=text,
            response_format="pcm"
    ) as response:
        logging.info("Receiving audio")
        for chunk in response.iter_bytes(1024):
            stream.write(chunk)
            if stop_event.is_set():
                break

def start_speech_thread(s):
    global audio_thread
    if len(s) > THRESHOLD_LEN:
        audio_thread = threading.Thread(target=speak, args=(s,))
        audio_thread.start()
    else:
        subprocess.Popen([BACKUP, s])

def cmd_dispatch():
    global audio_thread, queue
    start_speech_thread("\n".join(queue))
    queue = []

def write(line):
    sys.stdout.write(line + "\n")
    sys.stdout.flush()
    logging.info(f"out {line}")

def choose_voice():
    global voice, language, model
    if model == "supertonic-3":
        voice = config.get("DefaultVoice")
        return
    elif model == "kokoro":
        if language == "fr":  # Hardcode for now
            voice = "ff_siwis"
        elif language == "en":
            voice = 'af_bella'

def play(media_file):
    proc = subprocess.Popen(
        ["ffmpeg", "-i", media_file, "-f", "s16le", "-ar", "24000", "-ac", "1", "-"],
        stdout=subprocess.PIPE, stderr=subprocess.DEVNULL
    )
    while True:
        chunk = proc.stdout.read(1024)
        if not chunk:
            break
        stream.write(chunk)
        if stop_event.is_set():
            proc.terminate()
            break

def cmd_play(media_file):
    media_file = media_file.strip().strip('{}')
    stop_event.clear()
    global audio_thread
    audio_thread = threading.Thread(target=play, args=(media_file,))
    audio_thread.start()


def get_arg(line):
    return line[2:].strip().strip('{}')

def main():
    global client, config, voice, model, logging, stream, language
    log_path = os.path.join(os.environ.get("TMPDIR", "/tmp"), "emacspeak_ai.log")
    logging.basicConfig(
        filename=log_path,
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )

    config = parse_config(sys.argv[1]) if len(sys.argv) > 1 else {}
    logging.warning(f'Config {config} {sys.argv}')
    voice = config.get("AIDefaultVoice", os.environ.get("DTK_AI_VOICE"))
    model = config.get("AIDefaultModel", os.environ.get("DTK_AI_MODEL"))
    client = OpenAI(base_url=config.get("AIBaseURL"),
                    api_key=config.get("AIKey"))
    audio = pyaudio.PyAudio()
    stream = audio.open(format=8,
                        channels=1,
                        rate=24_000,
                        frames_per_buffer=1024,
                        output=True)

    while True:
        line = sys.stdin.readline().rstrip("\n")
        logging.info(f"line {line}")
        if line.startswith('q'):
            queue.append(get_arg(line))
        elif line.startswith('d'):
            cmd_dispatch()
        elif line == 's':
            stop_event.set()
        elif line.startswith('l'):  # Letter/character; fall back to espeak
            stop_event.set()
            subprocess.Popen(["espeak", line[2:].strip().strip('{}')])
        elif line.startswith('version'):
            start_speech_thread('emacspeak ai 0.1')
        elif line.startswith('tts_say'):
            start_speech_thread(get_arg(line))
        elif line.startswith('set_lang'):
            args = line[2:].strip('"').split(':')
            language = args[0]
            choose_voice()
            if len(args) > 1:
                voice = args[1]
        elif line.startswith('p'):
            cmd_play(line[2:])
        elif line == "":
            break
        # Still need to implement



    if audio_thread:
        audio_thread.join()

if __name__ == "__main__":
    main()
