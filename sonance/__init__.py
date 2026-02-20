"""Sonance prototype package."""

from .upmixer import (
    StreamingUpmixer,
    UpmixConfig,
    upmix_stereo_wav_to_5_1,
    validate_config,
)

__all__ = [
    "UpmixConfig",
    "StreamingUpmixer",
    "validate_config",
    "upmix_stereo_wav_to_5_1",
]
