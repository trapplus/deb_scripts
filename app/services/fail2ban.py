from app.utils import sysinfo_utils

__os: str | None = sysinfo_utils.detect_distro().lower()

if __os == "debian":
    from app.services.distro.debian.fail2ban import Fail2BanService
elif __os == "arch":
    from app.services.distro.arch.fail2ban import Fail2BanService
elif __os == "openwrt":  # TODO
    from app.services.distro.wrt.fail2ban import Fail2BanService
else:
    raise OSError("Unsuported distro!")
