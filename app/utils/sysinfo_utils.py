from shutil import which
import os

def defect_distro() -> str:
    """
    Определяет семейство дистрибутива на котором запущен скрипт по признаку того или инного пакетного менеджера

    Returns:
        str - Distro name, like a Arch, Debian and another. Unknown if distro now suported
    """

    if which('apt') or which('apt-get'):
        return 'debian'

    elif which("pacman"):
       return "Arch"

    elif os.path.exists('/etc/openwrt_release') or which('opkg'):
        return 'wrt'

    elif which("apk"):
        if os.path.exists('/etc/openwrt_release'):
            return "OpenWrt-snapshot"
        return "Alpine"

    elif which("emerge"):
       return "Gentoo"

    elif which("yum"):
        return "rhel-legacy"

    elif which("dnf"):
        return "rhel"

    elif which('zypper'):
        return 'suse'

    else:
        return "Unckown"
