# Sonance System Architecture (Desktop-first)

## Product form factor

- **Primary target:** desktop application (Windows first, macOS second)
- **Not initial target:** full system-level mobile interception

This is a low-latency audio middleware product, so desktop OSes are the practical starting point.

## Customer workflow

1. Install Sonance desktop app.
2. Install/enable Sonance virtual audio device.
3. Select **Sonance Virtual Device** as default system output.
4. In Sonance app, select physical output endpoint and layout:
   - 5.1 / 7.1 / Atmos-capable AVR
   - multichannel USB interface
   - headphones (virtual surround mode)
5. Play music normally in Spotify (or any app).
6. Sonance processes stream and routes to selected endpoint.

## Audio signal flow

```text
[Spotify/Desktop App] --stereo PCM--> [Sonance Virtual Device Input]
                                   --> [Real-time Processing Graph]
                                   --> [Output Device Adapter]
                                   --> [Physical Endpoint: AVR / DAC / Headphones]
```

Processing graph stages for MVP:

- Input resample/normalize (if needed)
- Stereo analysis (mid/side)
- Baseline upmix matrix + surround delay + LFE low-pass
- Per-channel limiter/clipping guard
- Output remap according to endpoint layout profile

Later AI stages:

- Source separation (vocals/bass/drums/other)
- Spatial scene estimation and dynamic object placement

## Speaker-system coordination details

### 1) Endpoint capability detection

Sonance reads OS audio endpoint metadata:

- Supported sample rates
- Channel counts/layouts
- Exclusive/shared mode support

If endpoint does not support selected layout, app falls back automatically and informs user.

### 2) Channel layout profiles

Sonance maintains explicit channel maps (for example):

- 5.1: `L, R, C, LFE, Ls, Rs`
- 7.1: `L, R, C, LFE, Ls, Rs, Lb, Rb`

The app renders to an internal canonical bus and remaps to endpoint-specific ordering.

### 3) Clocking and drift control

Input and output clocks can drift. Sonance uses:

- Ring buffers
- Minor asynchronous resampling
- Drift monitoring thresholds

to avoid underruns/overruns and keep latency stable.

### 4) Latency management

Latency budget target for “feels real-time”:

- Buffering + processing + output: <= 20 ms total

App exposes low/medium/high stability presets to trade latency vs dropout risk.

### 5) User calibration

Calibration UX includes:

- Speaker test tone (channel-by-channel)
- Per-channel trim (dB)
- Optional distance/delay settings

This ensures “rear/center/LFE feel wrong” issues are solvable without expert setup.

## Desktop vs mobile reality

### Desktop

- Feasible now via virtual audio drivers and user-selected endpoints.
- Best path for home theater customers.

### Mobile

- System-wide capture/rerouting usually restricted.
- Practical options are narrower:
  - in-app playback pipeline
  - headphone-focused effects
  - limited OS-specific audio-extension paths

## Recommended go-to-market implementation order

1. Windows desktop system-wide version (highest control + user base).
2. macOS desktop version (CoreAudio integration).
3. Headphone mode and calibration polish.
4. Explore mobile companion only after desktop PMF.
