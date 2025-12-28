import time
from subprocess import run

from app.services.ufw import UFWService
from app.utils.subprocess_utils import run_commands


class DebianUFWService(UFWService):
    def __init__(self):
        super().__init__()
        self.package_manager = "apt"

    def install(self):
        print("Installing UFW for Debian/Ubuntu...")

        run_commands([[self.package_manager, "update"]])
        run_commands([[self.package_manager, "install", "ufw", "-y"]])

        run_commands(
            [
                ["ufw", "default", "deny", "incoming"],
                ["ufw", "default", "allow", "outgoing"],
            ]
        )

        for action, port, description in self.default_rules:
            print(f"Adding rule: {action} {port} ({description})")
            run_commands([["ufw", action, port, "comment", description]])

        run_commands([["ufw", "--force", "enable"]])

        self._wait_for_status("active")

        run_commands(
            [
                ["ufw", "status", "verbose"],
                ["systemctl", "status", "ufw"],
            ]
        )

        print("UFW successfully installed and configured")

    def uninstall(self):
        print("Uninstalling UFW for Debian/Ubuntu...")

        run_commands([["ufw", "--force", "disable"]])

        self._wait_for_status("inactive")

        run_commands(
            [
                ["systemctl", "stop", "ufw"],
                ["systemctl", "disable", "ufw"],
            ]
        )

        run_commands([[self.package_manager, "remove", "ufw", "-y"]])
        run_commands([[self.package_manager, "autoremove", "-y"]])

        print("UFW successfully uninstalled")

    def _check_service_status(self, expected_status: str) -> bool:
        result = run(["systemctl", "is-active", "ufw"], text=True, capture_output=True)
        return result.stdout.strip() == expected_status

    def _wait_for_status(self, expected_status: str, timeout: int = 10):
        start_time = time.time()
        while time.time() - start_time < timeout:
            if self._check_service_status(expected_status):
                return
            time.sleep(0.5)
        print(f"Warning: failed to reach status '{expected_status}'")
