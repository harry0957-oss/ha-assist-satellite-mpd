FROM ghcr.io/home-assistant/base-debian:bookworm
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
WORKDIR /usr/src
ARG LINUX_VOICE_ASSISTANT_VERSION=1.1.15
ENV PIP_BREAK_SYSTEM_PACKAGES=1
RUN apt-get update && apt-get install --yes --no-install-recommends \
    python3 python3-pip git avahi-utils pulseaudio-utils alsa-utils pipewire-bin \
    pipewire-alsa pipewire-pulse build-essential libmpv-dev libasound2-plugins \
    ca-certificates iproute2 vim procps \
    && pip3 install --no-cache-dir -U setuptools wheel \
    && pip3 install --no-cache-dir \
      "linux-voice-assistant @ https://github.com/OHF-Voice/linux-voice-assistant/archive/refs/tags/v${LINUX_VOICE_ASSISTANT_VERSION}.tar.gz" \
    && git clone --depth 1 https://github.com/OHF-Voice/apps.git /tmp/ohf-apps \
    && apt-get clean && rm -rf /var/lib/apt/lists/*
COPY mpd_tts.py /tmp/mpd_tts.py
COPY patch_satellite.py /tmp/patch_satellite.py
RUN SITE_DIR="$(python3 -c 'import site; print(site.getsitepackages()[0])')" \
    && cp /tmp/mpd_tts.py "$SITE_DIR/linux_voice_assistant/mpd_tts.py" \
    && python3 /tmp/patch_satellite.py "$SITE_DIR/linux_voice_assistant/satellite.py" \
    && rm /tmp/mpd_tts.py /tmp/patch_satellite.py
RUN cp -a /tmp/ohf-apps/assist_satellite/sounds /usr/src/sounds \
    && cp -a /tmp/ohf-apps/assist_satellite/wakewords /usr/src/wakewords \
    && cp -a /tmp/ohf-apps/assist_satellite/rootfs/. / \
    && rm -rf /tmp/ohf-apps
RUN chmod a+x /etc/s6-overlay/s6-rc.d/assist_satellite/run \
    /etc/s6-overlay/s6-rc.d/assist_satellite/finish \
    /etc/s6-overlay/s6-rc.d/discovery/run
HEALTHCHECK --start-period=10m CMD pgrep -f linux_voice_assistant || exit 1
