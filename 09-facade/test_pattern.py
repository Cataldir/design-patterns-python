# test_facade.py - verify correct orchestration order with mocks
from __future__ import annotations

from unittest.mock import MagicMock, call

from good_example import VideoConverter


class TestVideoConverterFacade:
    def _build_mocks(self) -> dict[str, MagicMock]:
        codec = MagicMock()
        codec.select.return_value = b"raw-video"
        audio = MagicMock()
        audio.extract.return_value = b"audio-track"
        bitrate = MagicMock()
        bitrate.optimize.return_value = b"optimized-stream"
        muxer = MagicMock()
        muxer.mux.return_value = b"muxed-output"
        writer = MagicMock()
        writer.write.return_value = "output.mp4"
        return {
            "codec": codec,
            "audio": audio,
            "bitrate": bitrate,
            "muxer": muxer,
            "writer": writer,
        }

    def test_convert_calls_all_subsystems(self) -> None:
        mocks = self._build_mocks()
        facade = VideoConverter(**mocks)
        result = facade.convert("input.avi", "output.mp4", "mp4")
        mocks["codec"].select.assert_called_once_with("input.avi", "mp4")
        mocks["audio"].extract.assert_called_once_with(b"raw-video")
        mocks["bitrate"].optimize.assert_called_once_with(
            b"raw-video", b"audio-track", quality=720
        )
        mocks["muxer"].mux.assert_called_once_with(b"optimized-stream")
        mocks["writer"].write.assert_called_once_with(
            b"muxed-output", "output.mp4"
        )
        assert result == "output.mp4"

    def test_convert_calls_subsystems_in_order(self) -> None:
        manager = MagicMock()
        mocks = self._build_mocks()
        manager.attach_mock(mocks["codec"], "codec")
        manager.attach_mock(mocks["audio"], "audio")
        manager.attach_mock(mocks["bitrate"], "bitrate")
        manager.attach_mock(mocks["muxer"], "muxer")
        manager.attach_mock(mocks["writer"], "writer")
        facade = VideoConverter(**mocks)
        facade.convert("input.avi", "output.mp4")
        expected_order = [
            call.codec.select("input.avi", "mp4"),
            call.audio.extract(b"raw-video"),
            call.bitrate.optimize(b"raw-video", b"audio-track", quality=720),
            call.muxer.mux(b"optimized-stream"),
            call.writer.write(b"muxed-output", "output.mp4"),
        ]
        assert manager.mock_calls == expected_order

    def test_convert_uses_default_format(self) -> None:
        mocks = self._build_mocks()
        facade = VideoConverter(**mocks)
        facade.convert("input.avi", "output.mp4")
        mocks["codec"].select.assert_called_once_with("input.avi", "mp4")
