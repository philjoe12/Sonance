# Sonance

Sonance is an early-stage prototype for **real-time stereo-to-surround enhancement**.

This repository now contains a practical starting point:

- A baseline stereo → 5.1 upmix engine (rule-based DSP, no ML dependency)
- A CLI to process WAV files end-to-end
- Tests validating output format and core behavior
- An MVP architecture and product plan document

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
