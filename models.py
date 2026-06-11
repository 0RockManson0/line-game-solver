class BallChain:
    def __init__(self, balls: list[int]):
        if not balls:
            self.balls = []
        else:
            self.balls = balls.copy()

    def solve_with_log(self) -> tuple[int, list[str]]:
        total_destroyed = 0
        log = []
        step = 1
        
        if not self.balls:
            log.append("  [ИНФО] Список шариков пуст. Нечего уничтожать.")
            return 0, log

        while True:
            removed_flag, count, color = self._remove_first_chain()
            
            if removed_flag == 0:
                break
                
            total_destroyed += count
            log.append(f"  [ШАГ {step}] Найдена цепочка из {count} шариков цвета {color}. Они уничтожены.")
            step += 1

        if total_destroyed == 0:
            log.append("  [ИНФО] Цепочки из 3 и более шариков не найдены. Ничего не уничтожено.")
        else:
            log.append(f"  [ИТОГ] Всего уничтожено шариков: {total_destroyed}")

        return total_destroyed, log

    def _remove_first_chain(self) -> tuple[int, int, int]:
        i = 0
        n = len(self.balls)
        
        while i < n:
            count = 1
            while i + count < n and self.balls[i + count] == self.balls[i]:
                count += 1
            
            if count >= 3:
                color = self.balls[i]
                del self.balls[i : i + count]
                return 1, count, color
            
            i += count
            
        return 0, 0, 0