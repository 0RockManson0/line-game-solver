"""
Точка входа в приложение Line Game Solver.

Инициализирует и запускает основной цикл приложения.
"""

from app import Application


def main() -> None:
    """Инициализация и запуск приложения."""
    app = Application()
    app.run()


if __name__ == "__main__":
    main()
