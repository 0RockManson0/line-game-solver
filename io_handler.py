class InputError(Exception):
    """Исключение для ошибок пользовательского ввода"""
    pass


class InputHandler:
    @staticmethod
    def parse_input(data_str: str) -> list[int]:
        try:
            parts = data_str.split()
            if not parts:
                raise InputError("Пустой ввод")

            n = int(parts[0])
            if n > 100000:
                raise InputError("Количество шариков не должно превышать 10^5")

            if len(parts) != n + 1:
                raise InputError(f"Ожидалось {n} цветов, получено {len(parts) - 1}")

            colors = [int(x) for x in parts[1:]]
            for c in colors:
                if not (0 <= c <= 9):
                    raise InputError("Цвета должны быть целыми числами от 0 до 9")

            return colors
        except ValueError:
            raise InputError("Ввод должен содержать только целые числа, разделенные пробелами")

    @staticmethod
    def read_from_file(filepath: str) -> str:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except FileNotFoundError:
            raise InputError(f"Файл '{filepath}' не найден")
        except PermissionError:
            raise InputError(f"Нет прав на чтение файла '{filepath}'")
        except Exception as e:
            raise InputError(f"Ошибка чтения файла: {e}")