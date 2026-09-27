#!/usr/bin/env bash
set -Eeuo pipefail

# Installation und Server bleiben im Verzeichnis, aus dem dieses Skript
# aufgerufen wird. Kein sudo und keine Änderungen an Speech Dispatcher.
BASE_DIR="$(pwd -P)"
VENV="$BASE_DIR/.venv"
MODEL_DIR="$BASE_DIR/models"
MODEL="$MODEL_DIR/de_DE-dii-high.onnx"
CONFIG="$MODEL.json"
SERVER="$BASE_DIR/piper_openai_server.py"
REPO="https://huggingface.co/csukuangfj/vits-piper-de_DE-dii-high/resolve/main"

error() {
    printf 'FEHLER: %s\n' "$*" >&2
    exit 1
}

trap 'printf "FEHLER in Zeile %s: %s\n" "$LINENO" "$BASH_COMMAND" >&2' ERR

command -v python3 >/dev/null 2>&1 ||
    error "python3 fehlt."

command -v curl >/dev/null 2>&1 ||
    error "curl fehlt."

if [[ ! -e "$VENV" ]]; then
    printf 'Erstelle Python-Umgebung: %s\n' "$VENV"
    python3 -m venv "$VENV" ||
        error "venv konnte nicht erstellt werden. Unter Debian/Mint ggf. python3-venv installieren."
elif [[ ! -x "$VENV/bin/python" ]]; then
    error "$VENV existiert, ist aber keine nutzbare Python-Umgebung. Ich überschreibe sie nicht."
fi

PYTHON="$VENV/bin/python"

# Bereits vorhandene, funktionsfähige Pakete werden nicht erneut installiert.
if ! "$PYTHON" -c \
    'import piper, fastapi, uvicorn, imageio_ffmpeg' \
    >/dev/null 2>&1; then
    printf 'Installiere fehlende Abhängigkeiten in %s\n' "$VENV"
    "$PYTHON" -m pip install \
        'piper-tts>=1.3,<2' \
        'fastapi>=0.115,<1' \
        'uvicorn>=0.30,<1' \
        'imageio-ffmpeg>=0.6,<1'
fi

"$PYTHON" -c \
    'import piper, fastapi, uvicorn, imageio_ffmpeg' \
    || error "Die benötigten Python-Pakete lassen sich nicht importieren."

mkdir -p "$MODEL_DIR"

download_if_missing() {
    local url="$1"
    local destination="$2"
    local temporary

    if [[ -s "$destination" ]]; then
        printf 'Bereits vorhanden: %s\n' "$destination"
        return
    fi

    temporary="$(mktemp "$MODEL_DIR/.download.XXXXXXXX")"
    printf 'Lade herunter: %s\n' "$destination"

    if ! curl \
        --fail --location --show-error --silent \
        --retry 3 --retry-delay 2 \
        --connect-timeout 15 \
        --max-time 900 \
        "$url" --output "$temporary"; then
        rm -f "$temporary"
        error "Download fehlgeschlagen: $url"
    fi

    if [[ ! -s "$temporary" ]]; then
        rm -f "$temporary"
        error "Leere Datei heruntergeladen: $url"
    fi

    mv -f "$temporary" "$destination"
}

download_if_missing \
    "$REPO/de_DE-dii-high.onnx" \
    "$MODEL"

download_if_missing \
    "$REPO/de_DE-dii-high.onnx.json" \
    "$CONFIG"

# Prüft Modell UND Konfiguration, bevor der HTTP-Server gestartet wird.
PIPER_MODEL="$MODEL" "$PYTHON" -c \
    'import os; from piper import PiperVoice; PiperVoice.load(os.environ["PIPER_MODEL"])' \
    || error "Piper kann die Stimme nicht laden. Prüfe die beiden Modelldateien."

cat > "$SERVER" <<'PY'
import io
import logging
import math
import os
import subprocess
import wave
from contextlib import asynccontextmanager
from threading import Lock
from typing import Literal

import imageio_ffmpeg
from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from piper import PiperVoice, SynthesisConfig
from pydantic import BaseModel, ConfigDict, Field

MODEL_PATH = os.environ["PIPER_MODEL"]
VOICE_NAME = "de_DE-dii-high"
logger = logging.getLogger("piper_openai")
synthesis_lock = Lock()
loaded_voice = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global loaded_voice
    loaded_voice = PiperVoice.load(MODEL_PATH)
    yield
    loaded_voice = None


app = FastAPI(
    title="Lokale Piper-OpenAI-Sprachausgabe",
    lifespan=lifespan,
)


class SpeechRequest(BaseModel):
    model_config = ConfigDict(extra="ignore")

    model: str
    input: str = Field(min_length=1, max_length=4096)
    voice: str
    response_format: Literal["mp3", "wav", "pcm"] = "mp3"
    speed: float = 1.0


@app.get("/health")
def health():
    return {
        "status": "ok" if loaded_voice is not None else "starting",
        "voice": VOICE_NAME,
    }


@app.post("/v1/audio/speech")
def create_speech(request: SpeechRequest):
    if request.model not in ("piper", VOICE_NAME):
        raise HTTPException(
            status_code=400,
            detail="Unterstützte Modelle: piper, de_DE-dii-high",
        )

    if request.voice not in ("dii", VOICE_NAME):
        raise HTTPException(
            status_code=400,
            detail="Unterstützte Stimmen: dii, de_DE-dii-high",
        )

    if not math.isfinite(request.speed) or not 0.25 <= request.speed <= 4.0:
        raise HTTPException(
            status_code=400,
            detail="speed muss zwischen 0.25 und 4.0 liegen",
        )

    if loaded_voice is None:
        raise HTTPException(status_code=503, detail="Stimme noch nicht geladen")

    output = io.BytesIO()

    try:
        config = SynthesisConfig(length_scale=1.0 / request.speed)

        # Ein Modell wird im selben Prozess wiederverwendet; parallele
        # Synthesen werden zum Schutz des gemeinsamen Objekts serialisiert.
        with synthesis_lock:
            with wave.open(output, "wb") as wav_file:
                loaded_voice.synthesize_wav(
                    request.input,
                    wav_file,
                    syn_config=config,
                )

        wav_bytes = output.getvalue()

        if request.response_format == "wav":
            return Response(
                content=wav_bytes,
                media_type="audio/wav",
            )

        if request.response_format == "pcm":
            with wave.open(io.BytesIO(wav_bytes), "rb") as wav_file:
                if (
                    wav_file.getnchannels() != 1
                    or wav_file.getsampwidth() != 2
                    or wav_file.getframerate() != 24000
                ):
                    # OpenAI bezeichnet PCM als 24 kHz, 16 Bit, mono.
                    # Keine Audio-Daten mit falschen Parametern ausgeben.
                    raise HTTPException(
                        status_code=400,
                        detail=(
                            "PCM-Ausgabe benötigt 24 kHz, 16 Bit, mono; "
                            "dieses Modell liefert andere Parameter. "
                            "Bitte wav oder mp3 verwenden."
                        )
                    )
                pcm_bytes = wav_file.readframes(wav_file.getnframes())

            return Response(
                content=pcm_bytes,
                media_type="application/octet-stream",
            )

        command = [
            imageio_ffmpeg.get_ffmpeg_exe(),
            "-hide_banner",
            "-loglevel", "error",
            "-nostdin",
            "-f", "wav",
            "-i", "pipe:0",
            "-vn",
            "-codec:a", "libmp3lame",
            "-b:a", "128k",
            "-f", "mp3",
            "pipe:1",
        ]

        result = subprocess.run(
            command,
            input=wav_bytes,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=120,
            check=False,
        )

        if result.returncode != 0 or not result.stdout:
            detail = result.stderr.decode("utf-8", errors="replace")[:500]
            logger.error("MP3-Kodierung fehlgeschlagen: %s", detail)
            raise HTTPException(
                status_code=500,
                detail="MP3-Kodierung fehlgeschlagen; Server-Log prüfen",
            )

        return Response(
            content=result.stdout,
            media_type="audio/mpeg",
        )

    except HTTPException:
        raise
    except subprocess.TimeoutExpired as exc:
        logger.exception("Zeitüberschreitung bei der MP3-Kodierung")
        raise HTTPException(
            status_code=504,
            detail="Zeitüberschreitung bei der MP3-Kodierung",
        ) from exc
    except Exception as exc:
        logger.exception("Sprachausgabe fehlgeschlagen")
        raise HTTPException(
            status_code=500,
            detail="Sprachausgabe fehlgeschlagen; Server-Log prüfen",
        ) from exc
PY

HOST="${PIPER_HOST:-127.0.0.1}"
PORT="${PIPER_PORT:-5010}"

[[ "$HOST" == "127.0.0.1" ]] ||
    error "Aus Sicherheitsgründen ist nur PIPER_HOST=127.0.0.1 erlaubt."

[[ "$PORT" =~ ^[0-9]+$ ]] &&
[[ "$PORT" -ge 1 ]] &&
[[ "$PORT" -le 65535 ]] ||
    error "PIPER_PORT muss zwischen 1 und 65535 liegen."

printf '\nStarte Piper-API auf http://%s:%s/v1\n' "$HOST" "$PORT"
printf 'Beenden mit Strg+C. Modell: %s\n\n' "$MODEL"

export PIPER_MODEL="$MODEL"

exec "$PYTHON" -m uvicorn \
    piper_openai_server:app \
    --app-dir "$BASE_DIR" \
    --host "$HOST" \
    --port "$PORT" \
    --workers 1
