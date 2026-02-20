# Sonance

Sonance is an early-stage prototype for **real-time stereo-to-surround enhancement**.

This repository now contains a practical starting point:

- A baseline stereo → 5.1 upmix engine (rule-based DSP, no ML dependency)
- A CLI to process WAV files end-to-end
- Tests validating output format and core behavior
- An MVP architecture and product plan document

## Is this desktop or mobile?

**V1 should be desktop-first** (Windows/macOS), not mobile.

Why:

- Desktop allows system-audio capture and virtual audio devices needed for real-time processing.
- Mobile OSes heavily sandbox third-party apps and generally block arbitrary system-audio interception.
- Desktop users are more likely to already have 5.1/7.1/Atmos-capable output chains.

Mobile can be a later phase via:

- Headphone-focused spatial post-processing inside a dedicated player app, or
- Platform-specific extensions where allowed.

## How Sonance coordinates with speaker systems

Sonance sits **between audio apps and the real playback device**:

1. User installs Sonance + virtual output device.
2. User sets Sonance Virtual Device as system default output.
3. Spotify/YouTube/etc. output stereo PCM to Sonance.
4. Sonance upmixes/processes in real time.
5. Sonance sends 5.1/7.1 PCM to the selected physical endpoint (USB DAC, AVR via HDMI, sound card, etc.).

This means no Spotify API integration is required. Sonance acts like a system audio processor.

See [`docs/system-architecture.md`](docs/system-architecture.md) for detailed signal flow, device handling, and customer UX.

## Why this starter

Before building AI spatial reconstruction, you need a measurable baseline. This project gives you:

1. A deterministic upmixer to benchmark against
2. A clear contract for channel mapping/output layout
3. A place to plug in ML source-separation later

## Quick start

```bash
python -m sonance.cli input_stereo.wav output_5_1.wav
```

The current prototype expects:

- Input: 16-bit PCM stereo WAV
- Output: 16-bit PCM 5.1 WAV in channel order: `L, R, C, LFE, Ls, Rs`

## Run tests

```bash
python -m unittest discover -s tests -p 'test_*.py' -v
```

## Next steps

See [`docs/mvp-plan.md`](docs/mvp-plan.md) for the staged build plan from this baseline to a low-latency AI spatial engine.
