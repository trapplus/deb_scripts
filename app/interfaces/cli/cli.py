from app.interfaces.cli.menu import Menu
from app.services.bbr import BBRService
from app.services.docker import DockerService
from app.services.fail2ban import Fail2BanService
from app.services.ufw import UFWService


def run_interactive_script():
    menu = Menu()

    while True:
        menu.update_status()
        menu.display()

        choice = input()

        if choice == "0":
            break
        elif choice == "1":
            bbr_menu()
        elif choice == "2":
            docker_menu()
        elif choice == "3":
            fail2ban_menu()
        elif choice == "4":
            ufw_menu()


def bbr_menu():
    while True:
        print("\n1 - Enable BBR")
        print("2 - Disable BBR")
        print("0 - Назад")

        choice = input("Выбор: ")

        if choice == "0":
            break

        bbr = BBRService.create()

        if choice == "1":
            bbr.enable()
            print("BBR включен")
            input("Press Enter...")
        elif choice == "2":
            bbr.disable()
            print("BBR выключен")
            input("Press Enter...")


def docker_menu():
    while True:
        print("\n1 - Install Docker")
        print("2 - Uninstall Docker")
        print("0 - Назад")

        choice = input("Выбор: ")

        if choice == "0":
            break

        docker = DockerService.create()

        if choice == "1":
            docker.install()
            print("Docker установлен")
            input("Press Enter...")
        elif choice == "2":
            docker.uninstall()
            print("Docker удален")
            input("Press Enter...")


def fail2ban_menu():
    while True:
        print("\n1 - Install Fail2Ban")
        print("2 - Uninstall Fail2Ban")
        print("0 - Назад")

        choice = input("Выбор: ")

        if choice == "0":
            break

        fail2ban = Fail2BanService.create()

        if choice == "1":
            fail2ban.install()
            print("Fail2Ban установлен")
            input("Press Enter...")
        elif choice == "2":
            fail2ban.uninstall()
            print("Fail2Ban удален")
            input("Press Enter...")


def ufw_menu():
    while True:
        print("\n1 - Install UFW")
        print("2 - Uninstall UFW")
        print("0 - Назад")

        choice = input("Выбор: ")

        if choice == "0":
            break

        ufw = UFWService.create()

        if choice == "1":
            ufw.install()
            print("UFW установлен")
            input("Press Enter...")
        elif choice == "2":
            ufw.uninstall()
            print("UFW удален")
            input("Press Enter...")
