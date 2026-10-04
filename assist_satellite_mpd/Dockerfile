FROM ghcr.io/home-assistant/base-debian:bookworm
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
WORKDIR /usr/src
ARG LINUX_VOICE_ASSISTANT_VERSION=1.1.15
ENV PIP_BREAK_SYSTEM_PACKAGES=1
RUN apt-get update && apt-get install --yes --no-install-recommends \
    python3 python3-pip avahi-utils pulseaudio-utils alsa-utils pipewire-bin \
    pipewire-alsa pipewire-pulse build-essential libmpv-dev libasound2-plugins \
    ca-certificates iproute2 vim procps \
    && pip3 install --no-cache-dir -U setuptools wheel \
    && pip3 install --no-cache-dir \
      "linux-voice-assistant @ https://github.com/OHF-Voice/linux-voice-assistant/archive/refs/tags/v${LINUX_VOICE_ASSISTANT_VERSION}.tar.gz" \
    && apt-get clean && rm -rf /var/lib/apt/lists/*
COPY mpd_tts.py /usr/local/lib/python3.11/site-packages/linux_voice_assistant/mpd_tts.py
COPY patch_satellite.py /tmp/patch_satellite.py
RUN python3 /tmp/patch_satellite.py && rm /tmp/patch_satellite.py
COPY sounds/ ./sounds/
COPY wakewords/ ./wakewords/
WORKDIR /
COPY rootfs /
RUN chmod a+x /etc/s6-overlay/s6-rc.d/assist_satellite/run \
    /etc/s6-overlay/s6-rc.d/assist_satellite/finish \
    /etc/s6-overlay/s6-rc.d/discovery/run
HEALTHCHECK --start-period=10m CMD pgrep -f linux_voice_assistant || exit 1
