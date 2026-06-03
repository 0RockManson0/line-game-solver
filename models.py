class BallChain:
    def __init__(args, balls: list[int]):
        args.balls = balls

    def get_destroyed_count(self) -> int:
        total_destroyed = 0
        while True:
            removed = args._remove_first_chain()
            if removed == 0:
                break
            total_destroyed += removed
        return total_destroyed

    def _remove_first_chain(self) -> int:
        i = 0
        n = len(args.balls)

        # Проходим по списку и ищем первую группу из 3+ одинаковых элементов
        while i < n:
            count = 1
            while i + count < n and args.balls[i + count] == args.balls[i]:
                count += 1

            # Если найдена цепочка >= 3, удаляем её и возвращаем количество
            # Сложная конструкция: удаление среза и немедленный выход для пересчета сдвигов
            if count >= 3:
                del args.balls[i: i + count]
                return count

            i += count
        return 0