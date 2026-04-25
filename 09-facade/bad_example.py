# bad_example.py - client must coordinate five subsystem classes
from __future__ import annotations


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


def convert_video(source: str, target: str, format_: str) -> str:
    codec = VideoCodec()
    raw = codec.select(source, format_)
    extractor = AudioExtractor()
    audio = extractor.extract(raw)
    optimizer = BitrateOptimizer()
    optimized = optimizer.optimize(raw, audio, quality=720)
    muxer = Muxer()
    muxed = muxer.mux(optimized)
    writer = FileWriter()
    return writer.write(muxed, target)


if __name__ == "__main__":
    result = convert_video("input.avi", "output.mp4", "mp4")
    print(f"Converted: {result}")
