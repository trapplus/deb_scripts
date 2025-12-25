from app.services.uv import UVService


def interactive_run():
    print("UV manager\nВыберите действие:")
    user_input = str(input("0 - Выход\n1 - Установить\n2 - Удалить\nВыбор:"))
    app = UVService()
    match user_input:
        case "0":
            from app.interfaces.interactive.run import run_interactive_script

            run_interactive_script()
        case "1":
            app.install_uv()
        case "2":
            app.uninstall_uv()
        case _:
            print("Неверный ввод")
            interactive_run()
