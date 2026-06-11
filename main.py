"""
Точка входа в приложение Line Game Solver.

Инициализирует и запускает основной цикл приложения с обработкой прерываний.
"""

from app import Application


def main() -> None:
    """Инициализация и запуск приложения с защитой от KeyboardInterrupt."""
    app = Application()
    try:
        app.run()
    except KeyboardInterrupt:
        print("\n\n[УСПЕХ] Работа программы прервана пользователем (Ctrl+C).")


if __name__ == "__main__":
    main()
