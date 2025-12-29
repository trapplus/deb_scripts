import os
from shutil import which


def isRootRunned() -> bool:
    """
    Определяет, запущен ли скрипт от root

    Returns:
        bool - результат проверки, True: root, False: non root
    """

    __uid: int = os.geteuid()

    if __uid == 0:
        return True
    else:
        return False


def detect_distro() -> str:
    """
    Определяет семейство дистрибутива на котором запущен скрипт по признаку того или инного пакетного менеджера

    Returns:
        str - Distro name, like a Arch, Debian and another. Return unknown if disto cant be detected
    """

    if which("apt") or which("apt-get"):
        return "debian"

    elif which("pacman"):
        return "Arch"

    elif os.path.exists("/etc/openwrt_release") or which("opkg"):
        return "wrt"

    elif which("apk"):
        if os.path.exists("/etc/openwrt_release"):
            return "OpenWrt-snapshot"
        return "Alpine"

    elif which("emerge"):
        return "Gentoo"

    elif which("yum"):
        return "rhel-legacy"

    elif which("dnf"):
        return "rhel"

    elif which("zypper"):
        return "suse"

    else:
        return "Unckown"
