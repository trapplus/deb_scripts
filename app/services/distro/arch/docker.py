from app.utils.subprocess_utils import run_commands
from app.services.docker import DockerService


class ArchDockerService(DockerService):
    def install(self):
        run_commands(
            [
                ["pacman", "-Sy", "--noconfirm", "docker", "docker-compose"],
                ["systemctl", "enable", "docker"],
                ["systemctl", "start", "docker"],
                ["docker", "run", "hello-world"],
            ]
        )
    
    def uninstall(self):
        run_commands(
            [
                ["systemctl", "stop", "docker"],
                ["systemctl", "disable", "docker"],
                ["pacman", "-Rns", "--noconfirm", "docker", "docker-compose"],
            ]
        )