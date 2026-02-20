from __future__ import annotations

import argparse

from .upmixer import UpmixConfig, upmix_stereo_wav_to_5_1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Sonance stereo to 5.1 upmix prototype")
    parser.add_argument("input", help="Path to input stereo WAV (16-bit PCM)")
    parser.add_argument("output", help="Path to output 5.1 WAV")
    parser.add_argument("--center-gain", type=float, default=0.8)
    parser.add_argument("--lfe-gain", type=float, default=0.6)
    parser.add_argument("--surround-gain", type=float, default=0.65)
    parser.add_argument("--surround-delay-ms", type=float, default=12.0)
    parser.add_argument("--stereo-preserve-gain", type=float, default=1.0)
    parser.add_argument("--lfe-lowpass-hz", type=float, default=120.0)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    config = UpmixConfig(
        center_gain=args.center_gain,
        lfe_gain=args.lfe_gain,
        surround_gain=args.surround_gain,
        surround_delay_ms=args.surround_delay_ms,
        stereo_preserve_gain=args.stereo_preserve_gain,
        lfe_lowpass_hz=args.lfe_lowpass_hz,
    )
    upmix_stereo_wav_to_5_1(args.input, args.output, config)


if __name__ == "__main__":
    main()
