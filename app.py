"""
Модуль управления приложением.

Содержит класс для организации циклического
меню и взаимодействия с пользователем.
"""

from models import BallChain
from io_handler import InputHandler, InputError


class Application:
    """Главный класс приложения."""

    def __init__(self) -> None:
        """Инциализация обработчика."""
        self.handler = InputHandler()

    def _print_header(self) -> None:
        """Выводит заголовок программы в консоль."""
        print("\n" + "=" * 60)
        print(" " * 18 + "LINE GAME SOLVER")
        print(" " * 10 + "Алгоритм каскадного уничтожения цепочек")
        print("=" * 60)

    def run(self) -> None:
        """Запускает основной циклический цикл приложения."""
        while True:
            self._print_header()
            print("\nГЛАВНОЕ МЕНЮ:")
            print("  1. Ввести данные вручную")
            print("  2. Загрузить данные из файла (.txt)")
            print("  3. Выход из программы")
            print("-" * 60)

            choice = input("-> Ваш выбор (1-3): ").strip()

            if choice == '1':
                self._process_console()
            elif choice == '2':
                self._process_file()
            elif choice == '3':
                print("\n[УСПЕХ] Работа программы завершена.\n")
                break
            else:
                print("\n[ОШИБКА] Некорректный выбор. Введите 1, 2 или 3.")
                input("\nНажмите Enter, чтобы продолжить...")

    def _process_console(self) -> None:
        """Обрабатывает сценарий ручного ввода данных пользователем."""
        print("\n[ИНФО] Пример: 5 1 3 3 3 2  или  5, 1, 3, 3, 3, 2")
        try:
            data = input("-> Введите данные: ").strip()
            colors = self.handler.parse_input(data)
            self._solve(colors)
        except InputError as e:
            print(f"\n[ОШИБКА] Ввод: {e}")
        input("\nНажмите Enter, чтобы вернуться в меню...")

    def _process_file(self) -> None:
        """Обрабатывает сценарий загрузки данных из файла или его создания."""
        print("\n[ИНФО] Загрузка данных из файла")
        has_file = input(
            "-> Файл уже существует? (y/yes - да, иначе будет создан новый): "
        ).strip().lower()

        try:
            if has_file in ['y', 'yes', 'д', 'да', '1']:
                filepath = input("Введите имя файла: ").strip()
                data_str = self.handler.read_from_file(filepath)
            else:
                filepath = "auto_generated_data.txt"
                print(f"\n[СИСТЕМА] Создание файла '{filepath}'...")

                try:
                    self.handler.create_example_file(filepath)
                    print(f"[УСПЕХ] Файл '{filepath}' успешно создан!")
                    data_str = self.handler.read_from_file(filepath)
                except InputError as create_err:
                    print(f"\n[ОШИБКА] Не удалось создать файл: {create_err}")
                    input("\nНажмите Enter, чтобы вернуться в меню...")
                    return

            colors = self.handler.parse_input(data_str)
            formatted_colors = " ".join(map(str, colors))

            print("\n" + "=" * 60)
            print(" ОТЧЕТ О ЗАГРУЗКЕ ДАННЫХ:")
            print(f" * Файл: {filepath}")
            print(f" * Всего шариков: {len(colors)}")
            print(f" * Исходная последовательность: {formatted_colors}")
            print("=" * 60)

            self._solve(colors)

        except InputError as e:
            print(f"\n[ОШИБКА] {e}")
            input("\nНажмите Enter, чтобы вернуться в меню...")

    def _solve(self, colors: list[int]) -> None:
        """Запускает алгоритм решения задачи и выводит детальный отчет."""
        print("\n[СИСТЕМА] Анализ цепочки...")
        chain = BallChain(colors)
        total, log = chain.solve_with_log()
        print("\n" + "-" * 60)
        print(" ДЕТАЛЬНЫЙ ОТЧЕТ О ВЫЧИСЛЕНИЯХ:")
        print("-" * 60)
        for step_message in log:
            print(step_message)
        print("-" * 60)
