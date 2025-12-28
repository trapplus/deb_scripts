import os

from app.interfaces.cli.run import interactiveCLI


def main():
    global cli

    cli_global = interactiveCLI()

    cli_global.run_interactive_script()


if __name__ == "__main__":
    try:
        os.system("clear")
        main()
    except KeyboardInterrupt:
        print("\nВыход...")
