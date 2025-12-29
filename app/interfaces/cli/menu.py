import platform
from subprocess import run

from app.utils import sysinfo_utils


class Menu:
    def __init__(self):
        self.distro = sysinfo_utils.detect_distro()
        self.kernel = platform.release()
        self.hostname = platform.node()

        # Service statuses
        self.bbr_status = "Unknown"
        self.docker_status = "Unknown"
        self.fail2ban_status = "Unknown"
        self.ufw_status = "Unknown"

        self.menu_text = ""
        self.update_status()

    def update_status(self):
        """Update all service statuses"""
        self.bbr_status = self._check_bbr()
        self.docker_status = self._check_service("docker")
        self.fail2ban_status = self._check_service("fail2ban")
        self.ufw_status = self._check_ufw()
        self._build_menu_text()

    def _check_bbr(self):
        """Check BBR status"""
        try:
            result = run(
                ["sysctl", "net.ipv4.tcp_congestion_control"],
                capture_output=True,
                text=True,
            )
            if "bbr" in result.stdout:
                return "Enabled"
            return "Disabled"
        except Exception:
            return "Unknown"

    def _check_service(self, service_name):
        """Check service status (systemd)"""
        try:
            result = run(
                ["systemctl", "is-active", service_name], capture_output=True, text=True
            )
            status = result.stdout.strip()
            if status == "active":
                return "Running"
            return "Stopped"
        except Exception:
            return "Not Installed"

    def _check_ufw(self):
        """Check UFW status"""
        try:
            result = run(["ufw", "status"], capture_output=True, text=True)
            if "Status: active" in result.stdout:
                return "Active"
            return "Inactive"
        except Exception:
            return "Not Installed"

    def _build_menu_text(self):
        """Build menu text"""
        self.menu_text = f"""
╔════════════════════════════════════════════════════════════╗
║          DevOps Automation Scripts v1.0.4                  ║
╚════════════════════════════════════════════════════════════╝

System: {self.distro} | Kernel: {self.kernel} | Host: {self.hostname}
Services: BBR [{self.bbr_status}] | Docker [{self.docker_status}] | Fail2Ban [{self.fail2ban_status}] | UFW [{self.ufw_status}]

────────────────────────────────────────────────────────────

Выберите скрипт:
0 - Выход
1 - BBR
2 - Docker
3 - Fail2Ban
4 - UFW

Выбор: """

    def display(self):
        """Display menu"""
        print(self.menu_text, end="")
