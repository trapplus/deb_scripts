import os
from platform import system

from app.services.bbr import BBRService
from app.services.docker import DockerService
from app.services.fail2ban import Fail2BanService


class interactiveCLI:
    def __init__(self) -> None:
        self.bbr = BBRService()
        self.docker = DockerService()
        self.fail2ban = Fail2BanService()

        self.system: str = system()

    def run_interactive_script(self) -> None:
        user_input: str = str(
            input(
                "Выберите скрипт:\n0 - Выход\n1 - BBR\n2 - Docker\n3 - Fail2Ban\nВыбор:"
            )
        )

        match user_input:
            case "0":
                exit()
            case "1":
                os.system("clear")
                self.bbr_interactive_run()
            case "2":
                os.system("clear")
                self.docker_interactive_run()
            case "3":
                os.system("clear")
                self.fail2ban_interactive_run()
            case _:
                os.system("clear")
                print("Неверный ввод")
                self.run_interactive_script()

    def bbr_interactive_run(self):
        print("BBR manager\nВыберите действие:")
        user_input = str(input("0 - Выход\n1 - Включить\n2 - Выключить\nВыбор:"))
        match user_input:
            case "0":
                self.run_interactive_script()
            case "1":
                self.bbr.enable()
            case "2":
                self.bbr.disable()
            case _:
                print("Неверный ввод")
                self.bbr_interactive_run()

    def fail2ban_interactive_run(self):
        print("Fail2Ban manager\nВыберете действие:")
        user_input = str(input("0 - Выход\n1 - Установить\n2 - Удалить\nВыбор:"))

        match user_input:
            case "0":  # undo step
                self.run_interactive_script()
            case "1":
                self.fail2ban.install()
            case "2":
                self.fail2ban.uninstall()
            case _:
                print("Неверный ввод")
                # overload
                self.fail2ban_interactive_run()

    def docker_interactive_run(self):
        print("Docker manager\nВыберите действие:")
        user_input = str(input("0 - Выход\n1 - Установить\n2 - Удалить\nВыбор:"))
        match user_input:
            case "0":
                self.run_interactive_script()
            case "1":
                self.docker.install()
            case "2":
                self.docker.uninstall()
            case _:
                print("Неверный ввод")
                # overload
                self.docker_interactive_run()
