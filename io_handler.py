"""
Модуль обработки ввода-вывода.

Отвечает за чтение данных, валидацию и создание файлов.
"""


class InputError(Exception):
    """
    Исключение.

    Возникающее при ошибках пользовательского
    ввода или работы с файлами.
    """

    pass


class InputHandler:
    """Класс для безопасного получения данных от пользователя или из файлов."""

    @staticmethod
    def parse_input(data_str: str) -> list[int]:
        """
        Парсит строку ввода и валидирует данные шариков.

        Аргументы:
            data_str (str): Строка с количеством и цветами шариков.

        Возвращает:
            list[int]: Список целых чисел, представляющих цвета шариков.

        Исключения:
            InputError: При нарушении формата,
            диапазона значений или логики данных.
        """
        if not data_str or not data_str.strip():
            raise InputError("Ввод не может быть пустым.")

        try:
            clean_str = data_str.replace(',', ' ')
            parts = clean_str.split()

            if not parts:
                raise InputError("Ввод не содержит чисел.")

            n_str = parts[0]
            if not n_str.isdigit():
                raise InputError(
                    f"Кол-во должно быть целым числом, получено: '{n_str}'"
                )

            n = int(n_str)
            if n <= 0:
                raise InputError("Количество шариков должно быть больше 0.")
            if n > 100000:
                raise InputError("Количество шариков превышает 100 000.")

            if len(parts) != n + 1:
                raise InputError(
                    f"Ошибка: заявлено {n} шариков, введено {len(parts) - 1}."
                )

            colors = []
            for i, c_str in enumerate(parts[1:], start=1):
                if not c_str.isdigit():
                    raise InputError(
                        f"Цвет '{c_str}' (позиция {i}) не целое число."
                    )

                c = int(c_str)
                if not (0 <= c <= 9):
                    raise InputError(
                        f"Цвет '{c}' (позиция {i}) вне диапазона 0-9."
                    )
                colors.append(c)

            return colors

        except InputError:
            raise
        except Exception as e:
            raise InputError(f"Критическая ошибка формата данных: {e}")

    def read_from_file(self, filepath: str) -> str:
        """
        Читает и очищает содержимое файла.

        Аргументы:
            filepath (str): Путь к файлу.

        Возвращает:
            str: Очищенное содержимое файла в виде строки.

        Исключения:
            InputError: При отсутствии файла, ошибках прав доступа или формата.
        """
        filepath = filepath.strip()
        if not filepath:
            raise InputError("Имя файла не может быть пустым.")

        invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
        if any(char in filepath for char in invalid_chars):
            raise InputError("Имя файла содержит недопустимые символы.")

        if not (filepath.endswith('.txt') or filepath.endswith('.json')
                or filepath.endswith('.csv')):
            filepath += '.txt'

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            if not content.strip():
                raise InputError("Файл существует, но он абсолютно пуст.")

            return self._clean_content(content)

        except FileNotFoundError:
            raise InputError(f"Файл '{filepath}' не найден.")
        except PermissionError:
            raise InputError(f"Отказано в доступе к файлу '{filepath}'.")
        except IsADirectoryError:
            raise InputError(f"'{filepath}' папка, укажите имя файла.")
        except UnicodeDecodeError:
            raise InputError(f"Файл '{filepath}' содержит нечитаемые символы.")
        except Exception as e:
            raise InputError(f"Непредвиденная ошибка при чтении: {e}")

    def create_example_file(self, filepath: str) -> None:
        """
        Создает файл с примером данных, если он не существует.

        Аргументы:
            filepath (str): Путь для создания файла.

        Исключения:
            InputError: При невозможности создания файла.
        """
        filepath = filepath.strip()
        if not filepath:
            raise InputError("Имя файла для создания не может быть пустым.")

        if not (filepath.endswith('.txt') or filepath.endswith('.json')
                or filepath.endswith('.csv')):
            filepath += '.txt'

        example_data = "10 3 3 2 1 1 1 2 2 3 3"
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(example_data)
        except PermissionError:
            raise InputError("Отказано в доступе."
                  " Запустите от имени администратора.")
        except IsADirectoryError:
            raise InputError("Невозможно создать файл:"
                  " имя совпадает с папкой.")
        except Exception as e:
            raise InputError(f"Не удалось создать файл: {e}")

    @staticmethod
    def _clean_content(content: str) -> str:
        """
        Удаляет символы форматирования, оставляя только числа и пробелы.

        Аргументы:
            content (str): Исходное содержимое файла.

        Возвращает:
            str: Очищенная строка.
        """
        for char in ['{', '}', '[', ']', '"', "'", ':', '\n', '\r']:
            content = content.replace(char, ' ')
        return content.strip()
