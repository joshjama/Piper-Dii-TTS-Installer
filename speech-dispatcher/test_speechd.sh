#!/usr/bin/env bash
set -u

#cd /home/joshua/softwaredevelopement/ai/speechd_ai/speechd-ai || exit 1

echo '=== Konfiguration ==='
grep -E '^(AIDefaultModel|DefaultVoice) ' speechd_ai.conf

echo
echo '=== Test 1: Direkt über den Wrapper ==='
printf 'INIT\nAUDIO\n.\nSPEAK\n<speak>Hallo, dies ist ein direkter Test mit der Stimme F eins über meinen TTS-Server.</speak>\n.\nQUIT\n' |
  ./speechd_ai_wrapper speechd_ai.conf

echo
echo '=== Test 2: Über Speech Dispatcher ==='
spd-say -w -o piper \
  "Hallo, dies ist ein Test mit der Stimme F eins über Speech Dispatcher."

echo
echo '=== Letzte Meldungen des Python-Moduls ==='
tail -60 /tmp/speechd_ai.log

echo
echo '=== Letzte Meldungen des AI-Ausgabemoduls ==='
tail -40 "$XDG_RUNTIME_DIR/speech-dispatcher/log/ai.log"
