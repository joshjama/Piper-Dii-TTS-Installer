#!/usr/bin/env python3
"""Speech Dispatcher module for OpenAI-compatible TTS returning WAV audio."""

## File: speechd_ai.py
## Purpose: Connect Speech Dispatcher to an OpenAI-compatible TTS endpoint.
## Input: Speech Dispatcher commands, module configuration, and WAV responses.
## Output: Protocol responses on standard output and audio through PyAudio.
## Active path: speak() requests API speed 0.8; SoX adjusts playback speed.
## Privacy: Do not record spoken text or real API keys in the log.
## Import io: Python standard library; no separate installation.
## Import logging: Python standard library; no separate installation.
## Import os: Python standard library; no separate installation.
## Import re: Python standard library; no separate installation.
## Import signal: Python standard library; no separate installation.
## Import subprocess: Python standard library; no separate installation.
## Import sys: Python standard library; no separate installation.
## Import threading: Python standard library; no separate installation.
## Import wave: Python standard library; no separate installation.
## Import decimal: Python standard library; no separate installation.
## Import pyaudio: Install the PyAudio package in the module's Python environment.
## Import openai: Install the openai package in the module's Python environment.
## External program sox: Install the system package sox; it is not a Python import.
## External program espeak: Required only when the backup function is used.
## External program ffmpeg: Required only if the unused legacy path is called.
# def parse_config(path):
## Purpose: Read key-value settings from a module configuration file.
## Input: path is the path to the configuration file.
## Output: A dictionary mapping setting names to string values.
## Side effects: Reads the configuration file.
## Errors: File access and decoding errors propagate to the caller.
# def write(line):
## Purpose: Send one protocol response line to Speech Dispatcher.
## Input: line is a response without its final newline character.
## Output: None.
## Side effects: Writes to standard output and records the line in the log.
# def reset_events():
## Purpose: Clear the stop, pause, and resume events.
## Input: No arguments; uses the shared event objects.
## Output: None.
## Side effects: Changes shared event state.
# def strip_ssml(text):
## Purpose: Replace markup tags with spaces before synthesis.
## Input: text is a string that may contain SSML-style tags.
## Output: A string with matching tags replaced by spaces.
## Limitation: This regular expression is not a complete SSML parser.
# def play_wav(data):
## Purpose: Play a WAV response without changing its speed.
## Input: data is a complete WAV file as bytes.
## Output: None; samples are sent to the audio output device.
## Side effects: Opens, writes to, and closes a PyAudio output stream.
## Errors: Rejects compressed WAV data; audio-device errors may propagate.
# def safe_speed(value):
## Purpose: Round and clamp a speed value to the supported range.
## Input: value is convertible to a finite Decimal number.
## Output: A Decimal value between SPEED_MIN and SPEED_MAX.
## Errors: Rejects invalid or non-finite values.
# def speed_from_rate(value):
## Purpose: Convert a Speech Dispatcher rate to a playback speed.
## Input: value is a rate convertible to a finite Decimal number.
## Output: A floating-point speed based on DefaultSpeed and speed limits.
## Errors: Rejects invalid or non-finite rate values.
# def adjust_wav_tempo_old(data, target_speed):
## Purpose: Adjust a complete WAV file using the legacy FFmpeg path.
## Input: data is WAV bytes; target_speed is the requested speed.
## Output: Adjusted WAV bytes, or the original bytes if no change is needed.
## Side effects: May start an FFmpeg process.
## Errors: Unsupported WAV formats and FFmpeg failures may raise exceptions.
## Usage: The currently selected speak() path does not call this function.
# def play_wav_with_tempo(data, target_speed):
## Purpose: Play WAV audio at the requested speed using SoX when needed.
## Input: data is a complete WAV file; target_speed is the requested speed.
## Output: None; resulting audio is sent to the output device.
## Side effects: May start SoX, feed it WAV bytes, and play its PCM output.
## Errors: Unsupported WAV data, SoX failures, and audio failures may raise exceptions.
#     def feed_ffmpeg():
## Purpose: Feed WAV bytes to the SoX process in play_wav_with_tempo().
## Input: Uses data, process, and stop_event from the enclosing function.
## Output: None.
## Side effects: Writes WAV bytes to the process pipe and closes its input.
## Placement: Put this comment before the nested function, inside play_wav_with_tempo().
## Naming: The function name still mentions FFmpeg, but the active process is SoX.
# def speak(text):
## Purpose: Request speech at API speed 0.8 and adjust playback speed locally.
## Input: text is speech content received from Speech Dispatcher.
## Output: None; audio is played and a protocol END event is sent.
## Side effects: Calls the TTS endpoint and play_wav_with_tempo().
## Errors: Exceptions are logged instead of propagated.
## Note: The current implementation sends END even after a logged failure.
# def speak_api_speed(text):
## Purpose: Request speech using the TTS API's speed parameter.
## Input: text is speech content received from Speech Dispatcher.
## Output: None; audio is played and a protocol END event is sent.
## Side effects: Calls the TTS endpoint and play_wav().
## Errors: Exceptions are logged instead of propagated.
## Usage: The current cmd_speak() implementation does not select this function.
# def speak_full_ffmpeg_wait(text):
## Purpose: Use the legacy whole-file tempo-adjustment playback path.
## Input: text is speech content received from Speech Dispatcher.
## Output: None; playback is attempted and an END event is sent.
## Side effects: Calls the TTS endpoint and attempts audio processing.
## Errors: Processing errors and other exceptions are logged.
## Usage: The current cmd_speak() implementation does not select this function.
## Known mismatch: It calls adjust_wav_tempo(), but the posted file defines
## adjust_wav_tempo_old(); these names do not match.
# def use_backup(text):
## Purpose: Synthesize text with the configured backup program.
## Input: text is the text to synthesize.
## Output: None; WAV audio is played and an END event is sent.
## Side effects: Starts the backup program and calls play_wav().
## Errors: Backup-process and playback exceptions are logged.
## Usage: The current cmd_speak() implementation does not select this function.
# def read_body():
## Purpose: Read a dot-terminated Speech Dispatcher command body.
## Input: Protocol lines from standard input until "." or end of file.
## Output: The received lines joined into one string.
## Side effects: Consumes lines from standard input.
# def cmd_speak(message_type=None):
## Purpose: Acknowledge a speech command and start a worker thread.
## Input: message_type optionally identifies a special message type;
## the command body is read from standard input.
## Output: None; protocol acknowledgements are sent to Speech Dispatcher.
## Side effects: Resets shared events and starts speak() in a new thread.
# def choose_voice():
## Purpose: Select a voice for the current model and language.
## Input: Uses the current model, language, voice, and configuration.
## Output: None.
## Side effects: May update the global voice value.
# def cmd_set():
## Purpose: Read and apply Speech Dispatcher settings.
## Input: A settings body read from standard input.
## Output: None; protocol acknowledgements are sent to Speech Dispatcher.
## Side effects: May update voice, language, model, speed, and threshold.
## Errors: Invalid rates are logged and ignored; other invalid settings
## may still raise an exception in the posted implementation.
# def cmd_audio():
## Purpose: Accept audio settings and initialize PyAudio if necessary.
## Input: An audio-settings body read from standard input.
## Output: None; protocol acknowledgements are sent to Speech Dispatcher.
## Side effects: May create the global PyAudio interface.
## Errors: Audio-initialization errors may propagate.
# def cmd_loglevel():
## Purpose: Acknowledge a Speech Dispatcher log-level command.
## Input: A command body read from standard input.
## Output: None; protocol acknowledgements are sent to Speech Dispatcher.
## Side effects: Consumes the command body.
## Note: The posted implementation does not change Python's logging level.
# def main():
## Purpose: Initialize the module and handle Speech Dispatcher commands.
## Input: An optional configuration path from the command line and
## protocol commands from standard input.
## Output: Protocol responses on standard output; no return value.
## Side effects: Initializes logging and the API client, handles commands,
## waits for the last worker, and releases audio resources.
## Errors: Exits if the first protocol command is not INIT.

import io
import logging
import os
import re
import signal
import subprocess
import sys
import threading
import wave

import pyaudio
from openai import OpenAI
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

#THRESHOLD_LEN = 40
THRESHOLD_LEN = 0
BACKUP = "espeak"
speed = 1.0


def parse_config(path):
    config = {}
    with open(path, encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            key, _, value = line.partition(" ")
            config[key] = re.sub(r"\s*#.*$", "", value).strip().strip('"')
    return config


client = None
audio = None
audio_thread = None
stream = None
config = {}
stop_event = threading.Event()
pause_event = threading.Event()
resume_event = threading.Event()
voice = None
model = None
language = "en"
message_count = 0
write_lock = threading.Lock()


def write(line):
    with write_lock:
        sys.stdout.write(line + "\n")
        sys.stdout.flush()
    logging.info("out %s", line)


def reset_events():
    stop_event.clear()
    pause_event.clear()
    resume_event.clear()


def strip_ssml(text):
    return re.sub(r"<[^>]+>", " ", text)


def play_wav(data):
    global stream
    if audio is None:
        raise RuntimeError("AUDIO wurde noch nicht initialisiert")
    with wave.open(io.BytesIO(data), "rb") as wav:
        if wav.getcomptype() != "NONE":
            raise ValueError("Komprimiertes WAV wird nicht unterstuetzt")
        sample_format = audio.get_format_from_width(wav.getsampwidth())
        if stream is not None:
            stream.stop_stream()
            stream.close()
            stream = None
        stream = audio.open(
            format=sample_format,
            channels=wav.getnchannels(),
            rate=wav.getframerate(),
            frames_per_buffer=1024,
            output=True,
        )
        while not stop_event.is_set():
            chunk = wav.readframes(1024)
            if not chunk:
                break
            stream.write(chunk)
        stream.stop_stream()
        stream.close()
        stream = None

SPEED_MIN = Decimal("0.8")
SPEED_MAX = Decimal("1.4")
SPEED_STEP = Decimal("0.1")


def safe_speed(value):
    number = Decimal(str(value))
    if not number.is_finite():
        raise ValueError("Geschwindigkeit muss eine endliche Zahl sein")

    number = number.quantize(SPEED_STEP, rounding=ROUND_HALF_UP)
    return min(SPEED_MAX, max(SPEED_MIN, number))


def speed_from_rate(value):
    rate = Decimal(str(value))
    if not rate.is_finite():
        raise ValueError("Sprechrate muss eine endliche Zahl sein")

    rate = min(Decimal("100"), max(Decimal("-100"), rate))
    default = safe_speed(config.get("DefaultSpeed", "1.0"))

    if rate < 0:
        calculated = default + (default - SPEED_MIN) * rate / Decimal("100")
    else:
        calculated = default + (SPEED_MAX - default) * rate / Decimal("100")

    return float(safe_speed(calculated))

def adjust_wav_tempo_old(data, target_speed):
    tempo = target_speed / 0.8
    if abs(tempo - 1.0) < 0.000001:
        return data

    with wave.open(io.BytesIO(data), "rb") as wav:
        codecs = {
            1: "pcm_u8",
            2: "pcm_s16le",
            3: "pcm_s24le",
            4: "pcm_s32le",
        }
        codec = codecs.get(wav.getsampwidth())
        if wav.getcomptype() != "NONE" or codec is None:
            raise ValueError("Nicht unterstuetztes WAV-Sampleformat")

    result = subprocess.run(
        [
            "ffmpeg",
            "-hide_banner",
            "-loglevel", "error",
            "-nostdin",
            "-i", "pipe:0",
            "-af", f"atempo={tempo:.6f}",
            "-c:a", codec,
            "-f", "wav",
            "pipe:1",
        ],
        input=data,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
        timeout=30,
    )
    return result.stdout

def play_wav_with_tempo(data, target_speed):
    global stream

    tempo = target_speed / 0.8
    if abs(tempo - 1.0) < 0.000001:
        play_wav(data)
        return

    if audio is None:
        raise RuntimeError("AUDIO wurde noch nicht initialisiert")

    with wave.open(io.BytesIO(data), "rb") as wav:
        if wav.getcomptype() != "NONE":
            raise ValueError("Komprimiertes WAV wird nicht unterstuetzt")

        sample_width = wav.getsampwidth()
        channels = wav.getnchannels()
        sample_rate = wav.getframerate()

    raw_formats = {
        1: ("u8", "pcm_u8"),
        2: ("s16le", "pcm_s16le"),
        3: ("s24le", "pcm_s24le"),
        4: ("s32le", "pcm_s32le"),
    }
    if sample_width not in raw_formats:
        raise ValueError("Nicht unterstuetzte WAV-Samplebreite")

    raw_format, codec = raw_formats[sample_width]
    frame_bytes = sample_width * channels

    encoding = "unsigned-integer" if sample_width == 1 else "signed-integer"

    command = [
        "sox",
        "-q",
        "-t", "wav", "-",
        "-t", "raw",
        "-e", encoding,
        "-b", str(sample_width * 8),
        "-L",
        "-c", str(channels),
        "-r", str(sample_rate),
        "-",
        "tempo", "-s", f"{tempo:.6f}",
    ]

    #if abs(gain - 1.0) >= 0.000001:
    #   command.extend(["vol", f"{gain:.3f}"])

    process = subprocess.Popen(
        command,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=sys.stderr,
        bufsize=0,
    )

    def feed_ffmpeg():
        try:
            for offset in range(0, len(data), 65536):
                if stop_event.is_set():
                    break
                process.stdin.write(data[offset:offset + 65536])
        except (BrokenPipeError, OSError):
            pass
        finally:
            try:
                process.stdin.close()
            except OSError:
                pass

    feeder = threading.Thread(target=feed_ffmpeg, daemon=True)
    feeder.start()

    playback_stream = None
    received_audio = False

    try:
        playback_stream = audio.open(
            format=audio.get_format_from_width(sample_width),
            channels=channels,
            rate=sample_rate,
            frames_per_buffer=1024,
            output=True,
        )
        stream = playback_stream

        while not stop_event.is_set():
            chunk = process.stdout.read(1024 * frame_bytes)
            if not chunk:
                break
            received_audio = True
            playback_stream.write(chunk)

        if not stop_event.is_set():
            feeder.join()
            returncode = process.wait()
            if returncode != 0 or not received_audio:
                raise RuntimeError(
                    f"FFmpeg lieferte keine gueltige Audioausgabe "
                    f"(Exit-Status {returncode})"
                )
    finally:
        if process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()

        feeder.join(timeout=2)

        if process.stdout is not None:
            process.stdout.close()

        if playback_stream is not None:
            try:
                playback_stream.stop_stream()
            finally:
                playback_stream.close()

        if stream is playback_stream:
            stream = None


def speak(text):
    try:
        text = strip_ssml(text)
        target_speed = speed
        logging.info(
            "model %s voice %s proxy_speed 0.8 playback_target %.1f",
            model, voice, target_speed
        )

        with client.audio.speech.with_streaming_response.create(
            model=model,
            voice=voice,
            input=text,
            response_format="wav",
            speed=0.8,
        ) as response:
            data = response.read()

        if not stop_event.is_set():
            play_wav_with_tempo(data, target_speed)

    except Exception:
        logging.exception("TTS oder WAV-Wiedergabe fehlgeschlagen")
    finally:
        write("702 END")

def speak_api_speed(text):
    try:
        text = strip_ssml(text)
        logging.info(
            "model %s voice %s proxy_speed 0.8 playback_target %.1f",
            model, voice, target_speed
        )
        with client.audio.speech.with_streaming_response.create(
            model=model,
            voice=voice,
            input=text,
            response_format="wav",
            speed=speed,
        ) as response:
            data = response.read()
        if not stop_event.is_set():
            play_wav(data)
    except Exception:
        logging.exception("TTS oder WAV-Wiedergabe fehlgeschlagen")
    finally:
        write("702 END")

def speak_full_ffmpeg_wait(text):
    try:
        text = strip_ssml(text)
        target_speed = speed

        logging.info(
            "model %s voice %s proxy_speed 0.8 playback_target %.1f",
            model, voice, target_speed
        )

        with client.audio.speech.with_streaming_response.create(
            model=model,
            voice=voice,
            input=text,
            response_format="wav",
            speed=0.8,
        ) as response:
            data = response.read()

        if stop_event.is_set():
            return

        try:
            data = adjust_wav_tempo(data, target_speed)
        except (OSError, ValueError, subprocess.SubprocessError):
            logging.exception(
                "WAV-Tempobearbeitung fehlgeschlagen; spiele Original mit speed 0.8"
            )

        if not stop_event.is_set():
            play_wav(data)
    except Exception:
        logging.exception("TTS oder WAV-Wiedergabe fehlgeschlagen")
    finally:
        write("702 END")


def use_backup(text):
    try:
        proc = subprocess.Popen(
            [BACKUP, text, "--stdout"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        data, error = proc.communicate()
        if proc.returncode != 0:
            raise RuntimeError(error.decode(errors="replace"))
        if not stop_event.is_set():
            play_wav(data)
    except Exception:
        logging.exception("Backup-TTS fehlgeschlagen")
    finally:
        write("702 END")


def read_body():
    lines = []
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        line = line.rstrip("\n")
        if line == ".":
            break
        if line.startswith(".."):
            line = line[1:]
        lines.append(line)
    return "\n".join(lines)


def cmd_speak(message_type=None):
    global message_count, audio_thread
    write("202 OK SEND DATA")
    text = strip_ssml(read_body())
    if message_type is None:
        message_count += 1
    write("200 OK SPEAKING")
    write("701 BEGIN")
    reset_events()
    #target = use_backup if len(text) < THRESHOLD_LEN else speak
    target = speak
    audio_thread = threading.Thread(target=target, args=(text,))
    audio_thread.start()


def choose_voice():
    global voice

    if model == "supertonic-3":
        voice = config.get("DefaultVoice")
        return
    elif model == "piper":
        voice = config.get("DefaultVoice")
        return
    elif model == "kokoro":
        if language == "fr":
            voice = "ff_siwis"
        elif language == "en":
            if voice == "male1":
                voice = "am_fenrir"
            elif voice == "female1":
                voice = "af_bella"


def cmd_set():
    global voice, language, model, THRESHOLD_LEN, speed
    write("203 OK RECEIVING SETTINGS")
    for line in read_body().split("\n"):
        key, separator, value = line.partition("=")
        if not separator:
            continue
        if key == "voice":
            voice = value
        elif key == "language":
            language = value
        elif key == "model":
            model = value
        elif key == "rate":
            try:
                speed = speed_from_rate(value)
            except (InvalidOperation, ValueError):
                logging.warning("Ungueltiger rate-Wert: %r", value)
        elif key == "threshold":
            THRESHOLD_LEN = int(value)
    choose_voice()
    write("203 OK SETTINGS RECEIVED")


def cmd_audio():
    global audio
    write("207 OK RECEIVING AUDIO SETTINGS")
    read_body()
    if audio is None:
        audio = pyaudio.PyAudio()
    write("203 OK AUDIO INITIALIZED")


def cmd_loglevel():
    write("207 OK RECEIVING LOGLEVEL SETTINGS")
    read_body()
    write("203 OK LOGLEVEL SET")


def main():
    global client, config, voice, model, language, speed
    speed = speed_from_rate(0)
    log_path = os.path.join(os.environ.get("TMPDIR", "/tmp"), "speechd_ai.log")
    logging.basicConfig(
        filename=log_path,
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    config = parse_config(sys.argv[1]) if len(sys.argv) > 1 else {}
    voice = config.get("DefaultVoice")
    model = config.get("AIDefaultModel")
    language = config.get("Language", "en")
    client = OpenAI(
        base_url=config.get("AIBaseURL"),
        api_key=config.get("AIKey") or os.environ.get("OPENAI_API_KEY"),
    )
    line = sys.stdin.readline().rstrip("\n")
    if not line.startswith("INIT"):
        sys.stderr.write(f"Expected INIT, got {line!r}\n")
        sys.exit(3)
    write("299-AI initialized.")
    write("299 OK LOADED SUCCESSFULLY")
    choose_voice()
    while True:
        line = sys.stdin.readline().rstrip("\n")
        if line.startswith("SPEAK"):
            cmd_speak()
        elif line.startswith("SOUND_ICON"):
            cmd_speak("SOUND_ICON")
        elif line.startswith("CHAR"):
            cmd_speak("CHAR")
        elif line.startswith("KEY"):
            cmd_speak("KEY")
        elif line.startswith("STOP"):
            stop_event.set()
        elif line.startswith("PAUSE"):
            pause_event.set()
            write("703 EVENT PAUSE")
        elif line.startswith("LIST VOICES"):
            write("304 CANT LIST VOICES")
        elif line.startswith("SET"):
            cmd_set()
        elif line.startswith("AUDIO"):
            cmd_audio()
        elif line.startswith("LOGLEVEL"):
            cmd_loglevel()
        elif line.startswith("QUIT"):
            write("210 OK QUIT")
            break
        elif line.startswith("CANCEL"):
            stop_event.set()
            write("703 EVENT CANCEL")
        elif line.startswith("RESUME"):
            resume_event.set()
            write("703 EVENT PAUSE")
        elif not line:
            break
        else:
            logging.warning("Unknown command: %r", line)
            write("300 ERR UNKNOWN COMMAND")
    if audio_thread:
        audio_thread.join()
    if stream is not None:
        stream.close()
    if audio is not None:
        audio.terminate()


if __name__ == "__main__":
    main()
