"""MPD playback helper for spoken TTS."""
import os
import socket
import time

MPD_HOST = os.environ.get("MPD_TTS_HOST", "d4261985-bluetooth-audio-manager")
MPD_PORT = int(os.environ.get("MPD_TTS_PORT", "6600"))

def command(*commands: str) -> str:
    with socket.create_connection((MPD_HOST, MPD_PORT), timeout=5) as sock:
        stream = sock.makefile("rwb")
        greeting = stream.readline().decode("utf-8", errors="replace").strip()
        if not greeting.startswith("OK MPD"):
            raise RuntimeError(f"Unexpected MPD greeting: {greeting}")
        response = []
        for cmd in commands:
            stream.write((cmd + "\n").encode())
            stream.flush()
            while True:
                line = stream.readline().decode("utf-8", errors="replace").strip()
                if line.startswith("ACK"):
                    raise RuntimeError(line)
                if line == "OK":
                    break
                response.append(line)
        return "\n".join(response)

def play_and_wait(url: str) -> None:
    safe_url = url.replace("\\", "\\\\").replace('"', '\\"')
    command("clear", f'add "{safe_url}"', "play")
    started = False
    deadline = time.monotonic() + 120
    while time.monotonic() < deadline:
        status = command("status")
        state = next((line[7:] for line in status.splitlines() if line.startswith("state: ")), None)
        if state == "play":
            started = True
        elif started and state == "stop":
            return
        time.sleep(0.1)
    command("stop")
    raise TimeoutError("MPD TTS playback timed out")
