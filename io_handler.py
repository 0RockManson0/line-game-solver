class InputError(Exception):
    """Исключение для ошибок пользовательского ввода"""
    pass

class InputHandler:
    @staticmethod
    def parse_input(data_str: str) -> list[int]:
        if not data_str or not data_str.strip():
            raise InputError("Ввод не может быть пустым.")
            
        try:
            clean_str = data_str.replace(',', ' ')
            parts = clean_str.split()
            
            if not parts:
                raise InputError("Ввод не содержит чисел.")
            
            # 1. Валидация количества
            n_str = parts[0]
            if not n_str.isdigit():
                raise InputError(f"Количество шариков должно быть целым положительным числом, получено: '{n_str}'")
            
            n = int(n_str)
            if n <= 0:
                raise InputError("Количество шариков должно быть больше 0.")
            if n > 100000:
                raise InputError("Количество шариков не должно превышать 100 000 (защита от переполнения памяти).")
            
            # 2. Валидация длины массива
            if len(parts) != n + 1:
                raise InputError(f"Несоответствие данных: заявлено {n} шариков, а введено {len(parts) - 1}.")
            
            # 3. Валидация цветов
            colors = []
            for i, c_str in enumerate(parts[1:], start=1):
                if not c_str.isdigit():
                    raise InputError(f"Цвет '{c_str}' (позиция {i}) не является целым положительным числом.")
                
                c = int(c_str)
                if not (0 <= c <= 9):
                    raise InputError(f"Цвет '{c}' (позиция {i}) выходит за допустимый диапазон от 0 до 9.")
                colors.append(c)
            
            return colors
            
        except InputError:
            raise # Пробрасываем наши кастомные ошибки как есть
        except Exception as e:
            raise InputError(f"Критическая ошибка формата данных: {e}")

    def read_from_file(self, filepath: str) -> str:
        filepath = filepath.strip()
        if not filepath:
            raise InputError("Имя файла не может быть пустым.")
            
        # Базовая проверка на недопустимые символы в имени файла (Windows)
        invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
        if any(char in filepath for char in invalid_chars):
            raise InputError("Имя файла содержит недопустимые символы.")

        if not (filepath.endswith('.txt') or filepath.endswith('.json') or filepath.endswith('.csv')):
            filepath += '.txt'
            
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
            if not content.strip():
                raise InputError("Файл существует, но он абсолютно пуст.")
                
            return self._clean_content(content)
            
        except FileNotFoundError:
            raise InputError(f"Файл '{filepath}' не найден. Проверьте имя и расширение.")
        except PermissionError:
            raise InputError(f"Отказано в доступе к файлу '{filepath}'. Возможно, он открыт в другой программе или защищен.")
        except IsADirectoryError:
            raise InputError(f"'{filepath}' является папкой, а не файлом. Укажите полное имя файла (например, data.txt).")
        except UnicodeDecodeError:
            raise InputError(f"Файл '{filepath}' содержит нечитаемые символы (не UTF-8).")
        except Exception as e:
            raise InputError(f"Непредвиденная ошибка при чтении: {e}")

    def create_example_file(self, filepath: str) -> None:
        filepath = filepath.strip()
        if not filepath:
            raise InputError("Имя файла для создания не может быть пустым.")
            
        if not (filepath.endswith('.txt') or filepath.endswith('.json') or filepath.endswith('.csv')):
            filepath += '.txt'
            
        example_data = "10 3 3 2 1 1 1 2 2 3 3"
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(example_data)
        except PermissionError:
            raise InputError("Отказано в доступе. У программы нет прав на запись в эту папку (попробуйте запустить от имени администратора).")
        except IsADirectoryError:
            raise InputError("Невозможно создать файл, так как указанное имя совпадает с существующей папкой.")
        except Exception as e:
            raise InputError(f"Не удалось создать файл: {e}")

    @staticmethod
    def _clean_content(content: str) -> str:
        for char in ['{', '}', '[', ']', '"', "'", ':', '\n', '\r']:
            content = content.replace(char, ' ')
        return content.strip()