import math
import os
import struct
import tempfile
import unittest
import wave

from sonance.upmixer import UpmixConfig, upmix_stereo_wav_to_5_1


def _write_test_stereo(path: str, frames: int = 4800, sample_rate: int = 48000) -> None:
    data = []
    for n in range(frames):
        t = n / sample_rate
        l = int(12000 * math.sin(2 * math.pi * 440 * t))
        r = int(12000 * math.sin(2 * math.pi * 660 * t))
        data.extend([l, r])

    packed = struct.pack("<" + "h" * len(data), *data)
    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(sample_rate)
        w.writeframes(packed)


class UpmixerTests(unittest.TestCase):
    def test_outputs_5_1_wav_with_matching_frame_count(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            in_path = os.path.join(td, "in.wav")
            out_path = os.path.join(td, "out.wav")
            _write_test_stereo(in_path, frames=2048)

            upmix_stereo_wav_to_5_1(in_path, out_path)

            with wave.open(in_path, "rb") as src, wave.open(out_path, "rb") as out:
                self.assertEqual(src.getnframes(), out.getnframes())
                self.assertEqual(out.getnchannels(), 6)
                self.assertEqual(out.getsampwidth(), 2)
                self.assertEqual(src.getframerate(), out.getframerate())

    def test_rejects_non_stereo_input(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            in_path = os.path.join(td, "mono.wav")
            out_path = os.path.join(td, "out.wav")

            with wave.open(in_path, "wb") as w:
                w.setnchannels(1)
                w.setsampwidth(2)
                w.setframerate(48000)
                w.writeframes(struct.pack("<h", 0) * 100)

            with self.assertRaises(ValueError):
                upmix_stereo_wav_to_5_1(in_path, out_path)

    def test_rejects_invalid_config_values(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            in_path = os.path.join(td, "in.wav")
            out_path = os.path.join(td, "out.wav")
            _write_test_stereo(in_path, frames=64)

            invalid_configs = [
                UpmixConfig(center_gain=-0.1),
                UpmixConfig(lfe_gain=-1.0),
                UpmixConfig(surround_gain=-0.5),
                UpmixConfig(stereo_preserve_gain=-0.25),
                UpmixConfig(surround_delay_ms=-2.0),
                UpmixConfig(lfe_lowpass_hz=0.0),
            ]

            for config in invalid_configs:
                with self.assertRaises(ValueError):
                    upmix_stereo_wav_to_5_1(in_path, out_path, config=config)


if __name__ == "__main__":
    unittest.main()
