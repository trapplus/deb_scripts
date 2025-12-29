from app.utils.subprocess_utils import run_commands
from app.services.docker import DockerService


class WrtDockerService(DockerService):
    def install(self):
        print("Docker installation on OpenWrt is not recommended")
        print("OpenWrt typically doesn't have enough resources for Docker")
        print("Consider using LXC containers instead")
        
        run_commands(
            [
                ["opkg", "update"],
                ["opkg", "install", "dockerd", "docker-compose"],
                ["/etc/init.d/dockerd", "enable"],
                ["/etc/init.d/dockerd", "start"],
            ]
        )
    
    def uninstall(self):
        run_commands(
            [
                ["/etc/init.d/dockerd", "stop"],
                ["/etc/init.d/dockerd", "disable"],
                ["opkg", "remove", "dockerd", "docker-compose"],
            ]
        )