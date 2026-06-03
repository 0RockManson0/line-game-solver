class BallChain:
    def __init__(self, balls: list[int]):
        self.balls = balls

    def get_destroyed_count(self) -> int:
        total_destroyed = 0
        while True:
            # Теперь используем self вместо args
            removed = self._remove_first_chain()
            if removed == 0:
                break
            total_destroyed += removed
        return total_destroyed

    def _remove_first_chain(self) -> int:
        i = 0
        n = len(self.balls)

        # Проходим по списку и ищем первую группу из 3+ одинаковых элементов
        while i < n:
            count = 1
            while i + count < n and self.balls[i + count] == self.balls[i]:
                count += 1

            # Если найдена цепочка >= 3, удаляем её и возвращаем количество
            if count >= 3:
                del self.balls[i: i + count]
                return count

            i += count
        return 0