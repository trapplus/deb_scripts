import sys
from app.utils.sysinfo_utils import isRootRunned
from app.interfaces.cli import cli


def main():
    if not isRootRunned() and "--rootless" not in sys.argv:
        raise PermissionError("Permission denied. Run with sudo or use --rootless flag")
    
    if "--api" in sys.argv:
        print("API Mode is not developed yet.")
    else:
        cli.run_interactive_script()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")
    except PermissionError as e:
        print(f"Error: {e}")
        sys.exit(1)