from abc import ABC, abstractmethod

from app.utils import sysinfo_utils


class DockerService(ABC):
    """Base class for Docker management"""

    @abstractmethod
    def install(self):
        """Install Docker"""
        pass

    @abstractmethod
    def uninstall(self):
        """Uninstall Docker"""
        pass

    @staticmethod
    def create():
        """Factory method to create instance based on OS"""
        __os: str | None = sysinfo_utils.detect_distro().lower()

        if __os == "debian":
            from app.services.distro.debian.docker import DebianDockerService

            return DebianDockerService()
        if __os == "arch":
            from app.services.distro.arch.docker import ArchDockerService

            return ArchDockerService()
        if __os == "openwrt":
            from app.services.distro.wrt.docker import WrtDockerService

            return WrtDockerService()
        raise OSError(f"Unsupported distro: {__os}")
