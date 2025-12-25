from shutil import which

from app.utils.subprocess_utils import run_commands


class DockerService:
    def __init__(self) -> None:
        self.status: bool = True if which("docker") else False

    def install(self):
        run_commands(
            [
                ["apt", "update"],
                ["apt", "install", "-y", "curl"],
                ["curl", "-fsSL", "https://get.docker.com", "-o", "get-docker.sh"],
                ["sh", "./get-docker.sh"],
                ["rm", "./get-docker.sh"],
            ]
        )

    def uninstall(self):
        run_commands(
            [
                [
                    "apt",
                    "purge",
                    "docker-ce",
                    "docker-ce-cli",
                    "containerd.io",
                    "docker-buildx-plugin",
                    "docker-compose-plugin",
                    "docker-ce-rootless-extras",
                ],
                ["rm", "-rf", "/var/lib/docker"],
                ["rm", "-rf", "/var/lib/containerd"],
                ["rm", "/etc/apt/sources.list.d/docker.list"],
                ["rm", "/etc/apt/keyrings/docker.asc"],
            ]
        )
