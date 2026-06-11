from models import BallChain
from io_handler import InputHandler, InputError

class Application:
    def __init__(self):
        self.handler = InputHandler()

    def _print_header(self):
        print("\n" + "=" * 60)
        print(" " * 18 + "LINE GAME SOLVER")
        print(" " * 10 + "Алгоритм каскадного уничтожения цепочек")
        print("=" * 60)

    def run(self):
        while True:
            self._print_header()
            print("\nГЛАВНОЕ МЕНЮ:")
            print("  1. Ввести данные вручную (через пробел или запятую)")
            print("  2. Загрузить данные из файла (.txt, .json, .csv)")
            print("  3. Выход из программы")
            print("-" * 60)
            
            choice = input("-> Ваш выбор (1-3): ").strip()

            # Строгая валидация выбора меню
            if choice == '1':
                self._process_console()
            elif choice == '2':
                self._process_file()
            elif choice == '3':
                print("\n[УСПЕХ] Работа программы завершена. Успехов в учебе!\n")
                break
            else:
                print("\n[ОШИБКА] Некорректный выбор. Пожалуйста, введите строго 1, 2 или 3.")
                input("\nНажмите Enter, чтобы продолжить...")

    def _process_console(self):
        print("\n[ИНФО] Подсказка: введите количество шариков, а затем их цвета.")
        print("       Пример: 5 1 3 3 3 2  или  5, 1, 3, 3, 3, 2")
        try:
            data = input("-> Введите данные: ").strip()
            colors = self.handler.parse_input(data)
            self._solve(colors)
        except InputError as e:
            print(f"\n[ОШИБКА] Ввод: {e}")
        input("\nНажмите Enter, чтобы вернуться в меню...")

    def _process_file(self):
        print("\n[ИНФО] Загрузка данных из файла")
        has_file = input("-> У вас уже есть файл с данными? (y/yes - да, любая другая клавиша - создать новый): ").strip().lower()
        
        try:
            if has_file in ['y', 'yes', 'д', 'да', '1']:
                filepath = input("-> Введите имя или путь к файлу (например, data.txt): ").strip()
                data_str = self.handler.read_from_file(filepath)
            else:
                filepath = "auto_generated_data.txt"
                print(f"\n[СИСТЕМА] Попытка создать файл '{filepath}' в текущей папке проекта...")
                
                try:
                    self.handler.create_example_file(filepath)
                    print(f"[УСПЕХ] Файл '{filepath}' успешно создан!")
                    data_str = self.handler.read_from_file(filepath)
                except InputError as create_err:
                    print(f"\n[ОШИБКА] Не удалось создать файл: {create_err}")
                    print("[СОВЕТ] Проверьте права доступа к папке или укажите другой путь.")
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

    def _solve(self, colors: list[int]):
        print("\n[СИСТЕМА] Анализ цепочки...")
        try:
            chain = BallChain(colors)
            total, log = chain.solve_with_log()
            
            print("\n" + "-" * 60)
            print(" ДЕТАЛЬНЫЙ ОТЧЕТ О ВЫЧИСЛЕНИЯХ:")
            print("-" * 60)
            for step_message in log:
                print(step_message)
            print("-" * 60)
        except Exception as e:
            print(f"\n[КРИТИЧЕСКАЯ ОШИБКА] Сбой в алгоритме вычислений: {e}")
        input("\nНажмите Enter, чтобы вернуться в меню...")