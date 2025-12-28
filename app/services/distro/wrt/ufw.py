import time
from subprocess import run

from app.services.ufw import UFWService
from app.utils.subprocess_utils import run_commands


class WrtUFWService(UFWService):
    def __init__(self):
        super().__init__()

    def install(self):
        print("OpenWrt uses built-in firewall")
        print("Configuring firewall for OpenWrt...")

        fw_version = self._detect_firewall_version()

        if fw_version == "fw4":
            self._configure_fw4()
        else:
            self._configure_fw3()

        run_commands([["/etc/init.d/firewall", "restart"]])

        self._wait_for_status("running")

        run_commands(
            [
                ["/etc/init.d/firewall", "status"],
                ["iptables", "-L", "-n", "-v"],
            ]
        )

        print("Firewall successfully configured")

    def uninstall(self):
        print("Cannot remove built-in OpenWrt firewall")
        print("Resetting firewall to default settings...")

        run_commands(
            [
                ["uci", "revert", "firewall"],
                ["uci", "commit", "firewall"],
                ["/etc/init.d/firewall", "restart"],
            ]
        )

        print("Firewall reset to default settings")

    def _detect_firewall_version(self) -> str:
        result = run(["which", "fw4"], capture_output=True)
        return "fw4" if result.returncode == 0 else "fw3"

    def _configure_fw3(self):
        print("Configuring fw3...")

        commands = [
            ["uci", "set", "firewall.ssh=rule"],
            ["uci", "set", "firewall.ssh.name=Allow-SSH"],
            ["uci", "set", "firewall.ssh.src=wan"],
            ["uci", "set", "firewall.ssh.proto=tcp"],
            ["uci", "set", "firewall.ssh.dest_port=22"],
            ["uci", "set", "firewall.ssh.target=ACCEPT"],
            ["uci", "set", "firewall.http=rule"],
            ["uci", "set", "firewall.http.name=Allow-HTTP"],
            ["uci", "set", "firewall.http.src=wan"],
            ["uci", "set", "firewall.http.proto=tcp"],
            ["uci", "set", "firewall.http.dest_port=80"],
            ["uci", "set", "firewall.http.target=ACCEPT"],
            ["uci", "set", "firewall.https=rule"],
            ["uci", "set", "firewall.https.name=Allow-HTTPS"],
            ["uci", "set", "firewall.https.src=wan"],
            ["uci", "set", "firewall.https.proto=tcp"],
            ["uci", "set", "firewall.https.dest_port=443"],
            ["uci", "set", "firewall.https.target=ACCEPT"],
            ["uci", "commit", "firewall"],
        ]

        run_commands(commands)

    def _configure_fw4(self):
        print("Configuring fw4...")
        self._configure_fw3()

    def _check_service_status(self, expected_status: str) -> bool:
        result = run(["/etc/init.d/firewall", "status"], capture_output=True, text=True)
        if expected_status == "running":
            return result.returncode == 0
        else:
            return result.returncode != 0

    def _wait_for_status(self, expected_status: str, timeout: int = 10):
        start_time = time.time()
        while time.time() - start_time < timeout:
            if self._check_service_status(expected_status):
                return
            time.sleep(0.5)
        print(f"Warning: failed to reach status '{expected_status}'")
