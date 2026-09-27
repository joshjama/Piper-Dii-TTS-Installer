#!/usr/bin/env bash
# Gibt die AddModule-Zeile fuer die Dateien im aktuellen Verzeichnis aus.
set -euo pipefail

project_dir=$(pwd -P)
wrapper="$project_dir/speechd_ai_wrapper"
module_config="$project_dir/speechd_ai.conf"

if [[ ! -f "$wrapper" ]]; then
    printf 'Fehler: %s nicht gefunden. Bitte im Projektverzeichnis ausfuehren.\n' "$wrapper" >&2
    exit 1
fi
if [[ ! -x "$wrapper" ]]; then
    printf 'Fehler: %s ist nicht ausfuehrbar (ggf. chmod +x speechd_ai_wrapper).\n' "$wrapper" >&2
    exit 1
fi
if [[ ! -f "$module_config" ]]; then
    printf 'Fehler: %s nicht gefunden.\n' "$module_config" >&2
    exit 1
fi

# Die Pfade stehen in doppelten Anfuehrungszeichen der speechd.conf.
# Sonderzeichen, die dort zu einer anderen Interpretation fuehren koennen,
# nicht unbemerkt in eine Konfigurationszeile uebernehmen.
if [[ "$project_dir" == *'"'* || "$project_dir" == *'\'* || "$project_dir" == *$'\n'* ]]; then
    printf 'Fehler: Der Verzeichnispfad enthaelt ", Backslash oder Zeilenumbruch.\n' >&2
    exit 1
fi

line="AddModule \"ai\" \"$wrapper\" \"$module_config\""
printf 'Diese Zeile in die verwendete speechd.conf unter die anderen AddModule-Zeilen einfuegen:\n\n%s\n\n' "$line"
printf 'Systemweite Konfiguration: /etc/speech-dispatcher/speechd.conf\n'
printf 'Moegliche Benutzerkonfiguration: %s/.config/speech-dispatcher/speechd.conf\n' "$HOME"
if [[ -f "$HOME/.config/speech-dispatcher/speechd.conf" ]]; then
    printf 'Hinweis: Eine Benutzerkonfiguration existiert. Pruefe, ob Speech Dispatcher diese verwendet.\n'
fi
printf '\nNicht in /etc/speechd.conf einfuegen, sofern dein System nicht ausdruecklich diese Datei verwendet.\n'
printf 'Dieses Skript veraendert keine Datei und startet Speech Dispatcher nicht neu.\n'
printf 'Wenn ein spaeterer Neustart fuer deine Sprachausgabe sicher ist: mit spd-say -O pruefen, ob ai geladen wurde.\n'
