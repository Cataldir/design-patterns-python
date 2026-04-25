# test_proxy.py - verify lazy loading and access control
import pytest

from good_example import ImageProxy, ProtectedImage, RealImage


class TestVirtualProxy:
    def test_real_image_not_loaded_on_construction(self) -> None:
        proxy = ImageProxy("photos/sunset.png")
        assert proxy._real is None

    def test_real_image_loaded_on_first_display(self) -> None:
        proxy = ImageProxy("photos/sunset.png")
        proxy.display()
        assert proxy._real is not None

    def test_subsequent_display_reuses_same_instance(self) -> None:
        proxy = ImageProxy("photos/sunset.png")
        proxy.display()
        first = proxy._real
        proxy.display()
        assert proxy._real is first

    def test_get_path_does_not_trigger_loading(self) -> None:
        proxy = ImageProxy("photos/sunset.png")
        assert proxy.get_path() == "photos/sunset.png"
        assert proxy._real is None


class TestProtectionProxy:
    def test_viewer_cannot_display(self) -> None:
        real = RealImage("photos/secret.png")
        protected = ProtectedImage(real, role="viewer")
        with pytest.raises(PermissionError, match="viewer"):
            protected.display()

    def test_admin_can_display(self) -> None:
        real = RealImage("photos/secret.png")
        protected = ProtectedImage(real, role="admin")
        result = protected.display()
        assert "secret.png" in result

    def test_composed_proxies_lazy_load_with_access_control(self) -> None:
        lazy = ImageProxy("photos/secret.png")
        protected = ProtectedImage(lazy, role="admin")
        protected.display()
        assert lazy._real is not None
