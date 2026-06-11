"""
Модуль обработки ввода-вывода.
Отвечает за чтение данных, строгую валидацию и безопасную работу с файлами.
"""

from typing import List

MAX_BALLS = 100_000
MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10 МБ для защиты от DoS (F-03)


class InputError(Exception):
    """Исключение, возникающее при ошибках пользовательского ввода или работы с файлами."""
    pass


class InputHandler:
    """
    Класс для безопасного получения и проверки данных от пользователя или из файлов.
    """

    @staticmethod
    def _validate_filepath(filepath: str) -> str:
        """
        Проверяет и нормализует путь к файлу, защищая от Directory Traversal (F-01).
        """
        filepath = filepath.strip()
        if not filepath:
            raise InputError("Имя файла не может быть пустым.")
            
        invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
        if any(char in filepath for char in invalid_chars):
            raise InputError("Имя файла содержит недопустимые символы.")

        # Исправление F-08: Убираем ложную поддержку JSON/CSV, так как без библиотек 
        # их полноценный парсинг невозможен, а грязный хак недопустим.
        if not filepath.endswith('.txt'):
            filepath += '.txt'
            
        return filepath

    def parse_input(self, data_str: str) -> List[int]:
        """
        Парсит строку ввода и валидирует данные шариков.
        """
        if not data_str or not data_str.strip():
            raise InputError("Ввод не может быть пустым.")
            
        clean_str = data_str.replace(',', ' ')
        parts = clean_str.split()
        
        if not parts:
            raise InputError("Ввод не содержит чисел.")
        
        n_str = parts[0]
        if not n_str.isdigit():
            raise InputError(f"Количество должно быть целым числом, получено: '{n_str}'")
        
        n = int(n_str)
        if n <= 0:
            raise InputError("Количество шариков должно быть больше 0.")
        if n > MAX_BALLS:
            raise InputError(f"Количество шариков превышает лимит ({MAX_BALLS}).")
        
        if len(parts) != n + 1:
            raise InputError(f"Несоответствие: заявлено {n} шариков, введено {len(parts) - 1}.")
        
        colors = []
        for i, c_str in enumerate(parts[1:], start=1):
            if not c_str.isdigit():
                raise InputError(f"Цвет '{c_str}' (позиция {i}) не является целым числом.")
            
            c = int(c_str)
            if not (0 <= c <= 9):
                raise InputError(f"Цвет '{c}' (позиция {i}) вне допустимого диапазона 0-9.")
            colors.append(c)
        
        return colors

    def read_from_file(self, filepath: str) -> str:
        """
        Читает содержимое файла с защитой от переполнения памяти (DoS).
        """
        safe_path = self._validate_filepath(filepath)
        
        try:
            content = ""
            with open(safe_path, 'r', encoding='utf-8') as f:
                while True:
                    chunk = f.read(1024 * 1024)  # Читаем чанками по 1 МБ (F-03)
                    if not chunk:
                        break
                    content += chunk
                    if len(content.encode('utf-8')) > MAX_FILE_SIZE_BYTES:
                        raise InputError("Файл слишком большой (максимум 10 МБ).")
                
            if not content.strip():
                raise InputError("Файл существует, но он абсолютно пуст.")
                
            return self._clean_content(content)
            
        except FileNotFoundError:
            raise InputError(f"Файл '{safe_path}' не найден.")
        except PermissionError:
            raise InputError(f"Отказано в доступе к файлу '{safe_path}'.")
        except IsADirectoryError:
            raise InputError(f"'{safe_path}' является папкой, укажите имя файла.")
        except UnicodeDecodeError:
            raise InputError(f"Файл '{safe_path}' содержит нечитаемые символы.")

    def create_example_file(self, filepath: str) -> None:
        """
        Создает файл с примером данных, используя ту же строгую валидацию пути (F-01).
        """
        safe_path = self._validate_filepath(filepath)
        example_data = "10 3 3 2 1 1 1 2 2 3 3"
        
        try:
            with open(safe_path, 'w', encoding='utf-8') as f:
                f.write(example_data)
        except PermissionError:
            raise InputError("Отказано в доступе. Запустите программу от имени администратора.")
        except IsADirectoryError:
            raise InputError("Невозможно создать файл: имя совпадает с существующей папкой.")

    @staticmethod
    def _clean_content(content: str) -> str:
        """Удаляет символы переноса строки, оставляя только числа и пробелы."""
        return content.replace('\n', ' ').replace('\r', ' ').strip()