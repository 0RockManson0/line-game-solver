"""
Модуль бизнес-логики.

Содержит класс для представления цепочки
шариков и оптимизированного алгоритма их удаления.
"""

from typing import List, Tuple


class BallChain:
    """Класс, управляющий состоянием линии шариков."""

    def __init__(self, balls: List[int]) -> None:
        """Инциализация линии шариков."""
        self.balls = balls.copy() if balls else []

    def solve_with_log(self) -> Tuple[int, List[str]]:
        """
        Выполняет каскадное удаление цепочек из 3 и более шариков.

        Работает с локальной копией.
        """
        working_balls = self.balls.copy()
        total_destroyed = 0
        log = []
        step = 1

        if not working_balls:
            log.append("  [ИНФО] Список шариков пуст. Нечего уничтожать.")
            return 0, log

        i = 0
        while i < len(working_balls):
            count = 1
            while (i + count < len(working_balls) and
                    working_balls[i + count] == working_balls[i]):
                count += 1

            if count >= 3:
                color = working_balls[i]
                del working_balls[i: i + count]
                total_destroyed += count
                log.append(
                    f"  [ШАГ {step}] Найдена цепочка из {count} "
                    f"шариков цвета {color}. Они уничтожены."
                )
                step += 1
                # Откат индекса для проверки возможного образования новой цепочки 
                # после сдвига элементов. max(0, ...) предотвращает отрицательную индексацию.
                i = max(0, i - 2)
            else:
                i += count

        if total_destroyed == 0:
            log.append("  [ИНФО] Цепочки из 3 и более шариков не найдены.")
        else:
            log.append(f"  [ИТОГ] Всего уничтожено шариков: {total_destroyed}")

        return total_destroyed, log
