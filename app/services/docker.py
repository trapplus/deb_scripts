from app.utils import sysinfo_utils

__os: str | None = sysinfo_utils.detect_distro().lower()

if __os == "debian":
    from app.services.distro.debian.docker import DockerService
elif __os == "arch":
    from app.services.distro.arch.docker import DockerService
elif __os == "openwrt":
    from app.services.distro.wrt.docker import DockerService
else:
    raise OSError("Unsuported distro!")

dockerservice = DockerService()
