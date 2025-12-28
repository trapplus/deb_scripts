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
    print_step "Проверка uv..."

    if check_command uv; then
        print_success "uv уже установлен"
        return 0
    fi

    print_step "Установка uv..."
    if curl -fsSL "$UV_INSTALL_URL" | sh; then
        print_success "uv успешно установлен"

        export PATH="$HOME/.cargo/bin:$PATH"

        return 0
    else
        print_error "Не удалось установить uv"
        return 1
    fi
}

clone_repository() {
    print_step "Клонирование репозитория..."

    if [ -d "$INSTALL_DIR" ]; then
        print_info "Директория $INSTALL_DIR уже существует"
        read -p "$(echo -e ${YELLOW}Удалить и переустановить? [y/N]:${NC} )" -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            rm -rf "$INSTALL_DIR"
        else
            print_info "Пропускаем клонирование"
            return 0
        fi
    fi

    if ! check_command git; then
        print_error "Git не установлен. Установи git и попробуй снова"
        exit 1
    fi

    if git clone "$REPO_URL" "$INSTALL_DIR"; then
        print_success "Репозиторий склонирован в $INSTALL_DIR"
        return 0
    else
        print_error "Не удалось склонировать репозиторий"
        return 1
    fi
}

run_script() {
    print_step "Запуск скрипта..."

    cd "$INSTALL_DIR"

    if uv run main.py; then
        print_success "Скрипт выполнен успешно"
        return 0
    else
        print_error "Ошибка при выполнении скрипта"
        return 1
    fi
}

print_manual_run() {
    echo
    echo -e "${CYAN}${BOLD}════════════════════════════════════════${NC}"
    echo -e "${GREEN}${BOLD}   Установка завершена!${NC}"
    echo -e "${CYAN}${BOLD}════════════════════════════════════════${NC}"
    echo
    echo -e "${BOLD}Для запуска скрипта выполни:${NC}"
    echo
    echo -e "  ${MAGENTA}cd $INSTALL_DIR && uv run main.py${NC}"
    echo
    echo -e "${YELLOW}💡 Совет:${NC} Добавь алиас в ~/.bashrc или ~/.zshrc:"
    echo
    echo -e "  ${CYAN}alias deb='cd $INSTALL_DIR && uv run main.py'${NC}"
    echo
    echo -e "${CYAN}${BOLD}════════════════════════════════════════════════════${NC}"
}

# methods

main() {
    clear
    print_header

    if ! install_uv; then
        exit 1
    fi

    echo

    if ! clone_repository; then
        exit 1
    fi

    echo

    read -p "$(echo -e ${GREEN}${BOLD}Запустить скрипт сейчас? [Y/n]:${NC} )" -n 1 -r
    echo
    echo

    if [[ $REPLY =~ ^[Nn]$ ]]; then
        print_manual_run
    else
        if run_script; then
            echo
            print_success "Готово!"
            echo
            print_info "Для повторного запуска используй:"
            echo -e "  ${MAGENTA}cd $INSTALL_DIR && uv run main.py${NC}"
            echo
        else
            echo
            print_manual_run
        fi
    fi

    if [[ ! ":$PATH:" == *":$HOME/.cargo/bin:"* ]]; then
        echo
        print_info "Возможно, потребуется перезагрузить shell или выполнить:"
        echo -e "  ${CYAN}source ~/.bashrc${NC}  ${YELLOW}# или${NC}  ${CYAN}source ~/.zshrc${NC}"
        echo
    fi
}

main
