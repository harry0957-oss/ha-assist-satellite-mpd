from pathlib import Path
p = Path("/usr/local/lib/python3.11/site-packages/linux_voice_assistant/satellite.py")
s = p.read_text()
import_line = "from .mpd_tts import play_and_wait\n"
anchor = "from .util import call_all\n"
if import_line not in s:
    if anchor not in s:
        raise SystemExit("Import anchor not found")
    s = s.replace(anchor, anchor + import_line, 1)
old = "        self.state.tts_player.play(self._tts_url, done_callback=self._tts_finished)\n"
new = """        threading.Thread(
            target=self._play_tts_mpd,
            name="mpd-tts",
            daemon=True,
        ).start()
"""
if old not in s and "target=self._play_tts_mpd" not in s:
    raise SystemExit("TTS playback anchor not found")
if old in s:
    s = s.replace(old, new, 1)
method_anchor = "    def _tts_finished(self) -> None:\n"
method = """    def _play_tts_mpd(self) -> None:
        try:
            play_and_wait(self._tts_url)
        except Exception:
            _LOGGER.exception("MPD TTS playback failed")
        finally:
            self._tts_finished()

"""
if "def _play_tts_mpd" not in s:
    if method_anchor not in s:
        raise SystemExit("TTS finished anchor not found")
    s = s.replace(method_anchor, method + method_anchor, 1)
p.write_text(s)
