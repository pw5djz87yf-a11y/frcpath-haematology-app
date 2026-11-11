#!/bin/bash
# Records the Module 1 narration with a macOS voice (default: Jamie (Premium)).
# Uses only built-in macOS tools. Run in Terminal:   bash ~/Downloads/make_jamie_voice.sh
# Result: jamie_audio.zip on your Desktop. Send it back to Claude in the chat.
set -euo pipefail
VOICE="${1:-Jamie (Premium)}"
RATE="${2:-170}"
if ! say -v '?' | grep -qF "$VOICE"; then
  echo "The voice \"$VOICE\" is not installed."
  echo "Install it: System Settings > Accessibility > Spoken Content > System voice > Manage Voices..."
  echo "  > English (United Kingdom) > Jamie (Premium). Then run this script again."
  echo "Installed English voices:"; say -v '?' | grep -E "en_GB|en-GB" || true
  exit 1
fi
WORK="$(mktemp -d)/jamie_audio"; mkdir -p "$WORK"
TOTAL=$(grep -c $'\t' <<'LINES'
__LINES__
LINES
)
N=0
while IFS=$'\t' read -r ID TEXT; do
  [ -z "$ID" ] && continue
  N=$((N+1)); printf '\rRecording line %d of %d...' "$N" "$TOTAL"
  say -v "$VOICE" -r "$RATE" --file-format=WAVE --data-format=LEI16@22050 -o "$WORK/$ID.wav" -- "$TEXT"
done <<'LINES'
__LINES__
LINES
echo
( cd "$(dirname "$WORK")" && zip -qr "$HOME/Desktop/jamie_audio.zip" jamie_audio )
echo "Done: $HOME/Desktop/jamie_audio.zip ($N lines, voice: $VOICE)"
