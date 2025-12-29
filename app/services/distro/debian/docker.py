from subprocess import run
from app.utils.subprocess_utils import run_commands
from app.services.docker import DockerService


class DebianDockerService(DockerService):
    def install(self):
        run_commands(
            [
                ["apt", "update"],
                ["apt", "install", "-y", "ca-certificates", "curl"],
                ["install", "-m", "0755", "-d", "/etc/apt/keyrings"],
            ]
        )
        
        run_commands(
            [
                [
                    "curl",
                    "-fsSL",
                    "https://download.docker.com/linux/debian/gpg",
                    "-o",
                    "/etc/apt/keyrings/docker.asc",
                ],
                ["chmod", "a+r", "/etc/apt/keyrings/docker.asc"],
            ]
        )
        
        distro_info = run(
            ["bash", "-c", ". /etc/os-release && echo \"$VERSION_CODENAME\""],
            capture_output=True,
            text=True,
        ).stdout.strip()
        
        arch = run(["dpkg", "--print-architecture"], capture_output=True, text=True).stdout.strip()
        
        repo_line = f"deb [arch={arch} signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian {distro_info} stable"
        
        with open("/etc/apt/sources.list.d/docker.list", "w", encoding="utf-8") as f:
            f.write(repo_line + "\n")
        
        run_commands(
            [
                ["apt", "update"],
                [
                    "apt",
                    "install",
                    "-y",
                    "docker-ce",
                    "docker-ce-cli",
                    "containerd.io",
                    "docker-buildx-plugin",
                    "docker-compose-plugin",
                ],
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
                [
                    "apt",
                    "remove",
                    "-y",
                    "docker-ce",
                    "docker-ce-cli",
                    "containerd.io",
                    "docker-buildx-plugin",
                    "docker-compose-plugin",
                ],
                ["apt", "autoremove", "-y"],
                ["rm", "-f", "/etc/apt/sources.list.d/docker.list"],
                ["rm", "-f", "/etc/apt/keyrings/docker.asc"],
            ]
        )