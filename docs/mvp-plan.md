# Sonance MVP Plan (Stereo → Spatial)

## Product hypothesis

Users with surround systems and spatial-audio headphones will pay for clearly better immersion from stereo sources, if setup is simple and latency stays low.

## Phase 0 (this repo)

- Baseline matrix + DSP upmix engine
- Fixed 5.1 layout for evaluation
- Offline WAV pipeline for deterministic testing

## Phase 1 (desktop beta)

- System audio capture via virtual audio device
- Real-time processing callback (< 20 ms total pipeline latency target)
- Presets: Music Balanced, Vocal Focus, Wide Stage, Cinema
- Device output selector + calibration test tone

## Phase 2 (AI enhancement)

- Add lightweight source-separation model (vocals/drums/bass/other)
- Route stems to channel groups with confidence gating
- Hybrid DSP fallback when model confidence drops

## Phase 3 (differentiation)

- Personalized room adaptation using calibration sweep + mic capture
- Dynamic spatial scene prediction (depth and width)
- SDK mode for OEM/partners

## Success metrics

- Setup time: < 5 minutes from install to first playback
- Latency: <= 20 ms
- CPU budget: <= 15% on mainstream desktop CPU
- Subjective lift: users prefer Sonance to AVR upmix in blind A/B


## Delivery constraints (must-pass before broader rollout)

- Driver install success rate must stay high enough for self-serve onboarding.
- Routing reliability across sleep/wake and default-device changes must be verified.
- Stereo pass-through fallback must trigger automatically on processing failure.
- Hardware compatibility list should be explicit and phased by validated endpoint families.
- Legal/compliance review must confirm local-only processing posture and provider-safe messaging.

See [`docs/constraints-register.md`](constraints-register.md) for detailed constraints and mitigations.
