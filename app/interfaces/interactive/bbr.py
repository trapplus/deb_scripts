from app.services.bbr import BBRService


def interactive_run():
    print("BBR manager\nВыберите действие:")
    user_input = str(input(" 0 - Выход\n1 - Включить\n2 - Выключить\nВыбор:"))
    bbr = BBRService()
    match user_input:
        case "0":
            from app.interfaces.interactive.run import run_interactive_script

            run_interactive_script()
        case "1":
            bbr.enable_bbr()
        case "2":
            bbr.disable_bbr()
        case _:
            print("Неверный ввод")
            interactive_run()
