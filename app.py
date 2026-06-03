from models import BallChain
from io_handler import InputHandler, InputError


class Application:
    def __init__(self):
        self.handler = InputHandler()

    def run(self):
        while True:
            print("\n=== Игра 'Шарики' ===")
            print("1. Ввод данных из консоли")
            print("2. Ввод данных из файла")
            print("3. Выход")

            choice = input("Выберите действие (1-3): ").strip()

            if choice == '1':
                self._process_console()
            elif choice == '2':
                self._process_file()
            elif choice == '3':
                print("Завершение работы программы.")
                break
            else:
                print("Некорректный выбор. Пожалуйста, введите число от 1 до 3.")

    def _process_console(self):
        try:
            data = input("Введите количество шариков и их цвета через пробел: ")
            colors = self.handler.parse_input(data)
            self._solve(colors)
        except InputError as e:
            print(f"Ошибка ввода: {e}")

    def _process_file(self):
        try:
            filepath = input("Введите путь к файлу (например, input.txt): ").strip()
            data = self.handler.read_from_file(filepath)
            colors = self.handler.parse_input(data)
            self._solve(colors)
        except InputError as e:
            print(f"Ошибка: {e}")

    def _solve(self, colors: list[int]):
        chain = BallChain(colors)
        result = chain.get_destroyed_count()
        print(f"Результат: будет уничтожено {result} шариков.")