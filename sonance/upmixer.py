from __future__ import annotations

from dataclasses import dataclass
import math
import struct
import wave


@dataclass(frozen=True)
class UpmixConfig:
    """Configuration for baseline stereo to 5.1 upmixing."""

    center_gain: float = 0.8
    lfe_gain: float = 0.6
    surround_gain: float = 0.65
    surround_delay_ms: float = 12.0
    stereo_preserve_gain: float = 1.0
    lfe_lowpass_hz: float = 120.0


_MAX_INT16 = 32767
_MIN_INT16 = -32768


def _validate_config(cfg: UpmixConfig) -> None:
    numeric_fields = {
        "center_gain": cfg.center_gain,
        "lfe_gain": cfg.lfe_gain,
        "surround_gain": cfg.surround_gain,
        "surround_delay_ms": cfg.surround_delay_ms,
        "stereo_preserve_gain": cfg.stereo_preserve_gain,
        "lfe_lowpass_hz": cfg.lfe_lowpass_hz,
    }

    for field_name, value in numeric_fields.items():
        if not math.isfinite(value):
            raise ValueError(f"{field_name} must be a finite number.")

    if cfg.center_gain < 0.0:
        raise ValueError("center_gain must be >= 0.")
    if cfg.lfe_gain < 0.0:
        raise ValueError("lfe_gain must be >= 0.")
    if cfg.surround_gain < 0.0:
        raise ValueError("surround_gain must be >= 0.")
    if cfg.stereo_preserve_gain < 0.0:
        raise ValueError("stereo_preserve_gain must be >= 0.")
    if cfg.surround_delay_ms < 0.0:
        raise ValueError("surround_delay_ms must be >= 0.")
    if cfg.lfe_lowpass_hz <= 0.0:
        raise ValueError("lfe_lowpass_hz must be > 0.")


def _clamp_int16(value: float) -> int:
    if value > _MAX_INT16:
        return _MAX_INT16
    if value < _MIN_INT16:
        return _MIN_INT16
    return int(value)


def _one_pole_lowpass(current: float, prev: float, alpha: float) -> float:
    return prev + alpha * (current - prev)


def upmix_stereo_wav_to_5_1(input_path: str, output_path: str, config: UpmixConfig | None = None) -> None:
    """Convert a stereo 16-bit PCM WAV file to a 5.1 16-bit PCM WAV file.

    Output channel order: L, R, C, LFE, Ls, Rs.
    """
    cfg = config or UpmixConfig()
    _validate_config(cfg)

    with wave.open(input_path, "rb") as reader:
        channels = reader.getnchannels()
        width = reader.getsampwidth()
        framerate = reader.getframerate()
        frame_count = reader.getnframes()

        if channels != 2:
            raise ValueError(f"Expected stereo input (2 channels), got {channels}.")
        if width != 2:
            raise ValueError(f"Expected 16-bit PCM input (2-byte samples), got {width} bytes.")

        raw = reader.readframes(frame_count)

    samples = struct.unpack("<" + "h" * (len(raw) // 2), raw)

    delay_samples = max(1, int((cfg.surround_delay_ms / 1000.0) * framerate))
    delay_line = [0.0] * delay_samples
    delay_index = 0

    dt = 1.0 / framerate
    rc = 1.0 / (2.0 * 3.141592653589793 * cfg.lfe_lowpass_hz)
    alpha = dt / (rc + dt)
    lfe_state = 0.0

    out = []

    for i in range(0, len(samples), 2):
        l = float(samples[i])
        r = float(samples[i + 1])

        mono = 0.5 * (l + r)
        side = 0.5 * (l - r)

        c = cfg.center_gain * mono

        lfe_state = _one_pole_lowpass(mono, lfe_state, alpha)
        lfe = cfg.lfe_gain * lfe_state

        delayed_side = delay_line[delay_index]
        delay_line[delay_index] = side
        delay_index = (delay_index + 1) % delay_samples

        ls = cfg.surround_gain * delayed_side
        rs = -cfg.surround_gain * delayed_side

        out_l = cfg.stereo_preserve_gain * l
        out_r = cfg.stereo_preserve_gain * r

        out.extend(
            [
                _clamp_int16(out_l),
                _clamp_int16(out_r),
                _clamp_int16(c),
                _clamp_int16(lfe),
                _clamp_int16(ls),
                _clamp_int16(rs),
            ]
        )

    packed = struct.pack("<" + "h" * len(out), *out)

    with wave.open(output_path, "wb") as writer:
        writer.setnchannels(6)
        writer.setsampwidth(2)
        writer.setframerate(framerate)
        writer.writeframes(packed)
