# 🐍 DevOps Automation Scripts

![GitHub](https://img.shields.io/github/license/thegrayfoxxx/deb_scripts?color=blue)
![Python](https://img.shields.io/badge/Python-3.12%2B-blue?logo=python)
![UV](https://img.shields.io/badge/UV-0.6.0%2B-orange?logo=python)

**Набор Python-скриптов для автоматизации DevOps-задач в Linux-окружении**
Упрощение настройки серверов, оптимизации сетевых параметров и безопасности.

---

## 🚀 Основные возможности

- **Автоматизация настройки сервера**: BBR, Fail2Ban, Docker и другие оптимизации
- **DEB**: поддержка Debian, Ubuntu и производных дистрибутивов
- **ARCH**: поддержка Arch и производных дистрибутивов
- **Экосистема инструментов**:
  - UV для управления зависимостями
  - Pylint Для контроля качества кода 

---

## ⚙️ Быстрый старт

### Предварительные требования
- Python 3.12+
- Git
- POSIX-совместимая оболочка (bash/zsh)

### Установка и запуск
```bash
curl -fsSL https://raw.githubusercontent.com/trapplus/deb_scripts/master/install.sh | bash
```

---

## 📂 Структура проекта
```
deb_scripts/
deb_scripts/
├── app/
│   ├── interfaces/
│   │   ├── api/                    # API интерфейс (в разработке)
│   │   └── cli/                    # CLI интерфейс
│   │       └── run.py              # Точка входа CLI
│   │
│   ├── services/                   # Бизнес-логика сервисов
│   │   ├── bbr.py                  # Сервис BBR конгестии
│   │   ├── docker.py               # Сервис Docker
│   │   ├── fail2ban.py             # Сервис Fail2Ban
│   │   │
│   │   └── distro/                 # Реализации для дистрибутивов
│   │       ├── arch/               # Arch Linux
│   │       │   ├── bbr.py
│   │       │   ├── docker.py
│   │       │   └── fail2ban.py
│   │       │
│   │       ├── debian/             # Debian/Ubuntu
│   │       │   ├── bbr.py
│   │       │   ├── docker.py
│   │       │   └── fail2ban.py
│   │       │
│   │       └── wrt/                # OpenWrt
│   │           ├── bbr.py
│   │           ├── docker.py
│   │           └── fail2ban.py
│   │
│   └── utils/                      # Утилиты
│       ├── __init__.py
│       ├── subprocess_utils.py     # Работа с процессами
│       └── sysinfo_utils.py        # Информация о системе
│
├── main.py                         # Главная точка входа
├── pyproject.toml                  # Конфигурация проекта (uv)
├── uv.lock                         # Lockfile зависимостей
├── install.sh                      # Установочный скрипт
├── README.md                       # Документация
└── LICENSE                         # Лицензия
```
---

## 🗓️ Планы
### Выполнено:
1. Поддержка Arch Linux и ее производных.


### В выполнения
1. Реализовать поддержку для OpenWrt и ее производных, Alpine, .
2. Улучшение CLI-Интерфейса для более приятного UX.
3. Дополнительный функционал включающий в себя такие скрипты для установки 3X-UI, Zapret и podkop для OpenWrt.

---
## ⚠️ Безопасность

**Важно!** Скрипты выполняют системные изменения.

---

## 📜 Лицензия

MIT License © 2025 thegrayfoxxx - original

MIT License © 2025 trapplus - forked
