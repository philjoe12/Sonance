# Sonance Constraints Register (Additional Non-Obvious Constraints)

This document captures constraints that can break a stereo→surround product even when DSP quality is good.

## 1) Platform and driver constraints

- **Virtual driver signing/distribution:** Windows/macOS driver installation and trust prompts can reduce install conversion.
- **OS audio API differences:** WASAPI/CoreAudio behaviors differ for shared/exclusive mode, channel masks, and format negotiation.
- **Background lifecycle:** app restarts, sleep/wake, and default-device changes can silently break routing.

## 2) Latency and reliability constraints

- **End-to-end latency budget:** if total latency rises above ~20 ms, users perceive lag and “detached” playback.
- **Clock drift:** input and output device clocks drift over time; requires drift compensation.
- **Underrun resilience:** CPU spikes from other apps can produce pops/clicks unless buffering strategy is adaptive.

## 3) Device compatibility constraints

- **Channel-order mismatch:** physical endpoints may report non-canonical ordering.
- **Endpoint capability mismatch:** many devices report 5.1 support but fail at specific sample rates/bit depths.
- **Bluetooth limitations:** many Bluetooth profiles collapse to stereo and add high latency.

## 4) Content and policy constraints

- **Local-only processing boundary:** process audio on-device only; avoid storing or redistributing copyrighted streams.
- **Provider terms sensitivity:** avoid implying official integration with Spotify or other services.
- **DRM/protected path behavior:** some protected playback paths may block interception/rerouting.

## 5) UX constraints

- **Setup complexity ceiling:** too many routing steps kills adoption.
- **Calibration burden:** users need quick speaker checks (test tones, trims, delays) without pro-audio jargon.
- **Safe fallback behavior:** if processing fails, app should auto-fallback to stereo pass-through, not silence.

## 6) Performance and model constraints (AI phases)

- **Model footprint:** large separation models can exceed practical CPU/GPU budgets.
- **Artifact management:** aggressive separation causes musical artifacts that may be worse than AVR upmix.
- **Confidence gating:** low-confidence frames need hybrid DSP fallback logic.

## 7) Business and operations constraints

- **QA matrix size:** OS version × device driver × endpoint layout grows quickly.
- **Supportability:** routing/debug tooling is mandatory to resolve “no sound” tickets quickly.
- **Licensing strategy:** Atmos/object-audio branding and codec paths can require licensing/legal review.

## 8) Security/privacy constraints

- **Telemetry minimization:** diagnostics should avoid raw audio capture by default.
- **Crash diagnostics:** logs should include routing and format metadata without exposing private content.
- **Hardening:** audio-driver and IPC surfaces should be treated as privileged attack surfaces.

## Recommended product guardrails

- Ship desktop-first with explicit “best effort by endpoint” compatibility messaging.
- Enforce strict input/config validation and predictable fallback behavior.
- Add runtime diagnostics panel (device format, latency, buffer health, drift status).
- Stage rollout by a curated hardware compatibility list before broad release.
