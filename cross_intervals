from typing import List


def find_max_overlap(intervals: List[List[int]]) -> int:
    """
    Определяет наибольшее количество пересекающихся интервалов.

    Параметры:
        intervals (List[List[int]]): Список интервалов вида [[начало, конец], ...].

    Возвращает:
        int: Количество максимальных пересечений.
    """
    # Формируем события (начала и окончания интервалов)
    events = []
    for start, end in intervals:
        events.append((start, +1))  # Начала интервалов
        events.append((end, -1))    # Концы интервалов

    # Сортируем события по точке времени и типу события
    events.sort(key=lambda x: (x[0], x[1]))

    active_count = 0              # Текущее количество активных интервалов
    max_overlaps = 0              # Максимальная величина пересечений

    # Проходим по отсортированным событиям
    for point, type_event in events:
        active_count += type_event
        max_overlaps = max(max_overlaps, active_count)

    return max_overlaps


if __name__ == "__main__":
    # Тестируем функцию на примере
    intervals = [[1, 2], [4, 10], [3, 7], [2, 8], [5, 9], [6, 11]]
    result = find_max_overlap(intervals)
    print(f"Наибольшее количество пересекающихся интервалов: {result}")
