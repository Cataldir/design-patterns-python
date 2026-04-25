# good_example.py - facade with Protocol-based subsystems
from __future__ import annotations

from typing import Protocol


class VideoCodecProtocol(Protocol):
    def select(self, source: str, format_: str) -> bytes: ...


class AudioExtractorProtocol(Protocol):
    def extract(self, raw_data: bytes) -> bytes: ...


class BitrateOptimizerProtocol(Protocol):
    def optimize(
        self, video: bytes, audio: bytes, quality: int
    ) -> bytes: ...


class MuxerProtocol(Protocol):
    def mux(self, optimized: bytes) -> bytes: ...


class FileWriterProtocol(Protocol):
    def write(self, data: bytes, target: str) -> str: ...


class VideoCodec:
    def select(self, source: str, format_: str) -> bytes:
        print(f"[VideoCodec] Selecting codec for {format_}")
        return f"codec-data:{source}:{format_}".encode()


class AudioExtractor:
    def extract(self, raw_data: bytes) -> bytes:
        print("[AudioExtractor] Extracting audio track")
        return b"audio:" + raw_data


class BitrateOptimizer:
    def optimize(self, video: bytes, audio: bytes, quality: int) -> bytes:
        print(f"[BitrateOptimizer] Optimizing to quality={quality}")
        return b"optimized:" + video + b"|" + audio


class Muxer:
    def mux(self, optimized: bytes) -> bytes:
        print("[Muxer] Muxing audio and video streams")
        return b"muxed:" + optimized


class FileWriter:
    def write(self, data: bytes, target: str) -> str:
        print(f"[FileWriter] Writing output to {target}")
        return target


class VideoConverter:
    """Facade: one method orchestrates the entire conversion pipeline."""

    def __init__(
        self,
        codec: VideoCodecProtocol | None = None,
        audio: AudioExtractorProtocol | None = None,
        bitrate: BitrateOptimizerProtocol | None = None,
        muxer: MuxerProtocol | None = None,
        writer: FileWriterProtocol | None = None,
    ) -> None:
        self._codec = codec if codec is not None else VideoCodec()
        self._audio = audio if audio is not None else AudioExtractor()
        self._bitrate = bitrate if bitrate is not None else BitrateOptimizer()
        self._muxer = muxer if muxer is not None else Muxer()
        self._writer = writer if writer is not None else FileWriter()

    def convert(self, source: str, target: str, format_: str = "mp4") -> str:
        raw = self._codec.select(source, format_)
        audio = self._audio.extract(raw)
        optimized = self._bitrate.optimize(raw, audio, quality=720)
        muxed = self._muxer.mux(optimized)
        return self._writer.write(muxed, target)


if __name__ == "__main__":
    converter = VideoConverter()
    result = converter.convert("input.avi", "output.mp4")
    print(f"Converted: {result}")
