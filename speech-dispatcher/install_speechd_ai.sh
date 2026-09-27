#!/usr/bin/env bash
set -Eeuo pipefail

# Im Stammverzeichnis des bereits geklonten speechd-ai-Repositories ausführen.
repo=$(pwd -P)
wrapper="$repo/speechd_ai_wrapper"
module="$repo/speechd_ai.py"
config="$repo/speechd_ai.conf"
venv="$repo/.venv"

for file in "$wrapper" "$module" "$config"; do
    if [[ ! -f "$file" ]]; then
        printf 'Fehler: Datei fehlt: %s\nBitte dieses Skript im Repository-Stammverzeichnis ausführen.\n' "$file" >&2
        exit 1
    fi
done
if [[ "$repo" == *'"'* || "$repo" == *$'\n'* ]]; then
    printf 'Fehler: Repository-Pfad enthält ein Anführungszeichen oder einen Zeilenumbruch.\n' >&2
    exit 1
fi
if ! command -v python3 >/dev/null 2>&1; then
    printf 'Fehler: python3 fehlt.\n' >&2
    exit 1
fi

printf 'Repository: %s\n' "$repo"
if [[ ! -x "$venv/bin/python3" ]]; then
    printf 'Erstelle virtuelle Python-Umgebung ...\n'
    python3 -m venv "$venv" || {
        printf 'Fehler beim Erstellen der Umgebung. Auf Debian/Ubuntu ggf. python3-venv installieren.\n' >&2
        exit 1
    }
fi
printf 'Installiere openai und pyaudio in .venv ...\n'
if ! "$venv/bin/python3" -m pip install openai pyaudio; then
    printf '\nInstallation fehlgeschlagen. Falls PyAudio wegen portaudio.h scheitert:\n' >&2
    printf 'Auf Debian/Ubuntu: sudo apt install portaudio19-dev python3-dev\n' >&2
    printf 'Danach dieses Skript erneut ausführen.\n' >&2
    exit 1
fi
"$venv/bin/python3" -c 'import openai, pyaudio; print("Python-Imports: OK")'
if [[ ! -x "$wrapper" ]]; then
    chmod u+x "$wrapper"
    printf 'Wrapper für den aktuellen Benutzer ausführbar gemacht.\n'
fi

printf '\nInstallation abgeschlossen.\n'
printf 'Die Server-Basis-URL und das Modell bitte separat in %s prüfen.\n' "$config"
printf '\nDiese Zeile in die tatsächlich verwendete speechd.conf eintragen:\n\n'
printf 'AddModule "ai" "%s" "%s"\n' "$wrapper" "$config"
printf '\nSystemweite Datei auf Debian/Ubuntu normalerweise: /etc/speech-dispatcher/speechd.conf\n'
printf 'Alternative Benutzerdatei: ~/.config/speech-dispatcher/speechd.conf\n'
printf 'Das Skript ändert KEINE Speech-Dispatcher-Konfiguration, startet KEINEN Dienst neu und testet KEINE Audioausgabe.\n'
printf 'Die bisherige Standardstimme unverändert lassen.\n'