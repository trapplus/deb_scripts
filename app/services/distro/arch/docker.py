from shutil import which

from app.utils.subprocess_utils import run_commands

class DockerService:
    def __init__(self) -> None:
        self.status: bool = True if which("docker") else False
    
    def install(self):
        run_commands(
            [
                ["pacman", "-Syu", "--noconfirm", "docker", "docker-compose"],
                ["systemctl", "enable", "docker"],
                ["systemctl", "start", "docker"],
            ]
        )
    
    def uninstall(self):
        run_commands(
            [
                ["systemctl", "stop", "docker"],
                ["systemctl", "disable", "docker"],
                ["pacman", "-Rns", "--noconfirm", "docker", "docker-compose"],
                ["rm", "-rf", "/var/lib/docker"],
                ["rm", "-rf", "/var/lib/containerd"],
            ]
        )