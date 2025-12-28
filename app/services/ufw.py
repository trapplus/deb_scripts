from abc import ABC, abstractmethod

from app.utils import sysinfo_utils


class UFWService(ABC):
    """Base class for UFW management"""

    def __init__(self):
        self.default_rules = [
            ("allow", "22/tcp", "SSH"),
            ("allow", "80/tcp", "HTTP"),
            ("allow", "443/tcp", "HTTPS"),
        ]

    @abstractmethod
    def install(self):
        """Install UFW"""
        pass

    @abstractmethod
    def uninstall(self):
        """Uninstall UFW"""
        pass

    @abstractmethod
    def _check_service_status(self, expected_status: str) -> bool:
        """Check service status"""
        pass

    @staticmethod
    def create():
        """Factory method to create instance based on OS"""
        __os: str | None = sysinfo_utils.detect_distro().lower()

        if __os == "debian":
            from app.services.distro.debian.ufw import DebianUFWService

            return DebianUFWService()
        elif __os == "arch":
            from app.services.distro.arch.ufw import ArchUFWService

            return ArchUFWService()
        elif __os == "openwrt":
            from app.services.distro.wrt.ufw import WrtUFWService

            return WrtUFWService()
        else:
            raise OSError(f"Unsupported distro: {__os}")

    @staticmethod
    def is_supported() -> bool:
        """Check if current OS is supported"""
        try:
            __os = sysinfo_utils.detect_distro().lower()
            return __os in ["debian", "arch", "openwrt"]
        except Exception:
            return False

    @staticmethod
    def get_distro() -> str:
        """Get current distribution"""
        return sysinfo_utils.detect_distro().lower()
