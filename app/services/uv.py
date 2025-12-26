from app.utils import sysinfo_utils

__os: str | None = sysinfo_utils.defect_distro().lower()

if __os == "debian":
    from app.services.distro.debian.uv import UVService
elif __os == "arch":
    from app.services.distro.arch.uv import UVService
elif __os == "openwrt":  # TODO
    from app.services.distro.wrt.uv import UVService
else:
    raise OSError("Unsuported distro!")
