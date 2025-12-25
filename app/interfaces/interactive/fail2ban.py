from app.services.fail2ban import Fail2BanService


def interactive_run():
    print("Fail2Ban manager\nВыберете действие:")
    user_input = str(input("0 - Выход\n1 - Установить\n2 - Удалить\nВыбор:"))
    fail2ban = Fail2BanService()
    match user_input:
        case "0":
            from app.interfaces.interactive.run import run_interactive_script

            run_interactive_script()
        case "1":
            fail2ban.install_fail2ban()
        case "2":
            fail2ban.uninstall_fail2ban()
        case _:
            print("Неверный ввод")
            interactive_run()
