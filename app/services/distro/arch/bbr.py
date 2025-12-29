import time

from app.services.bbr import BBRService
from app.utils.subprocess_utils import run_commands


class ArchBBRService(BBRService):
    def enable(self):
        with open(self.path_to_sysctl_config, "a", encoding="utf-8") as f:
            f.write(self.bbr_config)
        run_commands([["sysctl", "-p"]])
        time.sleep(1)
        run_commands(
            [
                ["sysctl", "net.ipv4.tcp_congestion_control"],
                ["sysctl", "net.core.default_qdisc"],
            ]
        )

    def disable(self):
        with open(self.path_to_sysctl_config, "r", encoding="utf-8") as f:
            lines = f.readlines()

        filtered_lines = []
        for line in lines:
            if not (
                line.startswith("net.ipv4.tcp_congestion_control")
                or line.startswith("net.core.default_qdisc")
            ):
                filtered_lines.append(line)

        with open(self.path_to_sysctl_config, "w", encoding="utf-8") as f:
            f.writelines(filtered_lines)

        run_commands(
            [
                ["sysctl", "net.ipv4.tcp_congestion_control=cubic"],
                ["sysctl", "net.core.default_qdisc=fq_codel"],
                ["sysctl", "net.ipv4.tcp_congestion_control"],
                ["sysctl", "net.core.default_qdisc"],
            ]
        )
