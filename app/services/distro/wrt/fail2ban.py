import time
from subprocess import run
from app.utils.subprocess_utils import run_commands
from app.services.fail2ban import Fail2BanService


class WrtFail2BanService(Fail2BanService):
    def install(self):
        run_commands([["opkg", "update"]])
        run_commands([["opkg", "install", "fail2ban"]])
        with open(self.path_to_jail_config, "w", encoding="utf-8") as f:
            f.write(self.jail_str_config)
        run_commands(
            [
                ["/etc/init.d/fail2ban", "enable"],
                ["/etc/init.d/fail2ban", "restart"],
            ]
        )
        status_service = ""
        while status_service != "running":
            result = run(
                ["/etc/init.d/fail2ban", "status"], capture_output=True, text=True
            )
            status_service = "running" if result.returncode == 0 else "stopped"
            time.sleep(0.5)
        run_commands(
            [
                ["/etc/init.d/fail2ban", "status"],
                ["fail2ban-client", "status", "sshd"],
            ]
        )
    
    def uninstall(self):
        run_commands(
            [
                ["/etc/init.d/fail2ban", "disable"],
                ["/etc/init.d/fail2ban", "stop"],
            ]
        )
        status_service = ""
        while status_service != "stopped":
            result = run(
                ["/etc/init.d/fail2ban", "status"], capture_output=True, text=True
            )
            status_service = "stopped" if result.returncode != 0 else "running"
            time.sleep(0.5)
        run_commands(
            [
                ["/etc/init.d/fail2ban", "status"],
                ["fail2ban-client", "status", "sshd"],
                ["opkg", "remove", "fail2ban"],
                ["rm", "-f", self.path_to_jail_config],
            ]
        )