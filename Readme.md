# Piper Dii TTS for Speech Dispatcher

- Created with perplexity.ai
 
## What Is This?

This setup runs Piper TTS with the German `dii-high` voice as a local TTS server and connects it to Speech Dispatcher through the included AI output module. The `piper-dii.service` systemd unit manages the server.

## Requirements 

- ffmpeg 
- python3-pip 
- python3-venv 

## Installation

- 1. Copy `start_tts-server-piper-tts.sh` to `/home/tts/tts-server-piper-tts/` give it the users rights and make it executable.
- $ adduser tts 
- as root 
- mkdir /home/tts/tts-server-piper-tts/ && chown tts /home/tts/tts-server-piper-tts/ 
- $ cp start_tts-server-piper-tts.sh /home/tts/tts-server-piper-tts/ 
- $ chown tts /home/tts/tts-server-piper-tts/start_tts-server-piper-tts.sh 
- 2. Copy `piper-dii.service` to `/etc/systemd/system/`.
- as root 
- $ cp piper-dii.service /etc/systemd/system/ 
- $ systemctl daemon-reload && systemctl restart piper-dii.service 
- 3. In the `speech-dispatcher` directory, run the installation script, then the script that prints the `AddModule` line:

   ```bash
   cd speech-dispatcher
   bash install_speechd_ai.sh
   bash show-speechd-ai-addmodule.sh
   ```

- 4. Copy the complete `AddModule` line printed by the second script into **both** `/etc/speech-dispatcher/speechd.conf` and `~/.config/speech-dispatcher/speechd.conf` for the user who will run Speech Dispatcher. Check for an existing identical line before adding another one. The user configuration matters: adding the line only to `/etc/speech-dispatcher/speechd.conf` was not sufficient in this setup.
- 5. Open root's crontab with `sudo crontab -e` and add this line at the end:

   ```cron
   @reboot systemctl restart piper-dii.service
   ```

- 6. Reboot the machine.

## Usage

After rebooting, the systemd service should run the local Piper TTS server, and Speech Dispatcher should have the output module named by the `AddModule` line available. Use that module in your Speech Dispatcher client or configuration to speak with the German `dii-high` voice.

- To check the server and available output modules, run:

```bash
systemctl status piper-dii.service
spd-say -O
```

- Use the module name shown in the `AddModule` line for a direct Speech Dispatcher test; if it is `piper`, for example:

```bash
spd-say -o piper "Hallo, dies ist ein Test mit Piper."
```

- If the server is running but the module does not appear or does not speak, check that the `AddModule` line is present in the **user's** `~/.config/speech-dispatcher/speechd.conf` as well as in the system configuration.
