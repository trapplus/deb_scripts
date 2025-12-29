from abc import ABC, abstractmethod

from app.utils import sysinfo_utils


class Fail2BanService(ABC):
    """Base class for Fail2Ban management"""

    def __init__(self):
        self.path_to_jail_config = "/etc/fail2ban/jail.d/sshd.local"
        self.jail_str_config = """
[sshd]
enabled = true
backend = systemd
journalmatch = _SYSTEMD_UNIT=ssh.service
maxretry = 5
port = ssh
bantime = 1d
findtime = 1h
"""

    @abstractmethod
    def install(self):
        """Install Fail2Ban"""
        pass

    @abstractmethod
    def uninstall(self):
        """Uninstall Fail2Ban"""
        pass

    @staticmethod
    def create():
        """Factory method to create instance based on OS"""
        __os: str | None = sysinfo_utils.detect_distro().lower()

        if __os == "debian":
            from app.services.distro.debian.fail2ban import DebianFail2BanService

            return DebianFail2BanService()
        if __os == "arch":
            from app.services.distro.arch.fail2ban import ArchFail2BanService

            return ArchFail2BanService()
        if __os == "openwrt":
            from app.services.distro.wrt.fail2ban import WrtFail2BanService

            return WrtFail2BanService()
        raise OSError(f"Unsupported distro: {__os}")
