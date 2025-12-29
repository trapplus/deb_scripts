import time
from subprocess import run
from app.utils.subprocess_utils import run_commands
from app.services.fail2ban import Fail2BanService


class DebianFail2BanService(Fail2BanService):
    def install(self):
        run_commands([["apt", "install", "fail2ban", "-y"]])
        with open(self.path_to_jail_config, "w", encoding="utf-8") as f:
            f.write(self.jail_str_config)
        run_commands(
            [
                ["systemctl", "enable", "fail2ban"],
                ["systemctl", "restart", "fail2ban"],
            ]
        )
        status_service = ""
        while status_service != "active":
            status_service = run(
                ["systemctl", "is-active", "fail2ban"], text=True, capture_output=True
            ).stdout.strip()
            time.sleep(0.5)
        run_commands(
            [
                ["systemctl", "status", "fail2ban"],
                ["fail2ban-client", "status", "sshd"],
            ]
        )
    
    def uninstall(self):
        run_commands(
            [
                ["systemctl", "disable", "fail2ban"],
                ["systemctl", "stop", "fail2ban"],
            ]
        )
        status_service = ""
        while status_service != "inactive":
            status_service = run(
                ["systemctl", "is-active", "fail2ban"], text=True, capture_output=True
            ).stdout.strip()
            time.sleep(0.5)
        run_commands(
            [
                ["systemctl", "status", "fail2ban"],
                ["fail2ban-client", "status", "sshd"],
                ["apt", "remove", "fail2ban", "-y"],
                ["rm", "-f", self.path_to_jail_config],
            ]
        )