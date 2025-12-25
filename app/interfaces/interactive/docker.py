from app.services.docker import DockerService


def interactive_run():
    print("Docker manager\nВыберите действие:")
    user_input = str(input("0 - Выход\n1 - Установить\n2 - Удалить\nВыбор:"))
    docker = DockerService()
    match user_input:
        case "0":
            from app.interfaces.interactive.run import run_interactive_script

            run_interactive_script()
        case "1":
            docker.install_docker()
        case "2":
            docker.uninstall_docker()
        case _:
            print("Неверный ввод")
            interactive_run()
