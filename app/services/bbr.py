from abc import ABC, abstractmethod

from app.utils import sysinfo_utils


class BBRService(ABC):
    """Base class for BBR congestion control management"""

    def __init__(self):
        self.path_to_sysctl_config = "/etc/sysctl.conf"
        self.bbr_config = """
net.core.default_qdisc=fq_codel
net.ipv4.tcp_congestion_control=bbr
"""

    @abstractmethod
    def enable(self):
        """Enable BBR"""
        pass

    @abstractmethod
    def disable(self):
        """Disable BBR"""
        pass

    @staticmethod
    def create():
        """Factory method to create instance based on OS"""
        __os: str | None = sysinfo_utils.detect_distro().lower()

        if __os == "debian":
            from app.services.distro.debian.bbr import DebianBBRService

            return DebianBBRService()
        if __os == "arch":
            from app.services.distro.arch.bbr import ArchBBRService

            return ArchBBRService()
        if __os == "openwrt":
            from app.services.distro.wrt.bbr import WrtBBRService

            return WrtBBRService()
        raise OSError(f"Unsupported distro: {__os}")
