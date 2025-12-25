from app.interfaces.interactive import bbr, docker, fail2ban, uv


def run_interactive_script():
    user_input = str(
        input(
            "Выберите скрипт:\n0 - Выход\n1 - BBR\n2 - Docker\n3 - Fail2Ban\n4 - UV\nВыбор:"
        )
    )

    match user_input:
        case "0":
            exit()
        case "1":
            bbr.interactive_run()
        case "2":
            docker.interactive_run()
        case "3":
            fail2ban.interactive_run()
        case "4":
            uv.interactive_run()
        case _:
            print("Неверный ввод")
            run_interactive_script()
