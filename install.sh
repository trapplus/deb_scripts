#!/bin/bash
set -e

# Config
REPO_URL="https://github.com/trapplus/deb_scripts.git"
UV_INSTALL_URL="https://astral.sh/uv/install.sh"
INSTALL_DIR="$HOME/deb_scripts"
REPO_NAME="deb_scripts"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'
BOLD='\033[1m'

print_header() {
    echo -e "${CYAN}${BOLD}"
    echo "  ╔════════════════════════════════════════╗"
    echo "  ║         deb_scripts Installer          ║"
    echo "  ╚════════════════════════════════════════╝"
    echo -e "${NC}"
}

print_step() {
    echo -e "${BLUE}▶${NC} ${BOLD}$1${NC}"
}

print_success() {
    echo -e "${GREEN}✔${NC} $1"
}

print_error() {
    echo -e "${RED}✖${NC} $1"
}

print_info() {
    echo -e "${YELLOW}ℹ${NC} $1"
}

check_command() {
    if command -v "$1" &> /dev/null; then
        return 0
    else
        return 1
    fi
}

install_uv() {
    print_step "Checking uv installation..."

    if check_command uv; then
        print_success "uv already installed"
        return 0
    fi

    print_step "Installing uv..."
    if curl -fsSL "$UV_INSTALL_URL" | sh < /dev/null; then
        print_success "uv successfully installed"
        export PATH="$HOME/.cargo/bin:$PATH"
        return 0
    else
        print_error "Failed to install uv"
        return 1
    fi
}

setup_repository() {
    if [ -d "$INSTALL_DIR" ]; then
        print_info "Repository already exists at $INSTALL_DIR"
        read -p "$(echo -e ${YELLOW}Update scripts? [Y/n]:${NC} )" -n 1 -r
        echo
        
        if [[ $REPLY =~ ^[Nn]$ ]]; then
            print_info "Skipping update, using existing version"
            return 0
        fi
        
        print_step "Updating repository..."
        cd "$INSTALL_DIR"
        
        if git pull origin master < /dev/null; then
            print_success "Repository updated successfully"
            return 0
        else
            print_error "Failed to update repository"
            return 1
        fi
    else
        print_step "Cloning repository..."
        
        if ! check_command git; then
            print_error "Git is not installed. Please install git and try again"
            exit 1
        fi
        
        if git clone "$REPO_URL" "$INSTALL_DIR" < /dev/null; then
            print_success "Repository cloned to $INSTALL_DIR"
            return 0
        else
            print_error "Failed to clone repository"
            return 1
        fi
    fi
}

install_dependencies() {
    print_step "Installing dependencies..."
    
    cd "$INSTALL_DIR"
    
    if uv sync < /dev/null; then
        print_success "Dependencies installed successfully"
        return 0
    else
        print_error "Failed to install dependencies"
        return 1
    fi
}

run_script() {
    print_step "Running script..."
    
    cd "$INSTALL_DIR"
    
    if uv run main.py; then
        print_success "Script executed successfully"
        return 0
    else
        print_error "Error executing script"
        return 1
    fi
}

print_manual_run() {
    echo
    echo -e "${CYAN}${BOLD}════════════════════════════════════════${NC}"
    echo -e "${GREEN}${BOLD}   Installation completed!${NC}"
    echo -e "${CYAN}${BOLD}════════════════════════════════════════${NC}"
    echo
    echo -e "${BOLD}To run the script execute:${NC}"
    echo
    echo -e "  ${MAGENTA}cd $INSTALL_DIR && uv run main.py${NC}"
    echo
    echo -e "${YELLOW}Tip:${NC} Add alias to ~/.bashrc or ~/.zshrc:"
    echo
    echo -e "  ${CYAN}alias deb='cd $INSTALL_DIR && uv run main.py'${NC}"
    echo
    echo -e "${CYAN}${BOLD}════════════════════════════════════════${NC}"
}

main() {
    # Redirect stdin to /dev/tty if running through pipe (curl | bash)
    if [ ! -t 0 ]; then
        exec < /dev/tty
    fi
    
    clear
    print_header

    if ! install_uv; then
        exit 1
    fi

    echo

    if ! setup_repository; then
        exit 1
    fi

    echo

    if ! install_dependencies; then
        exit 1
    fi

    echo

    read -p "$(echo -e ${GREEN}${BOLD}Run script now? [Y/n]:${NC} )" -n 1 -r
    echo
    echo

    if [[ $REPLY =~ ^[Nn]$ ]]; then
        print_manual_run
    else
        if run_script; then
            echo
            print_success "Done!"
            echo
            print_info "To run again use:"
            echo -e "  ${MAGENTA}cd $INSTALL_DIR && uv run main.py${NC}"
            echo
        else
            echo
            print_manual_run
        fi
    fi

    if [[ ! ":$PATH:" == *":$HOME/.cargo/bin:"* ]]; then
        echo
        print_info "You may need to reload shell or run:"
        echo -e "  ${CYAN}source ~/.bashrc${NC}  ${YELLOW}or${NC}  ${CYAN}source ~/.zshrc${NC}"
        echo
    fi
}

main