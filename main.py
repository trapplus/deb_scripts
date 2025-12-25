from app.interfaces.cli.run import interactiveCLI

def main():
    global cli

    cli_global = interactiveCLI()

    cli_global.run_interactive_script()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Выход...")
