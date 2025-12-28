from app.utils import sysinfo_utils

__os: str | None = sysinfo_utils.detect_distro().lower()

if __os == "debian":
    from app.services.distro.debian.bbr import BBRService
elif __os == "arch":
    from app.services.distro.arch.bbr import BBRService
elif __os == "openwrt":  # TODO
    from app.services.distro.wrt.bbr import BBRService
else:
    raise OSError("Unsuported distro!")
